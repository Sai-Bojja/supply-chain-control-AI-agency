# 🏗️ Supply Chain Control AI Agency
### An Autonomous Multi-Agent System for Enterprise Inventory Orchestration

This repository contains a production-grade multi-agent AI system designed to automate the "Detect-Investigate-Resolve" loop in supply chain management. Built with a custom Python orchestration layer on top of the OpenAI SDK, the system moves beyond static forecasting by utilizing autonomous agents to handle complex, context-aware procurement tasks.

## 🌟 Key Differentiator: Seasonal Intelligence
Unlike traditional human-led workflows or static ERP logic that often treat inventory demand as linear, this agency is engineered to account for temporal context.

*   **The "Pumpkin Spice" Effect:** The agents autonomously identify seasonal trends (e.g., Summer BBQ peaks, Autumn seasonal flavors) and trigger proactive procurement cycles months in advance.
*   **Proactive vs. Reactive:** While a human team might miss a subtle seasonal shift until stock-outs occur, the `forecast_agent` identifies the upcoming demand curve and initiates the procurement loop.

## 🛠️ System Architecture
The agency follows a modular, "Separation of Concerns" design pattern. Each agent is a specialist inheriting from a unified base class to ensure consistent tool-use and logging.

### 📂 Repository Structure

#### `agents/` - The Core Intelligence Layer
*   `base_agent.py`: Abstract base class defining the shared schema for all agents.
*   `monitoring_agent.py`: Monitors real-time inventory levels and detects anomalies.
*   `forecast_agent.py`: Handles seasonal logic and demand prediction.
*   `root_cause_agent.py`: Diagnoses the "Why" behind stock gaps (e.g., transit delays vs. demand spikes).
*   `inventory_agent.py`: Identifies cross-location stock transfer opportunities to resolve local deficits.
*   `procurement_agent.py`: Executes the math for SKU quantities and vendor selection.
*   `communication_agent.py` & `email_agent.py`: Orchestrates human-in-the-loop notifications and summaries.
*   `tools.py`: Centralized library of validated functions (SQL connectors, web-search, etc.) available to the agents.

#### `core/` - Orchestration & State
*   `orchestrator.py`: The main runtime that manages agent handoffs, context propagation, and state transitions.
*   `state.py`: Defines the `AgentState` schema used to track SKU status across the lifecycle.
*   `llm_service.py`: Helper service for LLM interaction.

#### `data/` & Scripts
*   `data/`: Directory for storing inventory datasets (`inventory_data_real.csv`).
*   `app.py`: Streamlit-based dashboard for real-time monitoring and agent interaction.
*   `generate_data.py`: Script to generate realistic synthetic supply chain data with seasonality.

## 🛡️ Production-Grade Features
1.  **Custom Orchestration (OpenAI SDK)**
    Built natively on the OpenAI SDK (Prompt + Tools + Handoffs) rather than high-level wrappers. This allows for:
    *   **Lower Latency:** Minimal overhead between agent transitions.
    *   **Granular Control:** Precise management of system prompts and tool-calling validation.

2.  **Observability**
    Every "Reasoning Chain" is logged and displayed in the application UI:
    *   **Audit Trails:** See exactly why an agent decided to buy 500 units of a seasonal item.
    *   **Hallucination Prevention:** Structured output validation and logged reasoning steps to ensure reliability.

3.  **Human-in-the-Loop (HITL)**
    While the agents are autonomous, the system is designed for supervised execution. The `email_agent` drafts procurement recommendations for human approval before final orders are executed in the ERP.

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   OpenAI API Key

### Installation

```bash
# Clone the repository
git clone https://github.com/Sai-Bojja/supply-chain-control-AI-agency.git
cd supply-chain-control-AI-agency

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
export OPENAI_API_KEY='your-key'
# Optional: SMTP settings for email agent
# export SMTP_EMAIL='your_email@example.com'
# export SMTP_PASSWORD='your_password'
# export SMTP_SERVER='smtp.gmail.com'
# export SMTP_PORT='587'
```

### Running the Application

1.  **Generate Data (Optional):**
    If you want to start with a fresh dataset, run the generator:
    ```bash
    python generate_data.py
    ```

2.  **Launch the Dashboard:**
    ```bash
    streamlit run app.py
    ```

## 📊 Impact
*   **Automated Forecasting:** Reduced manual stock-check time by identifying seasonal shifts 2-3 weeks before human intervention.
*   **Data Integrity:** Centralized tool-use ensures all agents pull from a "Single Source of Truth" database.
*   **Strategic Procurement:** Enabled proactive buying strategies for high-variance seasonal SKUs.
