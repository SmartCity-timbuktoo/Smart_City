from ..local_runner import MCPServer
from .db import get_conn, EMERGENCY_DB
import uuid

server = MCPServer(name="emergency_mcp_server")


@server.tool()
def find_closest_emergency_office(woreda_name: str) -> dict:
    """
    Fetch emergency office contact info by woreda.
    """
    sql = """
        SELECT name, phone, email, address, 
               ST_X(location::geometry) as longitude,
               ST_Y(location::geometry) as latitude
        FROM offices
        WHERE woreda = %s
        LIMIT 1;
    """
    
    with get_conn(EMERGENCY_DB) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (woreda_name,))
            row = cur.fetchone()
    
    if not row:
        return {"error": f"No emergency office found for woreda: {woreda_name}"}
    
    return dict(row)


@server.tool()
def create_emergency_ticket(
    woreda: str,
    emergency_type: str,
    issue_description: str,
    user_contact: str | None = None,
    location_details: str | None = None,
) -> dict:
    """
    Create a new emergency ticket.
    """
    ticket_number = f"EMER-{uuid.uuid4().hex[:8].upper()}"
    
    sql = """
        INSERT INTO tickets
        (ticket_number, woreda, emergency_type, issue_description, user_contact, location_details, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING ticket_number, status, created_at;
    """
    
    with get_conn(EMERGENCY_DB) as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (ticket_number, woreda, emergency_type, issue_description, user_contact, location_details, "RECEIVED")
            )
            result = cur.fetchone()
            conn.commit()
    
    return dict(result)


@server.tool()
def get_emergency_ticket_status(ticket_number: str) -> dict:
    """
    Fetch current status of an emergency ticket.
    """
    sql = """
        SELECT ticket_number, woreda, emergency_type, status, created_at, updated_at
        FROM tickets
        WHERE ticket_number = %s;
    """
    
    with get_conn(EMERGENCY_DB) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (ticket_number,))
            row = cur.fetchone()
    
    if not row:
        return {"error": "Emergency ticket not found"}
    
    return dict(row)


if __name__ == "__main__":
    server.run(port=3333)
