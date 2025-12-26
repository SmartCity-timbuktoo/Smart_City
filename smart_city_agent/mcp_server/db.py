import os
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse

# Cloud Connection String (Populated from Env)
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_config(schema_name, local_dbname):
    """
    Returns DB config. 
    If DATABASE_URL is present, returns cloud config with 'schema'.
    Else, returns local config.
    """
    if DATABASE_URL:
        # We don't parse it here, psycopg2 handles it. We just flag the schema.
        return {
            "type": "cloud",
            "schema": schema_name
        }
    else:
        # Local Fallback
        return {
            "type": "local",
            "host": "localhost",
            "port": 5432,
            "dbname": local_dbname,
            "user": "postgres",
            "password": "postgrespass",
        }

# Emergency Agent Databases
EMERGENCY_DB = get_db_config("emergency", "emergency_db")
EMERGENCY_LEDGER_DB = get_db_config("emergency", "emergency_ledger_db")

# Power Agent Databases
POWER_DB = get_db_config("power", "power_db")
POWER_LEDGER_DB = get_db_config("power", "power_ledger_db")

# Sanitation Agent Databases
SANITATION_DB = get_db_config("sanitation", "sanitation_db")
SANITATION_LEDGER_DB = get_db_config("sanitation", "sanitation_ledger_db")

# Infrastructure Agent Databases
INFRASTRUCTURE_DB = get_db_config("infrastructure", "infrastructure_db")
INFRASTRUCTURE_LEDGER_DB = get_db_config("infrastructure", "infrastructure_ledger_db")

# Utility Agent Databases
UTILITY_DB = get_db_config("utility", "utility_db")
UTILITY_LEDGER_DB = get_db_config("utility", "utility_ledger_db")


def get_conn(cfg):
    """Create database connection with RealDictCursor for dict results"""
    
    if cfg["type"] == "cloud":
        # Cloud Connection (Supabase/Neon)
        # We inject the 'search_path' to route queries to the correct agent schema
        return psycopg2.connect(
            DATABASE_URL, 
            cursor_factory=RealDictCursor,
            options=f"-c search_path={cfg['schema']}"
        )
    else:
        # Local Connection
        # Use provided credentials, ignore 'type' and 'schema' keys
        db_args = {k: v for k, v in cfg.items() if k not in ["type", "schema"]}
        return psycopg2.connect(**db_args, cursor_factory=RealDictCursor)

