# 🇪🇹 Addis-Sync: Intelligent Urban Infrastructure Orchestrator

![Status](https://img.shields.io/badge/Status-Operational-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B)
![Agents](https://img.shields.io/badge/Agents-Gemini%202.0-8E44AD)
![Architecture](https://img.shields.io/badge/Architecture-Hub%20%26%20Spoke-orange)

**Addis-Sync** is a next-generation **Multi-Agent System (MAS)** designed to modernize urban service delivery in Addis Ababa. It serves as a centralized AI hub that intelligently routes citizen reports to specialized domain agents (Power, Water, Emergency, etc.), manages service tickets, and coordinates with municipal dispatch centers.

---

## 🏗️ Architecture: The "Local Runner" Engine

Addis-Sync runs on a custom **Local Runner** architecture designed to bypass dependency locks while leveraging the latest Gemini 2.5 Flash models.

### 🌟 Core Components

1.  **Hub-and-Spoke Agent Mesh**
    *   **Customer Service (Root)**: The brain. Uses semantic routing to classify user intent and delegate to specialists.
    *   **Specialist Agents (Spokes)**:
        *   🚑 **Emergency**: Fire, Ambulance, Police dispatch.
        *   ⚡ **Power**: Outage reporting and grid status.
        *   🗑️ **Sanitation**: Waste management and sewer issues.
        *   🏗️ **Infrastructure**: Road and construction hazards.
        *   💧 **Utility**: Water supply and hydraulic systems.

2.  **Local Runner Adapter** (`smart_city_agent/local_runner.py`)
    *   A high-performance adapter that replaces `vertexai.agent_engines`.
    *   **Agentic Loop**: Implements a multi-turn ReAct loop allowing agents to *Search -> Act -> Confirm* in a single user turn.
    *   **Tool Registry**: Dynamicaly discovers and registers Python functions as MCP (Model Context Protocol) tools.
    *   **Session Manager**: In-memory state tracking for conversation context (Woreda, Ticket History).

3.  **MCP Servers (Model Context Protocol)**
    *   5 dedicated "mock" servers simulating municipal databases.
    *   PostgreSQL-compatible queries (using local objects for the hackathon).
    *   Provides tools like `create_ticket`, `find_closest_office`, `get_status`.

---

## 🚀 Installation

This project is managed efficiently with `uv`.

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Google Cloud API Key (Gemini)

### Setup

1.  **Clone & Install**
    ```powershell
    git clone https://github.com/YourRepo/addis-sync.git
    cd addis-sync
    uv sync
    ```

2.  **Environment Configuration**
    Create a `.env` file in the root:
    ```ini
    GOOGLE_API_KEY=your_gemini_api_key_here
    GOOGLE_GENAI_USE_VERTEXAI=False
    ```

---

## 🖥️ Usage: The Multi-App Ecosystem

Addis-Sync provides two distinct interfaces orchestrated by a single launcher.

### 🟢 Start the Full System

Run the master orchestrator to launch both the Citizen App and Admin Dashboard simultaneously:

```powershell
uv run python run_system.py
```

*The orchestrator manages port allocation, health checks, and graceful shutdown.*

### 📱 1. Citizen Interface (Port `8501`)
**URL:** `http://localhost:8501`
- **Audience:** General Public.
- **Features:**
    - Natural language issue reporting ("My lights went out in Bole").
    - Real-time ticket creation.
    - AI-driven guidance and routing.

### 📊 2. Admin & Worker Dashboard (Port `8502`)
**URL:** `http://localhost:8502`
- **Audience:** City Operations, Dispatchers.
- **Features:**
    - **Admin Role:** Read-only global view of all tickets across all 5 departments.
    - **Worker Role:** Department-specific task lists.
    - **Action**: Update ticket status (RECEIVED → IN_PROGRESS → RESOLVED) which persists to the database.

---

## 📂 Project Structure

```bash
addis/
├── admin_worker_app.py       # 📊 Operations Dashboard (Streamlit)
├── app.py                    # 📱 Citizen Interface (Streamlit)
├── run_system.py             # 🎮 Master Orchestrator
├── requirements.txt          # Dependency lock
├── smart_city_agent/         # 🧠 Core Agent Logic
│   ├── agent.py              # Root Agent Definition
│   ├── local_runner.py       # ⚙️ Custom Execution Engine & Tool Registry
│   ├── session_manager.py    # Session State & History
│   ├── message_processor.py  # Chat Loop Logic
│   ├── mcp_server/           # 🔌 Tool Implementations (SQL mocks)
│   └── sub_agent/            # 🤖 Specialist Agent Definitions
│       ├── Emergency_Agent/
│       ├── Power_Agent/
│       ├── ...
└── .env                      # Configuration
```

---

## 🛠️ Key Technical Features

### Dynamic Tool Discovery
Tools are decorated with `@server.tool()` in the MCP layer. The `LocalRunner` inspects imported modules at runtime, populating a global registry. This allows agents to "wake up" with new capabilities simply by adding a function.

### Context-Aware Session State
The system maintains a sticky session state. If a user mentions "Bole Woreda" in turn 1, the Power Agent knows this location in turn 5 without asking again.
*Implemented via `InMemorySessionService`.*

### Multi-Agent Handoff
While disguised as a single conversation, the Root Agent dynamically swaps system instructions and toolsets based on intent classification, effectively "becoming" the specialist needed for the task.

---

## 🤝 Contributing

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingUpgrade`).
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

---


