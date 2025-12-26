from ..local_runner import MCPServer
from .db import get_conn, UTILITY_DB, UTILITY_LEDGER_DB
import uuid
from datetime import datetime

server = MCPServer(name="utility_mcp_server")


@server.tool()
def create_utility_ticket(
    woreda: str,
    issue_description: str,
    user_contact: str | None = None,
) -> dict:
    """
    Create a new utility ticket and store it in utility_ledger_db.
    """

    ticket_number = f"UTIL-{uuid.uuid4().hex[:8].upper()}"

    sql = """
        INSERT INTO utility_tickets
        (ticket_number, woreda, issue_description, user_contact, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING ticket_number;
    """

    with get_conn(UTILITY_LEDGER_DB) as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (ticket_number, woreda, issue_description, user_contact, "RECEIVED")
            )
            conn.commit()

    return {
        "ticket_number": ticket_number,
        "status": "RECEIVED"
    }


@server.tool()
def get_utility_office_by_woreda(woreda_name: str) -> dict:
    """
    Fetch utility office contact info by woreda.
    """
    sql = """
        SELECT name, phone, email, location
        FROM offices
        WHERE woreda = %s
        LIMIT 1;
    """

    with get_conn(UTILITY_DB) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (woreda_name,))
            row = cur.fetchone()

    if not row:
        return {"error": "No office found for this woreda"}

    return dict(row)


@server.tool()
def register_utility_interaction(
    woreda: str,
    issue_description: str,
    user_contact: str | None = None,
) -> dict:
    """
    Log user interaction in utility_ledger_db.
    """
    sql = """
        INSERT INTO utility_interactions (woreda, issue_description, user_contact)
        VALUES (%s, %s, %s)
        RETURNING id;
    """

    with get_conn(UTILITY_LEDGER_DB) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (woreda, issue_description, user_contact))
            interaction_id = cur.fetchone()["id"]
            conn.commit()

    return {
        "status": "SUCCESS",
        "interaction_id": interaction_id
    }


@server.tool()
def get_ticket_status(ticket_number: str) -> dict:
    """
    Fetch current status of a utility ticket.
    """

    sql = """
        SELECT ticket_number, woreda, status, created_at, updated_at
        FROM utility_tickets
        WHERE ticket_number = %s;
    """

    with get_conn(UTILITY_LEDGER_DB) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (ticket_number,))
            row = cur.fetchone()

    if not row:
        return {"error": "Ticket not found"}

    return dict(row)


if __name__ == "__main__":
    server.run(port=3333)
