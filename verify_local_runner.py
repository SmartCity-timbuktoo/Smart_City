
import os
import sys
import traceback
from dotenv import load_dotenv

# Ensure project root is in path
sys.path.append(os.getcwd())

try:
    load_dotenv()
    print("DOTENV loaded")
    
    from smart_city_agent.local_runner import AdkApp, Agent, TOOL_REGISTRY
    print("✅ Local Runner Imported")
    
    # Import root agent
    from smart_city_agent.agent import customer_service_agent
    print(f"✅ Root Agent Loaded: {customer_service_agent.name}")
    
    # Check Registry
    print(f"✅ Tool Registry Size: {len(TOOL_REGISTRY)}")
    
    # Initialize App
    app = AdkApp(agent=customer_service_agent)
    print("✅ AdkApp Initialized")
    
    # Check Registry AFTER initialization
    print(f"✅ Tool Registry Size: {len(TOOL_REGISTRY)}")
    
    # Run simple query
    print("Type: 'What can you help me with?'")
    try:
        response = app.run(user_id="test", session_id="test_session", prompt="What can you help me with?")
        print(f"✅ Response Received: {response[:100]}...")
    except Exception as e:
        print(f"❌ Run Failed: {e}")
        # traceback.print_exc()

except Exception as e:
    with open("verification.log", "w") as f:
        f.write(f"❌ Critical Failure: {e}\nTraceback:\n{traceback.format_exc()}")
    print(f"❌ Critical Failure: {e}")

# Flush stdout
sys.stdout.flush()

# Redirect stdout/stderr to capture ALL output including imports
class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.filename = filename
        # Clear file
        with open(self.filename, 'w') as f:
            f.write("STARTING VERIFICATION\n")

    def write(self, message):
        self.terminal.write(message)
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(message)

    def flush(self):
        self.terminal.flush()

sys.stdout = Logger("verification.log")
sys.stderr = sys.stdout

def log(msg):
    print(msg) # Now prints to both

try:
    log("DOTENV loaded")
    
    from smart_city_agent.local_runner import AdkApp, Agent, TOOL_REGISTRY
    log("✅ Local Runner Imported")
    
    # Import root agent
    from smart_city_agent.agent import customer_service_agent
    log(f"✅ Root Agent Loaded: {customer_service_agent.name} (Model: {customer_service_agent.model})")
    
    # Initialize App
    app = AdkApp(agent=customer_service_agent)
    log("✅ AdkApp Initialized")
    
    # Check Registry AFTER initialization
    log(f"✅ Tool Registry Size: {len(TOOL_REGISTRY)}")
    log(f"📋 Registered Tools: {list(TOOL_REGISTRY.keys())}")
    
    # Run simple query
    log("Running query 'What can you help me with?'...")
    response = app.run(user_id="test", session_id="test_session", prompt="What can you help me with?")
    log(f"✅ Response Received: {response[:100]}...")

except Exception as e:
    log(f"❌ Run Failed: {e}")
    # traceback.print_exc()
