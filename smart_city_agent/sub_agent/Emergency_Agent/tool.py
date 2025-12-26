"""
Emergency Agent tool stubs.
Actual implementation is in the MCP server.
"""

def find_closest_emergency_office(woreda_name: str) -> dict:
    """Find the nearest emergency office for a given woreda."""
    pass


def create_emergency_ticket(
    woreda: str,
    emergency_type: str,
    issue_description: str,
    user_contact: str | None = None,
    location_details: str | None = None,
) -> dict:
    """Create a new emergency ticket."""
    pass


def get_emergency_ticket_status(ticket_number: str) -> dict:
    """Get the status of an emergency ticket."""
    pass
