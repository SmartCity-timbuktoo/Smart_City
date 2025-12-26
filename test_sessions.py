"""
Tests for session management functionality in Addis-Sync agents
"""

import pytest
from smart_city_agent.session_manager import (
    get_session_service,
    create_session_id,
    create_user_id,
    SessionStateHelper
)


def test_session_creation():
    """Test creating a new session"""
    service = get_session_service()
    user_id = create_user_id()
    session_id = create_session_id()
    
    session = service.create_session(user_id, session_id)
    
    assert session is not None
    assert session.user_id == user_id
    assert session.session_id == session_id


def test_session_persistence():
    """Test that sessions persist across get calls"""
    service = get_session_service()
    user_id = create_user_id()
    session_id = create_session_id()
    
    # Create session
    session1 = service.create_session(user_id, session_id)
    session1.state['test_key'] = 'test_value'
    
    # Get same session again
    session2 = service.get_or_create(user_id, session_id)
    
    assert session2.state.get('test_key') == 'test_value'


def test_session_isolation():
    """Test that different users have isolated sessions"""
    service = get_session_service()
    
    user1_id = create_user_id()
    user2_id = create_user_id()
    session_id = create_session_id()
    
    # Create sessions for two different users
    session1 = service.create_session(user1_id, session_id)
    session1.state['user_data'] = 'user1_data'
    
    session2 = service.create_session(user2_id, session_id)
    session2.state['user_data'] = 'user2_data'
    
    # Verify isolation
    session1_check = service.get_or_create(user1_id, session_id)
    session2_check = service.get_or_create(user2_id, session_id)
    
    assert session1_check.state['user_data'] == 'user1_data'
    assert session2_check.state['user_data'] == 'user2_data'


def test_session_state_helper():
    """Test SessionStateHelper utilities"""
    service = get_session_service()
    user_id = create_user_id()
    session_id = create_session_id()
    session = service.create_session(user_id, session_id)
    
    # Test woreda storage
    SessionStateHelper.set_user_woreda(session, 'Bole')
    assert SessionStateHelper.get_user_woreda(session) == 'Bole'
    
    # Test issue type
    SessionStateHelper.set_current_issue_type(session, 'power_outage')
    assert SessionStateHelper.get_current_issue_type(session) == 'power_outage'
    
    # Test ticket storage
    SessionStateHelper.set_last_ticket(session, 'POWR-ABC12345', 'Power')
    ticket_info = SessionStateHelper.get_last_ticket(session)
    assert ticket_info is not None
    assert ticket_info['ticket_number'] == 'POWR-ABC12345'
    assert ticket_info['service_type'] == 'Power'
    
    # Test user preferences
    SessionStateHelper.set_user_preference(session, 'language', 'am')
    assert SessionStateHelper.get_user_preference(session, 'language') == 'am'


def test_session_context_clearing():
    """Test clearing session context while preserving user preferences"""
    service = get_session_service()
    user_id = create_user_id()
    session_id = create_session_id()
    session = service.create_session(user_id, session_id)
    
    # Set both session and user data
    session.state['current_issue'] = 'power'
    session.state['user:woreda'] = 'Bole'
    session.state['user:language'] = 'en'
    
    # Clear current context
    SessionStateHelper.clear_current_context(session)
    
    # Session data should be cleared
   assert 'current_issue' not in session.state
    
    # User preferences should remainassert session.state.get('user:woreda') == 'Bole'
    assert session.state.get('user:language') == 'en'


def test_session_metadata():
    """Test session metadata tracking"""
    service = get_session_service()
    user_id = create_user_id()
    session_id = create_session_id()
    
    session = service.create_session(user_id, session_id)
    
    # Get metadata
    metadata = service.get_session_info(user_id, session_id)
    
    assert metadata is not None
    assert metadata['user_id'] == user_id
    assert metadata['session_id'] == session_id
    assert 'created_at' in metadata
    assert 'last_accessed' in metadata
