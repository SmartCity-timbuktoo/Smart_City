# 🏙️ Smart City Agent: Urban Infrastructure Coordination Platform

This project is a multi-agent system designed to manage and coordinate various urban services for a smart city. It uses a central coordinating agent and several specialized sub-agents to handle requests related to emergency services, power, sanitation, infrastructure, and utilities.

## 🚀 Features

- **Multi-Agent Architecture**: A core customer service agent routes tasks to specialized agents.
- **Specialized Sub-Agents**: Separate agents for:
    - 🚨 **Emergency**: Manages emergency reports (fire, medical, accidents).
    - ⚡ **Power**: Handles power outages and grid issues.
    - 🗑️ **Sanitation**: Coordinates waste collection and sewage problems.
    - 🏗️ **Infrastructure**: Tracks and manages issues with roads, bridges, and public lighting.
    - 💧 **Utility**: Manages water supply and other utility services.
- **Interactive Interfaces**:
    - **Streamlit Web UI**: A user-friendly web interface for interacting with the system.
    - **Command-Line Interface (CLI)**: For testing and direct interaction with the agents.
- **Persistent Sessions**: Manages conversation context and state using a session manager.
- **Dedicated Databases**: Each sub-agent has its own database for managing its domain-specific data.

## 🏛️ Architecture

The system is built around a central **Customer Service Agent** that acts as the primary point of contact. When a user submits a query, this agent determines the nature of the request and routes it to the appropriate specialized sub-agent.

1.  **User Interface (Streamlit / CLI)**: The user interacts with the system.
2.  **Customer Service Agent**: Receives the user's message.
3.  **Routing**: The agent identifies the correct sub-agent (e.g., Power Agent for a power outage).
4.  **Sub-Agent Processing**: The specialized sub-agent takes over, processes the request, interacts with its dedicated database, and formulates a response.
5.  **Response**: The response is relayed back to the user through the main interface.

This modular design allows for clear separation of concerns and makes the system easily extensible.

## 📂 Project Structure

```
Smart_City/
│
├── app.py                  # Main Streamlit application entry point
├── run_cli.py              # Main CLI application entry point
├── requirements.txt        # Python dependencies
│
└── smart_city_agent/
    ├── agent.py            # Main customer service agent
    ├── local_runner.py     # ADK runner for local execution
    │
    ├── sub_agent/          # Directory for specialized agents
    │   ├── Emergency_Agent/
    │   ├── Power_Agent/
    │   └── ...
    │
    ├── mcp_server/         # Master Control Program server components
    │   ├── server.py
    │   └── ...
    │
    └── database/           # SQL database schemas and data
        ├── emergency_db/
        └── ...
```

## ⚙️ Setup and Installation

1.  **Prerequisites**:
    - Python 3.9+
    - `uv` package manager (`pip install uv`)

2.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd Smart_City
    ```

3.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

4.  **Install dependencies**:
    ```bash
    uv pip install -r requirements.txt
    ```

5.  **Set up environment variables**:
    - Create a file named `.env` in the project root.
    - Add your Google API key to the `.env` file:
      ```
      GOOGLE_API_KEY="your_api_key_here"
      ```

## ▶️ Usage

You can interact with the Smart City Agent platform through either the Streamlit Web UI or the CLI.

### Streamlit Web UI

For a rich, interactive experience, use the Streamlit application.

1.  **Launch the app**:
    ```bash
    streamlit run app.py
    ```
2.  Your web browser should automatically open with the UI. If not, navigate to the local URL shown in your terminal (usually `http://localhost:8501`).

### Command-Line Interface (CLI)

For quick tests and direct interaction, use the CLI.

1.  **Run the CLI**:
    ```bash
    python run_cli.py
    ```
2.  You can now type your queries directly into the terminal.
3.  Type `exit`, `quit`, or `q` to end the session.

## ✅ Testing

To verify that all components are set up correctly and the agents are functioning, you can run the integration tests.

```bash
pytest
```
