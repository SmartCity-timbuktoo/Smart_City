"""
Helper function for processing chat messages in Streamlit app
Extracted to simplify the main app.py logic
"""

def process_message_with_agent(runner, user_id, session_id, prompt):
    """
    Process a user message using the ADK Runner.
    
    Args:
        runner: ADK Runner instance
        user_id: User identifier
        session_id: Session identifier
        prompt: User's message
    
    Returns:
        str: Agent's response
    """
    try:
        # Use ADK Runner to process the message
        events = runner.run(
            user_id=user_id,
            session_id=session_id,
            prompt=prompt
        )
        
        if isinstance(events, str):
            return events
        
        # Extract response from events
        response_parts = []
        for event in events:
            # Extract text from various event types
            if hasattr(event, 'content'):
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_parts.append(part.text)
                elif hasattr(event.content, 'text') and event.content.text:
                    response_parts.append(event.content.text)
            elif hasattr(event, 'text') and event.text:
                response_parts.append(event.text)
        
        # Combine response
        if response_parts:
            return " ".join(response_parts)
        else:
            return "I've processed your request. How else can I help you?"
    
    except Exception as e:
        raise Exception(f"ADK Runner error: {str(e)}")
