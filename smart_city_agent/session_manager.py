"""
Session Management for Addis-Sync Multi-Agent System

Provides centralized session management using Google ADK's SessionService.
Supports both in-memory (development) and database-backed (production) sessions.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from .local_runner import Session


class AddisSessionService(InMemorySessionService):
    """
    Enhanced InMemorySessionService with additional features for Addis-Sync.
    
    Features:
    - User-specific session isolation
    - Session expiration tracking
    - Conversation context utilities
    - State management helpers
    """
    
    def __init__(self, session_timeout_minutes: int = 120):
        """
        Initialize the session service.
        
        Args:
            session_timeout_minutes: Minutes before a session is considered expired (default: 2 hours)
        """
        super().__init__()
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
        self._session_metadata: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, user_id: str, session_id: Optional[str] = None) -> Session:
        """
        Create a new session for a user.
        
        Args:
            user_id: Unique identifier for the user
            session_id: Optional session ID. If not provided, generates a new UUID
        
        Returns:
            Session object
        """
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        # Create session using parent class
        session = super().get_or_create(user_id=user_id, session_id=session_id)
        
        # Store metadata
        self._session_metadata[f"{user_id}:{session_id}"] = {
            'created_at': datetime.now(),
            'last_accessed': datetime.now(),
            'user_id': user_id,
            'session_id': session_id
        }
        
        return session
    
    def get_or_create(self, user_id: str, session_id: str) -> Session:
        """
        Get existing session or create new one.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
        
        Returns:
            Session object
        """
        key = f"{user_id}:{session_id}"
        
        # Check if session exists
        if key in self._session_metadata:
            # Update last accessed time
            self._session_metadata[key]['last_accessed'] = datetime.now()
        else:
            # Create new session
            return self.create_session(user_id, session_id)
        
        # Get session from parent
        return super().get_or_create(user_id=user_id, session_id=session_id)
    
    def is_session_expired(self, user_id: str, session_id: str) -> bool:
        """
        Check if a session has expired.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
        
        Returns:
            True if expired, False otherwise
        """
        key = f"{user_id}:{session_id}"
        
        if key not in self._session_metadata:
            return True
        
        last_accessed = self._session_metadata[key]['last_accessed']
        return datetime.now() - last_accessed > self.session_timeout
    
    def cleanup_expired_sessions(self) -> int:
        """
        Remove expired sessions from memory.
        
        Returns:
            Number of sessions cleaned up
        """
        expired_keys = []
        
        for key, metadata in self._session_metadata.items():
            if datetime.now() - metadata['last_accessed'] > self.session_timeout:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self._session_metadata[key]
            # Note: Parent class handles actual session cleanup
        
        return len(expired_keys)
    
    def get_session_info(self, user_id: str, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata about a session.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
        
        Returns:
            Session metadata or None if not found
        """
        key = f"{user_id}:{session_id}"
        return self._session_metadata.get(key)


class SessionStateHelper:
    """
    Helper utilities for managing session state in Addis-Sync agents.
    
    Provides convenience methods for storing and retrieving conversation context.
    """
    
    @staticmethod
    def set_user_woreda(session: Session, woreda: str) -> None:
        """Store user's woreda for future reference."""
        session.state['user:woreda'] = woreda
    
    @staticmethod
    def get_user_woreda(session: Session) -> Optional[str]:
        """Retrieve user's stored woreda."""
        return session.state.get('user:woreda')
    
    @staticmethod
    def set_current_issue_type(session: Session, issue_type: str) -> None:
        """Store the type of issue being discussed."""
        session.state['current_issue_type'] = issue_type
    
    @staticmethod
    def get_current_issue_type(session: Session) -> Optional[str]:
        """Get the current issue type."""
        return session.state.get('current_issue_type')
    
    @staticmethod
    def set_last_ticket(session: Session, ticket_number: str, service_type: str) -> None:
        """Store the last ticket created in this session."""
        session.state['last_ticket_number'] = ticket_number
        session.state['last_ticket_service'] = service_type
        session.state['last_ticket_created'] = datetime.now().isoformat()
    
    @staticmethod
    def get_last_ticket(session: Session) -> Optional[Dict[str, str]]:
        """Retrieve the last ticket information."""
        ticket_number = session.state.get('last_ticket_number')
        if ticket_number:
            return {
                'ticket_number': ticket_number,
                'service_type': session.state.get('last_ticket_service'),
                'created_at': session.state.get('last_ticket_created')
            }
        return None
    
    @staticmethod
    def set_user_preference(session: Session, key: str, value: Any) -> None:
        """Store a user preference with 'user:' prefix for persistence."""
        session.state[f'user:{key}'] = value
    
    @staticmethod
    def get_user_preference(session: Session, key: str, default: Any = None) -> Any:
        """Get a user preference."""
        return session.state.get(f'user:{key}', default)
    
    @staticmethod
    def clear_current_context(session: Session) -> None:
        """Clear session-scoped context (not user preferences)."""
        keys_to_remove = [k for k in session.state.keys() if not k.startswith('user:')]
        for key in keys_to_remove:
            del session.state[key]
    
    @staticmethod
    def add_to_history(session: Session, entry: str) -> None:
        """Add an entry to conversation history."""
        if 'conversation_history' not in session.state:
            session.state['conversation_history'] = []
        session.state['conversation_history'].append({
            'timestamp': datetime.now().isoformat(),
            'entry': entry
        })


# Global session service instance
_session_service: Optional[AddisSessionService] = None


def get_session_service(session_timeout_minutes: int = 120) -> AddisSessionService:
    """
    Get or create the global session service instance.
    
    Args:
        session_timeout_minutes: Session timeout in minutes (default: 2 hours)
    
    Returns:
        AddisSessionService instance
    """
    global _session_service
    
    if _session_service is None:
        _session_service = AddisSessionService(session_timeout_minutes=session_timeout_minutes)
    
    return _session_service


def create_session_id() -> str:
    """Generate a new unique session ID."""
    return str(uuid.uuid4())


def create_user_id() -> str:
    """Generate a new unique user ID."""
    return str(uuid.uuid4())
