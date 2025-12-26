"""
Sanitation Agent tool stubs.
Actual implementation is in the MCP server.
"""

def get_sanitation_office_by_woreda(woreda_name: str) -> dict:
    """Get sanitation office information for a given woreda."""
    pass


def create_sanitation_ticket(
    woreda: str,
    issue_description: str,
    user_contact: str | None = None,
) -> dict:
    """Create a new sanitation issue ticket."""
    pass


def get_sanitation_ticket_status(ticket_number: str) -> dict:
    """Get the status of a sanitation ticket."""
    pass
