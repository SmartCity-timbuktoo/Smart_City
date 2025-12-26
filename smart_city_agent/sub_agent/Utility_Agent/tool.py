"""
Utility Agent tool stubs.
Actual implementation is in the MCP server.
"""

def get_utility_office_by_woreda(woreda_name: str) -> dict:
    """Get utility office information for a given woreda."""
    pass


def create_utility_ticket(
    woreda: str,
    issue_description: str,
    user_contact: str | None = None,
) -> dict:
    """Create a new utility issue ticket."""
    pass


def get_ticket_status(ticket_number: str) -> dict:
    """Get the status of a utility ticket."""
    pass
