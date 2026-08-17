# AI Agent with Tool/Function Calling

This project implements an autonomous AI agent capable of invoking tools (functions) to answer user queries accurately. It integrates with the OpenAI API and demonstrates a functional tool-calling loop, multi-step execution, and safety guardrails.

## Architecture & Features

- **Tool Definitions (Checkpoint 1)**: Defines 3 modular tools (`get_current_location`, `get_weather`, `calculate`) using strict JSON schemas.
- **Tool Selection (Checkpoint 2)**: The model accurately selects the appropriate tools based on user queries, or answers directly.
- **Execution & Synthesis (Checkpoint 3)**: Parses tool arguments, executes local Python functions, and synthesizes tool outputs into a natural language response.
- **Chained Execution (Checkpoint 4)**: The agent can invoke multiple tools in a single session, solving multi-step problems (e.g., location -> weather).
- **Infinite Loop Guardrail (Checkpoint 5)**: Limits execution to a maximum of 5 iterations to prevent runaway token usage.
- **Structured Logging (Checkpoint 6)**: Prints detailed, structured logs showcasing the iteration steps, tool arguments, and synthetic responses.

## Setup Instructions

1. **Clone the repository** (if not already done).
2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**:
   Copy the example environment file and insert your API key.
   ```bash
   cp .env.example .env
   # Edit .env and replace your_api_key_here with your OpenAI API key
   ```

## Execution

Run the agent script to see the tool-calling loop in action:

```bash
python agent.py
```

### Sample Output Log
```
--- Testing Query: What is the weather in my current location? ---
2026-08-17 22:15:00 - INFO - Iteration 1: Sending request to model...
2026-08-17 22:15:02 - INFO - Tool called: get_current_location with arguments: {}
2026-08-17 22:15:02 - INFO - Tool output: San Francisco, CA
2026-08-17 22:15:02 - INFO - Iteration 2: Sending request to model...
2026-08-17 22:15:04 - INFO - Tool called: get_weather with arguments: {'location': 'San Francisco, CA'}
2026-08-17 22:15:04 - INFO - Tool output: 65F and sunny
2026-08-17 22:15:04 - INFO - Iteration 3: Sending request to model...
2026-08-17 22:15:06 - INFO - Final Answer synthesized:
The weather in your current location, San Francisco, CA, is 65°F and sunny.
```
