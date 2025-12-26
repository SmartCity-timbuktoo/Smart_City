from ..local_runner import MCPServer
from .db import get_conn, INFRASTRUCTURE_DB
import uuid

server = MCPServer(name="infrastructure_mcp_server")


@server.tool()
def get_infrastructure_office_by_woreda(woreda_name: str) -> dict:
    """
    Fetch infrastructure office contact info by woreda.
    """
    sql = """
        SELECT name, phone, email, address,
               ST_X(location::geometry) as longitude,
               ST_Y(location::geometry) as latitude
        FROM offices
        WHERE woreda = %s
        LIMIT 1;
    """
    
    with get_conn(INFRASTRUCTURE_DB) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (woreda_name,))
            row = cur.fetchone()
    
    if not row:
        return {"error": f"No infrastructure office found for woreda: {woreda_name}"}
    
    return dict(row)


@server.tool()
def create_infrastructure_ticket(
    woreda: str,
    issue_description: str,
    user_contact: str | None = None,
) -> dict:
    """
    Create a new infrastructure issue ticket.
    """
    ticket_number = f"INFR-{uuid.uuid4().hex[:8].upper()}"
    
    sql = """
        INSERT INTO tickets
        (ticket_number, woreda, issue_description, user_contact, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING ticket_number, status, created_at;
    """
    
    with get_conn(INFRASTRUCTURE_DB) as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (ticket_number, woreda, issue_description, user_contact, "RECEIVED")
            )
            result = cur.fetchone()
            conn.commit()
    
    return dict(result)


@server.tool()
def get_infrastructure_ticket_status(ticket_number: str) -> dict:
    """
    Fetch current status of an infrastructure ticket.
    """
    sql = """
        SELECT ticket_number, woreda, status, created_at, updated_at
        FROM tickets
        WHERE ticket_number = %s;
    """
    
    with get_conn(INFRASTRUCTURE_DB) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (ticket_number,))
            row = cur.fetchone()
    
    if not row:
        return {"error": "Infrastructure ticket not found"}
    
    return dict(row)


if __name__ == "__main__":
    server.run(port=3336)
