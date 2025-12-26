# Addis-Sync CLI Runner - Usage Guide

## Quick Start

```bash
python run_cli.py
```

## What It Does

The CLI runner provides an interactive interface to test the Addis-Sync multi-agent platform.

## Features

- ✓ Interactive chat with the customer service agent
- ✓ Automatic routing to specialist sub-agents
- ✓ Session management for conversation context
- ✓ Support for all 5 service domains:
  - Emergency Response
  - Power Services
  - Sanitation Services
  - Infrastructure Services
  - Utility Services

## Example Usage

```
You: There's a power outage in Bole

Agent: I understand you're experiencing a power outage. I'm connecting you with our Power Agent who will help report this and provide Bole's power office contact information...
```

## Commands

- Type your query naturally
- Type `exit`, `quit`, or `q` to quit
- Press `Ctrl+C` to interrupt

## Requirements

- GOOGLE_API_KEY must be set in `.env` file
- All agent modules must be importable
- google-adk must be installed

## Troubleshooting

If the runner fails to initialize:
1. Check that `.env` contains GOOGLE_API_KEY
2. Verify all agents load: `python test_integration.py`
3. Check google-adk version: `pip show google-adk`
