# Addis-Sync Streamlit UI - Quick Guide

## ✅ App is Running!

**Local URL**: http://localhost:8501
**Network URL**: http://192.168.1.4:8502

## Features

### 🏠 Main Interface
- **Chat Interface**: Type your query and get responses
- **Service Cards**: Visual overview of all 5 service domains
- **Quick Stats**: Track messages and session status
- **Sample Queries**: Pre-written examples for each service

### 🛠️ Services Available
1. **🚨 Emergency** - Fire, Medical, Accidents
2. **⚡ Power** - Outages, Transformers
3. **🗑️ Sanitation** - Waste, Sewer, Drainage
4. **🏗️ Infrastructure** - Roads, Bridges, Lights
5. **💧 Utility** - Water Supply, Pipes

### ⚙️ Sidebar
- System status indicator
- Service domain cards with color coding
- Clear chat button
- Help section

## How to Use

1. **Open the app** in your browser (automatically opens)
2. **Type your issue** in the chat input at the bottom
3. **Provide woreda** when asked
4. **Get response** with office contact and ticket number

## Example Queries

Try these:
- "There's a power outage in Bole"
- "The garbage hasn't been collected"
- "There's a pothole on the main road"
- "No water supply since this morning"

## Current Status

⚠️ **Note**: The app currently shows demo responses. Full agent integration requires:
- Proper google-adk Runner setup
- Session service implementation
- MCP server connection

The UI is fully functional and can be enhanced with actual agent responses once the Runner is properly configured.

## Stopping the App

Press `Ctrl+C` in the terminal where Streamlit is running.

## Restarting

```bash
uv run streamlit run app.py
```
