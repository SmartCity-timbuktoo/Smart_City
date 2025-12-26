
import streamlit as st
import pandas as pd
import psycopg2
from smart_city_agent.mcp_server.db import (
    get_conn,
    EMERGENCY_DB,
    POWER_DB,
    SANITATION_DB,
    INFRASTRUCTURE_DB,
    UTILITY_DB
)

# Map Agent Names to DB Configs
AGENT_DBS = {
    "Emergency": EMERGENCY_DB,
    "Power": POWER_DB,
    "Sanitation": SANITATION_DB,
    "Infrastructure": INFRASTRUCTURE_DB,
    "Utility": UTILITY_DB
}

st.set_page_config(page_title="Addis-Sync Admin", layout="wide")

st.title("Addis-Sync: Operations Dashboard")

# --- Role Selection ---
role = st.sidebar.selectbox("Select Role", ["Admin", "Worker"])

def fetch_all_tickets():
    """Fetch tickets from ALL agent databases."""
    all_data = []
    
    for agent_name, db_config in AGENT_DBS.items():
        try:
            with get_conn(db_config) as conn:
                with conn.cursor() as cur:
                    # Check if tickets table exists first (handling empty setup)
                    cur.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = 'tickets'
                        );
                    """)
                    if cur.fetchone()['exists']:
                        cur.execute("SELECT * FROM tickets")
                        rows = cur.fetchall()
                        for row in rows:
                            # Convert RealDictRow to dict and add Agent tag
                            r = dict(row)
                            r['agent'] = agent_name
                            all_data.append(r)
        except Exception as e:
            st.error(f"Error connecting to {agent_name} DB: {e}")
            
    return pd.DataFrame(all_data)

def update_ticket_status(agent_name, ticket_number, new_status):
    """Update ticket status in valid DB."""
    db_config = AGENT_DBS.get(agent_name)
    if not db_config:
        return False
        
    try:
        with get_conn(db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE tickets SET status = %s, updated_at = NOW() WHERE ticket_number = %s",
                    (new_status, ticket_number)
                )
                conn.commit()
        return True
    except Exception as e:
        st.error(f"Update failed: {e}")
        return False

# --- Admin View ---
if role == "Admin":
    st.header("Admin Overview: All Reports")
    st.info("Read-Only Access")
    
    if st.button("Refresh Data"):
        st.rerun()
        
    df = fetch_all_tickets()
    
    if not df.empty:
        # Reorder columns for readability
        cols = ['agent', 'ticket_number', 'status', 'woreda', 'created_at', 'issue_description']
        # Handle missing columns gracefully
        available_cols = [c for c in cols if c in df.columns]
        other_cols = [c for c in df.columns if c not in cols]
        
        st.dataframe(
            df[available_cols + other_cols],
            use_container_width=True,
            hide_index=True
        )
        
        # Stats
        st.subheader("Statistics")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### By Agent")
            st.bar_chart(df['agent'].value_counts())
        with c2:
            st.markdown("### By Status")
            st.warning("Status Distribution")
            status_counts = df['status'].value_counts()
            st.write(status_counts)
            
    else:
        st.warning("No tickets found in any database.")

# --- Worker View ---
else:
    st.header("Worker Portal: Task Management")
    
    selected_agent = st.sidebar.selectbox("Select Your Department", list(AGENT_DBS.keys()))
    
    # Fetch data for single agent
    db_config = AGENT_DBS[selected_agent]
    current_data = []
    
    try:
        with get_conn(db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM tickets ORDER BY created_at DESC")
                rows = cur.fetchall()
                current_data = [dict(r) for r in rows]
    except Exception as e:
        st.error(f"Connection error: {e}")
        
    if current_data:
        df = pd.DataFrame(current_data)
        
        # Editable Dataframe
        st.subheader(f"{selected_agent} Tickets")
        
        # Allow editing 'status'
        edited_df = st.data_editor(
            df,
            column_config={
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    help="Update ticket status",
                    width="medium",
                    options=[
                        "RECEIVED",
                        "IN_PROGRESS",
                        "RESOLVED",
                        "CLOSED",
                        "CANCELLED"
                    ],
                    required=True,
                ),
                "ticket_number": st.column_config.TextColumn("Ticket #", disabled=True),
                "created_at": st.column_config.DatetimeColumn("Created", disabled=True),
                "issue_description": st.column_config.TextColumn("Issue", disabled=True),
            },
            hide_index=True,
            use_container_width=True,
            key="ticket_editor"
        )
        
        # Detect Changes
        # Streamlit data_editor returns the FULL edited dataframe state?
        # Yes. We need to compare or just button "Save Changes"
        
        if st.button("Save Status Updates"):
            # Iterate and update
            # Optimization: In a real app, track changes via session state or editor output diff
            # Here: simple brute force check against DB? Or just update all? 
            # Better: Loop rows and update.
            
            success_count = 0
            for index, row in edited_df.iterrows():
                # We update all rows to match editor state (inefficient but safe for MVP)
                # But we should check if it changed? 
                # Let's just update.
                t_num = row['ticket_number']
                new_status = row['status']
                
                # Find original
                original = df[df['ticket_number'] == t_num].iloc[0]
                if original['status'] != new_status:
                    if update_ticket_status(selected_agent, t_num, new_status):
                        success_count += 1
            
            if success_count > 0:
                st.success(f"Updated {success_count} tickets successfully!")
                st.rerun()
            else:
                st.info("No changes detected.")
                
    else:
        st.info(f"No tickets found for {selected_agent}.")

