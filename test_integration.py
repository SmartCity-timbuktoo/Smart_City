"""
Addis-Sync System Integration Test
Tests agent loading, database connections, and environment configuration.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("ADDIS-SYNC SYSTEM INTEGRATION TEST")
print("=" * 60)

# Test 1: Environment Variables
print("\n[1/4] Testing Environment Configuration...")
api_key = os.getenv('GOOGLE_API_KEY')
if api_key:
    print(f"  ✓ GOOGLE_API_KEY is set ({len(api_key)} characters)")
else:
    print("  ✗ GOOGLE_API_KEY is NOT set")
    sys.exit(1)

# Test 2: Agent Imports
print("\n[2/4] Testing Agent Imports...")
try:
    from smart_city_agent.agent import customer_service_agent
    print(f"  ✓ Customer Service Agent loaded")
    print(f"    - Model: {customer_service_agent.model}")
    print(f"    - Sub-agents: {len(customer_service_agent.sub_agents)}")
    
    for agent in customer_service_agent.sub_agents:
        print(f"      • {agent.name} ({agent.model})")
except Exception as e:
    print(f"  ✗ Failed to load agents: {e}")
    sys.exit(1)

# Test 3: Database Configuration
print("\n[3/4] Testing Database Configuration...")
try:
    from smart_city_agent.mcp_server.db import (
        EMERGENCY_DB, POWER_DB, SANITATION_DB, 
        INFRASTRUCTURE_DB, UTILITY_DB, get_conn
    )
    db_configs = [
        ("Emergency DB", EMERGENCY_DB),
        ("Power DB", POWER_DB),
        ("Sanitation DB", SANITATION_DB),
        ("Infrastructure DB", INFRASTRUCTURE_DB),
        ("Utility DB", UTILITY_DB),
    ]
    
    for name, config in db_configs:
        print(f"  • {name}: {config['dbname']} @ {config['host']}:{config['port']}")
        
except Exception as e:
    print(f"  ✗ Failed to load database configs: {e}")
    sys.exit(1)

# Test 4: Database Connections
print("\n[4/4] Testing Database Connections...")
connection_results = []
for name, config in db_configs:
    try:
        conn = get_conn(config)
        conn.close()
        print(f"  ✓ {name} connection successful")
        connection_results.append((name, True))
    except Exception as e:
        print(f"  ✗ {name} connection failed: {e}")
        connection_results.append((name, False))

# Summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)

successful_connections = sum(1 for _, result in connection_results if result)
total_connections = len(connection_results)

print(f"\nDatabase Connections: {successful_connections}/{total_connections} successful")

if successful_connections == total_connections:
    print("\n✓ ALL TESTS PASSED - System is ready!")
    sys.exit(0)
else:
    print("\n⚠ SOME TESTS FAILED - Check database setup")
    print("\nFailed connections:")
    for name, result in connection_results:
        if not result:
            print(f"  - {name}")
    
    print("\nNext steps:")
    print("  1. Ensure PostgreSQL is running")
    print("  2. Create the databases using schema files:")
    print("     psql -U postgres -c 'CREATE DATABASE emergency_db;'")
    print("     psql -U postgres -d emergency_db -f smart_city_agent/database/emergency_db/schema.sql")
    print("     psql -U postgres -d emergency_db -f smart_city_agent/database/emergency_db/data.sql")
    print("  3. Repeat for other databases")
    sys.exit(1)
