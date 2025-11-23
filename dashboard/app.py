import streamlit as st
import json
import pandas as pd
import time
import os

LOG_FILE = "audit_log.json"

st.set_page_config(page_title="MetaGuardian Dashboard", layout="wide")

st.title("🛡️ MetaGuardian: AI Governance & Compliance Orchestrator")
st.markdown("### Addressing the meta-challenge of governing AI systems themselves")

def load_data():
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# Auto-refresh mechanism
placeholder = st.empty()

data = load_data()

with placeholder.container():
    # Metrics
    total_decisions = len(data)
    high_risk = sum(1 for d in data if not d["compliance_check"]["compliant"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Decisions Monitored", total_decisions)
    col2.metric("Policy Violations Detected", high_risk, delta_color="inverse")
    col3.metric("Active Agents", 3)

    # Recent Activity Feed
    st.subheader("Recent Agent Decisions")
    
    if data:
        # Reverse to show newest first
        recent_data = data[::-1]
        
        for item in recent_data[:5]:
            decision = item["original_decision"]
            compliance = item["compliance_check"]
            
            with st.expander(f"{item['timestamp']} - {decision.get('agent_name', 'Unknown')} ({decision.get('decision', 'N/A')})"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Decision Details:**")
                    st.json(decision)
                with c2:
                    st.markdown("**Compliance Check:**")
                    if compliance["compliant"]:
                        st.success("✅ Compliant")
                    else:
                        st.error(f"❌ Violation: {compliance['violation_type']}")
                        st.write(compliance["message"])

    # Data Table
    st.subheader("Audit Log")
    if data:
        df_data = []
        for i, item in enumerate(data):
            row = {
                "ID": i + 1,
                "Time": item["timestamp"],
                "Agent": item["original_decision"]["agent_name"],
                "Decision": item["original_decision"]["decision"],
                "Compliant": item["compliance_check"]["compliant"],
                "Violation": item["compliance_check"]["violation_type"]
            }
            df_data.append(row)
        st.dataframe(pd.DataFrame(df_data))

    # Human-in-the-Loop Review Queue
    st.markdown("---")
    c_rev, c_health = st.columns([2, 1])
    
    with c_rev:
        st.subheader("👮 Human Review Queue")
        pending_reviews = [d for d in data if not d["compliance_check"]["compliant"]]
        
        if not pending_reviews:
            st.info("No high-risk decisions pending review.")
        else:
            for i, item in enumerate(pending_reviews):
                with st.container():
                    st.warning(f"Violation: {item['compliance_check']['violation_type']}")
                    st.write(f"Agent: {item['original_decision']['agent_name']}")
                    st.write(f"Details: {item['compliance_check']['message']}")
                    
                    c1, c2 = st.columns(2)
                    if c1.button(f"Approve", key=f"app_{i}"):
                        import requests
                        try:
                            requests.post("http://localhost:5000/resolve_decision", json={"audit_id": i, "action": "APPROVE"})
                            st.success("Approved!")
                            time.sleep(0.5)
                            st.rerun()
                        except:
                            st.error("Connection Error")
                            
                    if c2.button(f"Reject", key=f"rej_{i}"):
                         import requests
                         try:
                            requests.post("http://localhost:5000/resolve_decision", json={"audit_id": i, "action": "REJECT"})
                            st.error("Rejected!")
                            time.sleep(0.5)
                            st.rerun()
                         except:
                            st.error("Connection Error")
                    st.markdown("---")

    with c_health:
        st.subheader("🏥 System Health")
        # Fetch status from orchestrator
        import requests
        try:
            status = requests.get("http://localhost:5000/system_status").json()
            blocked = status.get("blocked_agents", [])
            counts = status.get("violation_counts", {})
            
            st.write("**Violation Counts:**")
            st.json(counts)
            
            st.write("**Blocked Agents:**")
            if not blocked:
                st.success("All agents active.")
            else:
                for agent in blocked:
                    st.error(f"⛔ {agent}")
                    if st.button(f"Unblock {agent}"):
                        requests.post("http://localhost:5000/unblock_agent", json={"agent_name": agent})
                        st.rerun()
        except:
            st.warning("Orchestrator Offline")

    # Natural Language Governance
    st.markdown("---")
    st.subheader("💬 Ask Meta-Guardian")
    query = st.text_input("Ask a question about compliance (e.g., 'Show me high risk loans', 'Show blocked agents')")
    
    if query:
        query = query.lower()
        results = []
        
        if "high risk" in query or "violation" in query:
            results = [d for d in data if not d["compliance_check"]["compliant"]]
            st.write(f"Found {len(results)} violations:")
        elif "loan" in query:
            results = [d for d in data if d["original_decision"]["agent_name"] == "LoanApprovalBot"]
            st.write(f"Found {len(results)} loan decisions:")
        elif "hiring" in query:
            results = [d for d in data if d["original_decision"]["agent_name"] == "HiringBot"]
            st.write(f"Found {len(results)} hiring decisions:")
        elif "blocked" in query:
            st.info("Check the System Health panel above for blocked agents.")
        else:
            st.write("I didn't understand that query. Try asking about 'high risk', 'loans', or 'hiring'.")
            
        if results:
            st.dataframe(pd.DataFrame([r["original_decision"] for r in results]))

# Auto-Refresh Logic
if st.sidebar.button("Refresh Now"):
    st.rerun()

time.sleep(15)
st.rerun()
