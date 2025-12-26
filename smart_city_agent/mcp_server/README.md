# Addis-Sync MCP Servers

This directory contains Model Context Protocol (MCP) servers for all domain agents.

## MCP Servers

Each server runs on a different port and provides tools for its respective domain:

| Server | Port | Tools |
|--------|------|-------|
| Emergency | 3333 | `find_closest_emergency_office`, `create_emergency_ticket`, `get_emergency_ticket_status` |
| Power | 3334 | `get_power_office_by_woreda`, `create_power_ticket`, `get_power_ticket_status` |
| Sanitation | 3335 | `get_sanitation_office_by_woreda`, `create_sanitation_ticket`, `get_sanitation_ticket_status` |
| Infrastructure | 3336 | `get_infrastructure_office_by_woreda`, `create_infrastructure_ticket`, `get_infrastructure_ticket_status` |
| Utility | 3337 | `get_utility_office_by_woreda`, `create_utility_ticket`, `get_ticket_status` |

## Usage

### Running Individual Servers

```bash
# Emergency server
python emergency_server.py

# Power server
python power_server.py

# Sanitation server  
python sanitation_server.py

# Infrastructure server
python infrastructure_server.py

# Utility server
python utility_server.py
```

### Running All Servers

Create a script to run all servers in parallel or use a process manager like `supervisord`.

## Database Configuration

Update `db.py` with your PostgreSQL credentials:

```python
EMERGENCY_DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "emergency_db",
    "user": "postgres",
    "password": "YOUR_PASSWORD",
}
```

Replace `YOUR_PASSWORD` with your actual PostgreSQL password.

## Tool Descriptions

### Office Lookup Tools
- `get_*_office_by_woreda(woreda_name: str)` - Returns office details for a given woreda

### Ticket Creation Tools
- `create_*_ticket(woreda, issue_description, user_contact?)` - Creates a new ticket

### Status Checking Tools
- `get_*_ticket_status(ticket_number: str)` - Returns ticket status and details
