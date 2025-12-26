"""
Infrastructure Agent tool stubs.
Actual implementation is in the MCP server.
"""

def get_infrastructure_office_by_woreda(woreda_name: str) -> dict:
    """Get infrastructure office information for a given woreda."""
    pass


def create_infrastructure_ticket(
    woreda: str,
    issue_description: str,
    user_contact: str | None = None,
) -> dict:
    """Create a new infrastructure issue ticket."""
    pass


def get_infrastructure_ticket_status(ticket_number: str) -> dict:
    """Get the status of an infrastructure ticket."""
    pass
