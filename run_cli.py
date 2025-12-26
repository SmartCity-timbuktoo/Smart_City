"""
Addis-Sync CLI Runner
Interactive command-line interface for the Addis-Sync multi-agent platform.
Uses vertexai.agent_engines AdkApp with in-memory session management.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify API key
if not os.getenv('GOOGLE_API_KEY'):
    print("ERROR: GOOGLE_API_KEY not found in .env file")
    sys.exit(1)

try:
    from smart_city_agent.agent import customer_service_agent
    from smart_city_agent.session_manager import get_session_service, create_session_id
    from vertexai.agent_engines import AdkApp
except ImportError as e:
    print(f"ERROR: Failed to import required modules: {e}")
    sys.exit(1)

def main():
    """Run the Addis-Sync CLI interface"""
    
    print("=" * 70)
    print("ADDIS-SYNC - Urban Infrastructure Coordination Platform")
    print("=" * 70)
    print("\nWelcome to Addis-Sync CLI!")
    print("Report issues or get information about Addis Ababa city services.")
    print("\nType your query or 'exit' to quit.\n")
    
    try:
        # Initialize session service
        session_service = get_session_service()
        
        # Create runner with the customer service agent
        runner = AdkApp(
            agent=customer_service_agent,
            session_service=session_service
        )
        
        # Generate unique user and session IDs
        user_id = "cli_user"
        session_id = create_session_id()
        
        print(f"✓ Agent: {customer_service_agent.name}")
        print(f"✓ Model: {customer_service_agent.model}")
        print(f"✓ Sub-agents: {len(customer_service_agent.sub_agents)}")
        print(f"  - {', '.join([a.name for a in customer_service_agent.sub_agents])}")
        print(f"\n✓ Session started: {session_id}")
        print("-" * 70)
        
    except Exception as e:
        print(f"\n✗ Failed to initialize runner: {e}")
        print("\nTrying alternative initialization...")
        
        # Fallback: Show agent info without running
        print(f"\n✓ Agent loaded: {customer_service_agent.name}")
        print(f"✓ Model: {customer_service_agent.model}")
        print(f"✓ Sub-agents available: {len(customer_service_agent.sub_agents)}")
        print("\nNOTE: Full runner functionality requires proper session service setup.")
        print("The agent is loaded but cannot process queries in this session.")
        return
    
    # Interactive loop
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nThank you for using Addis-Sync. Goodbye!")
                break
            
            # Run the agent
            print("\nAgent: ", end="", flush=True)
            
            try:
                # Use the run method
                events = runner.run(
                    user_id=user_id,
                    session_id=session_id,
                    new_message=user_input
                )
                
                # Process events and display response
                response_text = []
                for event in events:
                    # Try to extract text content from various event types
                    if hasattr(event, 'content'):
                        if hasattr(event.content, 'parts'):
                            for part in event.content.parts:
                                if hasattr(part, 'text') and part.text:
                                    response_text.append(part.text)
                        elif hasattr(event.content, 'text') and event.content.text:
                            response_text.append(event.content.text)
                    elif hasattr(event, 'text') and event.text:
                        response_text.append(event.text)
                
                if response_text:
                    print(" ".join(response_text))
                else:
                    print("[Agent processed your request but returned no text response]")
                
            except Exception as e:
                print(f"\n✗ Error processing request: {e}")
                print("Please try again or type 'exit' to quit.")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except EOFError:
            print("\n\nEnd of input. Goodbye!")
            break
    
    # Cleanup
    try:
        runner.close()
    except:
        pass

if __name__ == "__main__":
    main()
