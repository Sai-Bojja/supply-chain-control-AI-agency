import streamlit as st
import pandas as pd
import time
import graphviz
from core.orchestrator import Orchestrator

st.set_page_config(page_title="Supply Chain Control Tower", layout="wide", page_icon="🏢")

# Custom CSS for "Production Grade" look
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🏢 Autonomous Supply Chain Control Tower</h1>", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/inventory_data_real.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file not found. Please ensure 'data/inventory_data_real.csv' exists.")
    st.stop()

# Initialize Session State
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None
if "active_sku" not in st.session_state:
    st.session_state["active_sku"] = None

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png", width=100)
    st.header("System Controls")
    selected_sku = st.selectbox("Select SKU to Monitor", df["SKU_ID"].tolist())
    
    # Reset state if SKU changes
    if selected_sku != st.session_state["active_sku"]:
        st.session_state["analysis_result"] = None
        st.session_state["active_sku"] = selected_sku
        
    st.markdown("---")
    st.markdown("**Active Agents:**")
    st.markdown("✅ Monitoring")
    st.markdown("✅ Forecast")
    st.markdown("✅ Root Cause (Web Enabled)")
    st.markdown("✅ Inventory")
    st.markdown("✅ Procurement")
    st.markdown("✅ Communication")

# Dashboard Metrics
col1, col2, col3, col4, col5 = st.columns(5)
selected_data = df[df["SKU_ID"] == selected_sku].iloc[0]

# Product Header
st.markdown(f"## 📦 {selected_data['Product_Name']}")
st.markdown(f"**Category:** {selected_data['Category']} | **Location:** {selected_data['Location']} | **Season:** {selected_data.get('Season', 'All Year')}")
st.markdown("---")

with col1:
    st.metric("Current Stock", f"{selected_data['Current_Stock']} units")
with col2:
    st.metric("Forecast (30 Days)", f"{selected_data['Forecast']} units")
with col3:
    st.metric("On Order", f"{selected_data.get('On_Order', 0)} units")
with col4:
    st.metric("Past 30 Days Sales", f"{selected_data['Sales_Trend_Last_30_Days']} units", 
             delta=int(selected_data['Sales_Trend_Last_30_Days'] - selected_data['Forecast']))
with col5:
    st.metric("Lead Time", f"{selected_data['Supplier_Lead_Time']} days")

st.markdown("---")

# Main Execution Area
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📡 Live Agent Network")
    graph_placeholder = st.empty()
    
    def render_graph(active_agent=None):
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR', size='8,5')
        dot.attr('node', shape='box', style='filled', color='lightgrey')
        
        agents = ["Monitoring", "Forecast", "Root Cause", "Inventory", "Procurement", "Communication"]
        
        for agent in agents:
            if agent == active_agent:
                dot.node(agent, style='filled', fillcolor='#ff9999', color='red')
            else:
                dot.node(agent)
                
        dot.edge("Monitoring", "Forecast")
        dot.edge("Forecast", "Root Cause")
        dot.edge("Root Cause", "Inventory")
        dot.edge("Inventory", "Procurement")
        dot.edge("Procurement", "Communication")
        
        graph_placeholder.graphviz_chart(dot)

    # Render initial graph
    render_graph()

    st.subheader("📝 Agent Activity Log")
    log_container = st.container()
    
    # If we have a result in state, render it
    if st.session_state["analysis_result"]:
        result = st.session_state["analysis_result"]
        for log in result["logs"]:
            with log_container:
                if "ALERT" in log:
                    st.error(log)
                elif "Updating" in log or "Action" in log:
                    st.warning(log)
                else:
                    st.info(log)

with col_right:
    st.subheader("⚙️ Actions")
    
    if st.button("🚀 Initiate Autonomous Resolution", type="primary"):
        sku_data = selected_data.to_dict()
        orchestrator = Orchestrator()
        
        # Clear previous state
        st.session_state["analysis_result"] = None
        log_container.empty()
        
        # Custom callback to update UI in real-time
        def update_ui(agent_name, message):
            render_graph(agent_name)
            with log_container:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(f"**{agent_name}**: {message}")
            time.sleep(0.5) # Faster for better UX

        with st.spinner("Orchestrating agents..."):
            result_context = orchestrator.run(sku_data)
            
        # Replay logs for visual effect
        for log in result_context["logs"]:
            if "]" in log:
                agent_name = log.split("]")[0].replace("[", "")
                message = log.split("]")[1].strip()
            else:
                agent_name = "System"
                message = log
            update_ui(agent_name, message)
            
        render_graph(None)
        
        # Save result to state
        st.session_state["analysis_result"] = result_context
        st.success("Workflow Completed. Data Updated.")
        time.sleep(1)
        st.rerun() # Rerun to update top metrics, but state will preserve logs

    # Display Final Summary & Changes if available
    if st.session_state["analysis_result"]:
        res = st.session_state["analysis_result"]
        
        st.markdown("### 📋 Executive Summary")
        st.info(res.get("final_summary", "No summary."))
        
        st.markdown("### 📊 Data Updates Applied")
        
        # Calculate Deltas
        old_forecast = selected_data['Forecast'] # Note: This might be the NEW value if we reran. 
        # To show true delta, we'd need to capture 'before' state. 
        # But since we reran, 'selected_data' is now the UPDATED data.
        # So we can just show the Current Values as "New State".
        
        st.write("**New System State:**")
        st.write(f"- **Forecast**: {res.get('new_forecast', 'Unchanged')}")
        st.write(f"- **On Order**: {res.get('sku_data', {}).get('On_Order', 'Unchanged')}") # This comes from context, might be old if not updated in context object
        
        # Better: Show what the agents *decided*
        if res.get("new_forecast"):
             st.write(f"✅ **Forecast Updated**: -> {res['new_forecast']}")
        
        proc_action = res.get("procurement_action") or ""
        if "Create PO" in proc_action:
             st.write(f"✅ **Procurement**: {proc_action}")
             
        inv_action = res.get("inventory_action") or ""
        if "Transfer" in inv_action:
             st.write(f"✅ **Inventory**: {inv_action}")

