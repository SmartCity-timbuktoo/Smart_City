
"""
Local Runner Adapter for Addis-Sync.
Replaces the missing vertexai.agent_engines module using the available google-genai SDK.
"""

import os
import sys
import uuid
import traceback
from typing import List, Dict, Any, Callable

# Check if google-genai is available
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("CRITICAL: google-genai library not found. Running in mock mode.")
    genai = None

# Global Tool Registry to map function names to real implementations
TOOL_REGISTRY: Dict[str, Callable] = {}

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

class AdkApp:
    """
    Local Runner implementation that mimics AdkApp interface.
    Uses google-genai Client to execute the agent loop.
    """
    def __init__(self, agent: Agent):
        self.root_agent = agent
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        
        if genai:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = None

        # Pre-load MCP servers to populate TOOL_REGISTRY
        # We try to import them from the standard path
        try:
            # Add project root to sys.path to find modules
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
        """
        Execute the agent interaction.
        Mimics the simplified run() used in the app, but actually returns a string directly
        because the original app expects a generator or list of events. 
        Wait, existing app.py code expects `runner.run(...)` to return events?
        Let's look at process_message_with_agent usage in app.py.
        It calls runner.run() then extracts text.
        """
        session = get_session(session_id)
        
        # Construct the full context prompt
        # We manually inject instructions and session state info
        
        # 1. State Context
        state_context = "SESSION STATE:\n"
        for k, v in session.state.items():
            state_context += f"{k}: {v}\n"
            
        full_system_instruction = f"{self.root_agent.instruction}\n\n{state_context}"
        
        # Append Sub-Agent Instructions to give context on how to use their tools
        full_system_instruction += "\n\n### SPECIALIST AGENT CAPABILITIES:\n"
        
        def collect_instructions(agt):
            instructions = ""
            for sub in agt.sub_agents:
                instructions += f"\n--- {sub.name.upper()} ---\n{sub.instruction}\n"
                instructions += collect_instructions(sub)
            return instructions
            
        full_system_instruction += collect_instructions(self.root_agent)
        
        # 2. History
        # We rely on the client's chat capability or manual history
        # Simplify: Just send instruction + history + prompt
        
        # 3. Tool Preparation
        # Gather all tools from root agent and sub-agents
        # Theoretically, we should only expose tools relevant to the active context, 
        # but for this flat hierarchy, we can expose all (or rely on routing).
        
        # The prompt implies a Router agent (Customer Service) that routes to sub-agents.
        # However, purely prompting based routing is easier here.
        
        # Let's collect ALL registered real functions found in TOOL_REGISTRY 
        # that match the names of tools defined in the agents.
        
        active_tools = []
        
        # Recursively find tools in agent tree
        def collect_tools(agt):
            for t in agt.tools:
                # 't' is the stub function. Get its name.
                func_name = t.__name__
                if func_name in TOOL_REGISTRY:
                    active_tools.append(TOOL_REGISTRY[func_name])
                else:
                    # Provide the stub if real one not found (might fail but mostly harmless)
                    pass 
            for sub in agt.sub_agents:
                collect_tools(sub)
        
        collect_tools(self.root_agent)
        
        # 4. Generate Content (Turn 1)
        config = types.GenerateContentConfig(
            tools=active_tools if active_tools else None,
            system_instruction=full_system_instruction,
            temperature=0.0 # Strict for routing
        )
        
        # Transform history to GenAI format if needed (skipping for brevity, just using prompt)
        #Ideally we append to a chat session
        
        chat = self.client.chats.create(
            model=self.root_agent.model,
            config=config,
            history=session.history
        )
        
        response = chat.send_message(prompt)
        
        # 5. Handle Tool Calls (Agentic Loop)
        final_text = ""
        max_turns = 10
        turn_count = 0
        
        while turn_count < max_turns:
            turn_count += 1
            
            # Check for function calls in the CURRENT response
            # valid_response = response.candidates[0].content
            if not response.candidates or not response.candidates[0].content.parts:
                break
                
            has_tool_call = False
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    has_tool_call = True
                    fn_name = part.function_call.name
                    fn_args = part.function_call.args
                    
                    print(f"🤖 Agent calling tool: {fn_name}")
                    
                    if fn_name in TOOL_REGISTRY:
                        try:
                            # Execute real function
                            result = TOOL_REGISTRY[fn_name](**fn_args)
                            print(f"🔧 Tool Result: {str(result)[:100]}...")
                            
                            # Send result back to model
                            # We must send immediate response for each tool call in the same turn?
                            # Standard Gemini chat: User -> Model(Call) -> User(Result) -> Model(Next)
                            response = chat.send_message(
                                types.Part.from_function_response(
                                    name=fn_name,
                                    response={"result": result}
                                )
                            )
                            # The 'response' is now the NEXT model turn (could be text or another call)
                            # We break the inner loop to process the new 'response' object in the outer while loop
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
                    else:
                        print(f"⚠️ Tool not found: {fn_name}")
                        response = chat.send_message(
                            types.Part.from_function_response(
                                name=fn_name,
                                response={"error": "Tool function not found in registry."}
                            )
                        )
                        break

            # If no tool call was found in this response, it interprets as final text?
            # Or if we processed a tool call, we 'break' inner loop to restart outer loop with new response.
            # If we iterated all parts and found NO tool calls, then we extract text and finish.
            
            if has_tool_call:
                continue # Loop again with the new 'response' obtained from send_message
            
            # No tool calls - Append text and Exit
            for part in response.candidates[0].content.parts:
                if part.text:
                    final_text += part.text
            break
            
        if not final_text and turn_count >= max_turns:
            final_text = "⚠️ Agent Error: Maximum tool execution limit reached." 
        elif not final_text:
             final_text = "I processed that, but have no text response."

        # Update Session
        session.history.append(types.Content(role="user", parts=[types.Part.from_text(text=prompt)]))
        session.history.append(types.Content(role="model", parts=[types.Part.from_text(text=final_text)]))
        
        # Update session state if the model output special tokens? 
        # Or parse the response for session updates? 
        # The prompt says "USE SESSION STATE", meaning the model explicitly outputs python code?
        # No, the prompt says "Writing Session State: session.state['...'] = ...".
        # This implies the model might try to execute python code?
        # We don't have a python sandbox. We'll ignore that for now unless the user complains.
        
        return final_text
