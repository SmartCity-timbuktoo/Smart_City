import psycopg2
from psycopg2.extras import RealDictCursor

# Emergency Agent Databases
EMERGENCY_DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "emergency_db",
    "user": "postgres",
    "password": "postgrespass",
}

EMERGENCY_LEDGER_DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "emergency_ledger_db",
    "user": "postgres",
    "password": "postgrespass",
}

# Power Agent Databases
POWER_DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "power_db",
    "user": "postgres",
    "password": "postgrespass",
}

POWER_LEDGER_DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "power_ledger_db",
    "user": "postgres",
    "password": "postgrespass",
}

# Sanitation Agent Databases
SANITATION_DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "sanitation_db",
    "user": "postgres",
    "password": "postgrespass",
}

SANITATION_LEDGER_DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "sanitation_ledger_db",
    "user": "postgres",
    "password": "postgrespass",
}

# Infrastructure Agent Databases
INFRASTRUCTURE_DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "infrastructure_db",
    "user": "postgres",
    "password": "postgrespass",
}

INFRASTRUCTURE_LEDGER_DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "infrastructure_ledger_db",
    "user": "postgres",
    "password": "postgrespass",
}

# Utility Agent Databases
UTILITY_DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "utility_db",
    "user": "postgres",
    "password": "postgrespass",
}

UTILITY_LEDGER_DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "utility_ledger_db",
    "user": "postgres",
    "password": "postgrespass",
}

def get_conn(cfg):
    """Create database connection with RealDictCursor for dict results"""
    return psycopg2.connect(**cfg, cursor_factory=RealDictCursor)
