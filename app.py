import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
from core.orchestrator import Orchestrator
import graphviz
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="SC-Control | Autonomous Supply Chain",
    layout="wide",
    page_icon="🏙️",
    initial_sidebar_state="expanded"
)

# --- CUSTOM THEME (CSS) ---
st.markdown("""
<style>
    /* Global Theme - "Executive Dark" / Professional */
    /* .stApp controlled by config.toml now */
    
    /* Metrics Cards */
    div[data-testid="metric-container"] {
        background-color: #1a1e26; /* Dark slate */
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #4e8cff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Headers -> Inherit from theme but ensure weights */
    h1, h2, h3 {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-weight: 600;
    }
    h1 { font-size: 2.2rem; margin-bottom: 0px; }
    
    /* Sidebar -> Inherit */
    
    /* Buttons handled by theme mostly, but keeping custom hover */
    .stButton>button {
        border-radius: 6px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col_head_1, col_head_2 = st.columns([1, 4])
with col_head_1:
    st.markdown("<div style='font-size: 3rem;'>🏙️</div>", unsafe_allow_html=True)
with col_head_2:
    st.markdown("# Autonomous Supply Chain Control Tower")
    st.markdown("*AI-Driven Demand Planning & Inventory Optimization*")

st.divider()

# --- DATA LOADER ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/inventory_data_real.csv")
    except FileNotFoundError:
        st.error("❌ Data source unavailable. Check connection.")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.subheader("📍 Control Panel")
    selected_sku = st.selectbox(
        "Select Product SKU", 
        df["SKU_ID"].tolist(),
        format_func=lambda x: f"{x} - {df[df['SKU_ID']==x]['Product_Name'].values[0]}"
    )
    
    # State Management Logic
    if "active_sku" not in st.session_state or st.session_state["active_sku"] != selected_sku:
        st.session_state["active_sku"] = selected_sku
        st.session_state["analysis_result"] = None # Reset analysis on valid SKU switch

    st.markdown("---")
    st.markdown("### 🛠️ Simulation Params")
    sim_season = st.selectbox("Simulated Season", ["Winter", "Summer", "All Year"], index=0)
    
    st.info(f"System Time: {datetime.now().strftime('%H:%M')} EST")
    st.caption("v2.1.0-Production | OpenAI Agents")

# --- KPI DASHBOARD ---
sku_data = df[df["SKU_ID"] == selected_sku].iloc[0]

# Metrics Layout
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Current Stock", f"{sku_data['Current_Stock']:,}", help="Physical inventory on hand")
with col2:
    fc_delta = int(sku_data['Forecast'] - sku_data['Sales_Trend_Last_30_Days'])
    st.metric("30-Day Forecast", f"{sku_data['Forecast']:,}", delta=fc_delta, delta_color="inverse")
with col3:
    st.metric("Sales Trend (30d)", f"{sku_data['Sales_Trend_Last_30_Days']:,}", "Velocity")
with col4:
    st.metric("On Order", f"{sku_data.get('On_Order', 0):,}", help="Inbound stock")
with col5:
    coverage = round(sku_data['Current_Stock'] / sku_data['Forecast'], 2) if sku_data['Forecast'] else 0
    st.metric("Weeks of Supply", f"{coverage * 4} wks", delta="Low Risk" if 0.8 < coverage < 1.5 else "High Risk", delta_color="normal" if 0.8 < coverage < 1.5 else "inverse")

# --- MAIN CHARTS & AGENT INTERFACE ---
col_main, col_logs = st.columns([1.8, 1.2])

with col_main:
    st.subheader("📈 Supply & Demand Intelligence")
    
    # CHART: Plotly Forecast vs Actuals (Simulated history for demo)
    # In a real app, we'd pull historicals. Here we generate a simple line chart.
    import numpy as np
    
    # Simulate past 6 months data for the chart
    months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    base_sales = sku_data['Sales_Trend_Last_30_Days']
    # Add random variance
    history = [base_sales * (0.8 + 0.1 * i + np.random.normal(0, 0.05)) for i in range(6)]
    forecast_line = [None] * 5 + [sku_data['Forecast']] # Forecast point
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=history, mode='lines+markers', name='Sales History', line=dict(color='#4e8cff', width=3)))
    fig.add_trace(go.Scatter(x=["Dec", "Jan Forecast"], y=[history[-1], sku_data['Forecast']], mode='lines+markers', name='Forecast', line=dict(color='#00cc96', dash='dot')))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fafafa'),
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Timeline",
        yaxis_title="Units",
        height=300,
        showlegend=True
    )
    st.plotly_chart(fig, width="stretch")

    st.markdown("### 🌐 Agent Network Status")
    
    # Reusing the Graphviz visual but cleaner
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR', bgcolor='transparent')
    graph.attr('node', shape='box', style='rounded,filled', fontcolor='white', fillcolor='#262730', color='#4e8cff')
    graph.attr('edge', color='#888888')
    
    # Highlight active path based on logs? For now static map.
    nodes = ["Monitoring", "Forecast", "RootCause", "Inventory", "Procurement"]
    for n in nodes:
        graph.node(n)
        
    graph.edge("Monitoring", "Forecast")
    graph.edge("Forecast", "Inventory", label="Deficit?")
    graph.edge("Inventory", "RootCause", label="Risk?")
    graph.edge("Inventory", "Procurement", label="Shortfall")
    
    st.graphviz_chart(graph, width="stretch")

with col_logs:
    st.subheader("📡 Autonomous Resolution")
    
    # Action Container
    action_box = st.container()
    
    with action_box:
        st.markdown(f"""
        **Context**: SKU {selected_sku} ({sku_data['Product_Name']})  
        **Issue**: {'⚠️ Stock Risk Deteceted' if coverage < 0.8 else '✅ Healthy'}
        """)
        
        # Fixing the button as well
        if st.button("RUN DIAGNOSTINC & RESOLVE", type="primary", use_container_width=True):
            st.session_state["analysis_result"] = None # Clear old
            
            # Streaming UI
            placeholder = st.empty()
            with placeholder.container():
                st.info("🔄 Initializing Multi-Agent System...")
            
            orchestrator = Orchestrator()
            
            # Add simulation params to data
            run_data = sku_data.to_dict()
            run_data["Season"] = sim_season
            
            with st.spinner("🤖 Agents working..."):
                result = orchestrator.run(run_data)
                st.session_state["analysis_result"] = result
            
            placeholder.empty()

    if st.session_state["analysis_result"]:
        st.divider()
        st.markdown("#### 📧 Email Report")
        email_addr = st.text_input("Recipient Email", placeholder="manager@example.com")
        if st.button("Send Summary", type="secondary", use_container_width=True):
            if not email_addr:
                st.error("Please enter an email address.")
            else:
                from agents.email_agent import email_agent
                
                # Context for Email Agent
                results = st.session_state["analysis_result"]
                email_ctx = {
                    "summary": results.get("final_summary", ""),
                    "logs": results.get("logs", []),
                    "user_email": email_addr
                }
                
                with st.spinner("Generating and Sending Email..."):
                    orch = Orchestrator()
                    email_status = orch.run_agent_ad_hoc(email_agent, email_ctx)
                
                if "Error" in email_status or "Failed" in email_status:
                    st.error(email_status)
                else:
                    st.success(email_status)

    st.divider()
    
    # Live Feed / Results
    if st.session_state["analysis_result"]:
        res = st.session_state["analysis_result"]
        
        # --- PROPOSED ACTIONS & APPROVAL ---
        # identify pending actions
        actions = {}
        if res.get("new_forecast"): actions["Update Forecast"] = f"New Value: {res['new_forecast']}"
        if res.get("po_qty"): actions["Create PO"] = f"Qty: {res['po_qty']} units"
        if res.get("transfer_qty"): actions["Transfer Stock"] = f"Qty: {res['transfer_qty']} units"
        
        # Only show approval if there are actions AND they haven't been processed yet
        if actions:
            st.info("✋ **Human Approval Required**")
            
            # Show diff
            act_df = pd.DataFrame(list(actions.items()), columns=["Action", "Details"])
            st.table(act_df)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Approve & Execute Changes", use_container_width=True):
                    # EXECUTE
                    orch = Orchestrator()
                    status_msg = orch.persist_changes(sku_data["SKU_ID"], res)
                    st.success(status_msg)
                    time.sleep(1) 
                    st.rerun()
            with c2:
                if st.button("❌ Reject Proposed Actions", use_container_width=True):
                    st.warning("Actions Rejected. No changes made.")
                    # Optionally clear state or just leave it
                    
        # --- STATUS BAR ---
        status = res.get("status", "Healthy")
        risk_type = res.get("risk_type", "None")
        
        if status == "Risk":
            if "Stock-out" in risk_type:
               st.error(f"🚨 **CRITICAL STATUS: {risk_type.upper()}** - IMMEDIATE ACTION REQUIRED")
            else:
               st.warning(f"⚠️ **STATUS: {risk_type.upper()}** - MONITORING")
        else:
            st.success("✅ **STATUS: OPTIMAL** - SUPPLY CHAIN IS HEALTHY")
        # ------------------
        
        with st.expander("🔍 Executive Summary", expanded=True):
            st.markdown(res.get("final_summary", "No summary available."))
            
        # Action Log Timeline
        st.subheader("📜 Execution Trace")
        logs = res.get("logs", [])
        
        for log in logs:
            if "Tool" in log:
                 st.markdown(f"🛠️ `{log}`")
            elif "Error" in log:
                st.error(log)
            elif "[" in log:
                # Format: [AgentName] Message
                parts = log.split("]", 1)
                agent = parts[0].replace("[", "")
                msg = parts[1]
                st.markdown(f"**{agent}**: {msg}")
            else:
                st.info(log)
                
    else:
        st.info("👆 Click 'Run' to start the autonomous agents.")
