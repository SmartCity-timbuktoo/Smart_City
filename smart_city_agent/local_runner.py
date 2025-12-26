"""
Local Runner Adapter for Addis-Sync.
Replaces the missing vertexai.agent_engines module using the available google-genai SDK.
Now supports OpenRouter Fallback!
"""

import os
import sys
import uuid
import inspect
import json
import traceback
from typing import List, Dict, Any, Callable
from dotenv import load_dotenv
from pathlib import Path

# Load env vars from project root (3 levels up from this file: smart_city_agent/local_runner.py)
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"DEBUG: Loaded .env from {env_path}")
else:
    load_dotenv() # Fallback to default search
    print("DEBUG: Loaded .env from default search")

# Provider Imports
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("CRITICAL: google-genai library not found. Running in mock mode.")
    genai = None

try:
    import openai
except ImportError:
    openai = None
    print("WARNING: openai library not found. OpenRouter fallback will be disabled.")

# Global Tool Registry
TOOL_REGISTRY: Dict[str, Callable] = {}

# User-requested Free Models
OPENROUTER_MODELS = [
    "meta-llama/llama-3.2-3b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "nousresearch/hermes-3-llama-3.1-405b:free",
    "tngtech/deepseek-r1t2-chimera:free",
    "meta-llama/llama-3.3-70b-instruct:free"
]

class MCPServer:
    """Mock MCPServer that registers tools to the global registry."""
    def __init__(self, name: str):
        self.name = name

    def tool(self):
        def decorator(func):
            # Register the real function by name
            print(f"DEBUG: Registering tool {func.__name__} in {self.name}")
            TOOL_REGISTRY[func.__name__] = func
            # Return the function as is
            return func
        return decorator

class Session:
    """Simple in-memory session state."""
    def __init__(self, session_id: str):
        self.id = session_id
        self.history = []
        self.state = {} # Arbitrary key-value storage for agents

class InMemorySessionService:
    """Mock implementation of Google ADK session service."""
    def __init__(self):
        pass

    def get_or_create(self, session_id: str, user_id: str = None) -> Session:
        return get_session(session_id)

SESSION_STORE: Dict[str, Session] = {}

def get_session(session_id: str) -> Session:
    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = Session(session_id)
    return SESSION_STORE[session_id]

class Agent:
    """Agent definition compatible with google.adk.agents.Agent."""
    def __init__(
        self,
        name: str,
        model: str,
        description: str = "",
        instruction: str = "",
        tools: List[Callable] = None,
        sub_agents: List['Agent'] = None,
        server=None # ignored compatibility arg
    ):
        self.name = name
        self.model = model
        self.description = description
        self.instruction = instruction
        self.tools = tools or []
        self.sub_agents = sub_agents or []

def get_function_schema(func: Callable) -> dict:
    """Convert a Python function to OpenAI Tool Schema."""
    sig = inspect.signature(func)
    doc = inspect.getdoc(func) or "No description provided."
    
    properties = {}
    required = []
    
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        type(None): "null"
    }

    for name, param in sig.parameters.items():
        param_type = type_map.get(param.annotation, "string") # Default to string
        properties[name] = {
            "type": param_type,
            "description": f"Parameter: {name}" 
        }
        if param.default == inspect.Parameter.empty:
            required.append(name)
            
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": doc,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }

class AdkApp:
    """
    Local Runner implementation that mimics AdkApp interface.
    Supports Dual-Mode: Gemini (Primary) -> OpenRouter (Fallback).
    """
    def __init__(self, agent: Agent):
        self.root_agent = agent
        
        # Load Gemini Client
        self.gemini_key = os.environ.get("GOOGLE_API_KEY")
        self.gemini_client = None
        if self.gemini_key and genai:
            self.gemini_client = genai.Client(api_key=self.gemini_key)
            print(f"DEBUG: Gemini Client Initialized (Key: {self.gemini_key[:4]}***)")
        else:
            print(f"DEBUG: Gemini Client MISSING (Key: {bool(self.gemini_key)}, Lib: {bool(genai)})")
            
        # Load OpenRouter Client
        self.openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        self.openrouter_client = None
        if self.openrouter_key and openai:
            self.openrouter_client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.openrouter_key,
            )
            print(f"DEBUG: OpenRouter Client Initialized (Key: {self.openrouter_key[:4]}***)")
        else:
            print(f"DEBUG: OpenRouter Client MISSING (Key: {bool(self.openrouter_key)}, Lib: {bool(openai)})")

        # Pre-load MCP servers
        try:
            project_root = os.getcwd()
            if project_root not in sys.path:
                sys.path.append(project_root)
                
            from smart_city_agent.mcp_server import (
                emergency_server, 
                power_server, 
                sanitation_server, 
                infrastructure_server, 
                utility_server
            )
            print(f"✅ LocalRunner: Loaded MCP Servers. Registry size: {len(TOOL_REGISTRY)}")
        except Exception as e:
            print(f"⚠️ LocalRunner: Failed to auto-load MCP servers: {e}")

    def run(self, user_id: str, session_id: str, prompt: str) -> str:
        """Main execution entry point."""
        
        # Try Gemini First
        if self.gemini_client:
            try:
                print("🔵 Attempting execution with Gemini...")
                return self.run_with_gemini(user_id, session_id, prompt)
            except Exception as e:
                print(f"⚠️ Gemini execution failed: {e}")
                print("🔄 Switching to OpenRouter Fallback...")
        
        # Fallback to OpenRouter
        if self.openrouter_client:
            try:
                return self.run_with_openrouter(user_id, session_id, prompt)
            except Exception as e:
                return f"❌ All providers failed. OpenRouter error: {e}"
        else:
            return "❌ Configuration Error: Neither Gemini (failed) nor OpenRouter (missing key) are available."

    def _prepare_context(self, session: Session) -> tuple[str, list[Callable]]:
        """Common context preparation helper."""
        # 1. State Context
        state_context = "SESSION STATE:\n"
        for k, v in session.state.items():
            state_context += f"{k}: {v}\n"
            
        full_system_instruction = f"{self.root_agent.instruction}\n\n{state_context}"
        
        # 2. Sub-Agent Instructions
        full_system_instruction += "\n\n### SPECIALIST AGENT CAPABILITIES:\n"
        def collect_instructions(agt):
            instructions = ""
            for sub in agt.sub_agents:
                instructions += f"\n--- {sub.name.upper()} ---\n{sub.instruction}\n"
                instructions += collect_instructions(sub)
            return instructions
        full_system_instruction += collect_instructions(self.root_agent)
        
        # 3. Collect Tools
        active_tools = []
        def collect_tools(agt):
            for t in agt.tools:
                if t.__name__ in TOOL_REGISTRY:
                    active_tools.append(TOOL_REGISTRY[t.__name__])
            for sub in agt.sub_agents:
                collect_tools(sub)
        collect_tools(self.root_agent)
        
        return full_system_instruction, active_tools

    def run_with_gemini(self, user_id: str, session_id: str, prompt: str) -> str:
        session = get_session(session_id)
        if not self.gemini_client:
            raise ValueError("Gemini client not initialized")

        instruction, tools = self._prepare_context(session)
        
        config = types.GenerateContentConfig(
            tools=tools if tools else None,
            system_instruction=instruction,
            temperature=0.0
        )
        
        chat = self.gemini_client.chats.create(
            model=self.root_agent.model,
            config=config,
            history=session.history
        )
        
        response = chat.send_message(prompt)
        
        # Gemini Agentic Loop
        final_text = ""
        max_turns = 10
        turn_count = 0
        
        while turn_count < max_turns:
            turn_count += 1
            if not response.candidates or not response.candidates[0].content.parts:
                break
                
            has_tool_call = False
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    has_tool_call = True
                    fn_name = part.function_call.name
                    fn_args = part.function_call.args
                    print(f"🤖 (Gemini) calling tool: {fn_name}")
                    
                    if fn_name in TOOL_REGISTRY:
                        try:
                            result = TOOL_REGISTRY[fn_name](**fn_args)
                            print(f"🔧 Tool Result: {str(result)[:100]}...")
                            response = chat.send_message(
                                types.Part.from_function_response(
                                    name=fn_name,
                                    response={"result": result}
                                )
                            )
                            break
                        except Exception as e:
                            print(f"❌ Tool Error: {e}")
                            response = chat.send_message(
                                types.Part.from_function_response(
                                    name=fn_name,
                                    response={"error": str(e)}
                                )
                            )
                            break
            
            if has_tool_call:
                continue
            
            for part in response.candidates[0].content.parts:
                if part.text:
                    final_text += part.text
            break
            
        if not final_text:
            final_text = "I processed that, but have no text response."

        # Update Session history (Google Format)
        session.history.append(types.Content(role="user", parts=[types.Part.from_text(text=prompt)]))
        session.history.append(types.Content(role="model", parts=[types.Part.from_text(text=final_text)]))
        
        return final_text

    def run_with_openrouter(self, user_id: str, session_id: str, prompt: str) -> str:
        session = get_session(session_id)
        instruction, tools = self._prepare_context(session)
        
        # Convert Tools to OpenAI Format
        openai_tools = [get_function_schema(t) for t in tools] if tools else None
        
        # Build Messages (Context + Instruction + History Conversion)
        messages = [{"role": "system", "content": instruction}]
        
        # Convert existing Google History to OpenAI
        # This is a lossy conversion (simple text only) for fallback
        for content in session.history:
            parts = content.parts
            text = " ".join([p.text for p in parts if p.text])
            messages.append({"role": content.role, "content": text})
            
        messages.append({"role": "user", "content": prompt})
        
        # Fallback Loop
        # Try models in order until one works
        for model in OPENROUTER_MODELS:
            try:
                print(f"🟠 (OpenRouter) Trying model: {model}")
                return self._execute_openai_loop(messages, openai_tools, model, session, prompt)
            except Exception as e:
                print(f"⚠️ Model {model} failed: {e}")
                continue
                
        raise RuntimeError("All OpenRouter fallback models failed.")

    def _execute_openai_loop(self, messages, tools, model, session, original_prompt):
        """Standard OpenAI ReAct Loop"""
        final_text = ""
        max_turns = 10
        turn_count = 0
        
        while turn_count < max_turns:
            turn_count += 1
            
            completion = self.openrouter_client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto" if tools else None
            )
            
            msg = completion.choices[0].message
            messages.append(msg)
            
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    fn_name = tool_call.function.name
                    fn_args = json.loads(tool_call.function.arguments)
                    print(f"🤖 (OpenRouter) calling tool: {fn_name}")
                    
                    result_str = ""
                    if fn_name in TOOL_REGISTRY:
                        try:
                            result = TOOL_REGISTRY[fn_name](**fn_args)
                            result_str = json.dumps(result)
                            print(f"🔧 Tool Result: {result_str[:100]}...")
                        except Exception as e:
                            result_str = json.dumps({"error": str(e)})
                    else:
                        result_str = json.dumps({"error": "Function not found"})
                        
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result_str
                    })
                # Loop continues to send tool results back to model
            else:
                final_text = msg.content
                break
                
        # Update Session History (Back-convert to Google Format for continuity)
        # Note: We append the simplified interaction
        if genai:
             session.history.append(types.Content(role="user", parts=[types.Part.from_text(text=original_prompt)]))
             session.history.append(types.Content(role="model", parts=[types.Part.from_text(text=final_text or "")]))
        
        return final_text or "No response generated."
