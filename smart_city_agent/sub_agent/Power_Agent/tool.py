"""
Power Agent tool stubs.
Actual implementation is in the MCP server.
"""

def get_power_office_by_woreda(woreda_name: str) -> dict:
    """Get power office information for a given woreda."""
    pass


def create_power_ticket(
    woreda: str,
    issue_description: str,
    user_contact: str | None = None,
) -> dict:
    """Create a new power issue ticket."""
    pass


def get_power_ticket_status(ticket_number: str) -> dict:
    """Get the status of a power ticket."""
    pass
