# Checkpoint Submissions

Below are the text and code snippets corresponding to each checkpoint, ready for direct copy-pasting into the submission boxes.

---

### Checkpoint 1: Tool Definitions
**Description:** Defining 3 modular tools with explicit JSON schemas and parameter definitions.

**Code Snippet:**
```python
# Tools
def get_current_location():
    """Returns the current location of the user."""
    return "San Francisco, CA"

def get_weather(location: str):
    """Returns the current weather for a given location."""
    if "San Francisco" in location:
        return "65F and sunny"
    return "70F and clear"

def calculate(expression: str):
    """Evaluates a mathematical expression and returns the result."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error evaluating expression: {e}"

# Tool Definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_location",
            "description": "Get the current location of the user.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g., San Francisco, CA"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate, e.g., '2 + 2'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]
```

---

### Checkpoint 2: Tool Selection
**Description:** Configuring the model to invoke appropriate tools. We enable this by passing `tools=TOOLS` and `tool_choice="auto"` to the OpenAI chat completions endpoint.

**Code Snippet:**
```python
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
```

---

### Checkpoint 3: Execution & Synthesis
**Description:** Parsing tool calls, executing functions locally, appending the result as a tool message, and allowing the model to synthesize a final answer.

**Code Snippet:**
```python
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                logger.info(f"Tool called: {function_name} with arguments: {function_args}")
                
                function_to_call = AVAILABLE_FUNCTIONS.get(function_name)
                if function_to_call:
                    function_response = function_to_call(**function_args)
                    logger.info(f"Tool output: {function_response}")
                    
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(function_response)
                    })
                else:
                    logger.warning(f"Function {function_name} not found.")
        else:
            logger.info(f"Final Answer synthesized:\n{message.content}")
            return message.content
```

---

### Checkpoint 4: Chained Execution
**Description:** The structure leverages a loop (`for i in range(max_iterations):`) to repeatedly feed tool results back into the model until a final answer is returned. This handles sequences like retrieving location, then querying weather.

**Code Snippet:**
```python
def run_agent(user_query: str, max_iterations: int = 5):
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. Use tools when necessary..."},
        {"role": "user", "content": user_query}
    ]
    
    for i in range(max_iterations):
        # ... completion request and tool execution code ...
        # if no tool calls are made, synthesize and return final response.
```

---

### Checkpoint 5: Infinite Loop Guardrail
**Description:** Hard `max_iterations` ceiling is set to `5` iterations to stop runaway loops and cap API costs.

**Code Snippet:**
```python
def run_agent(user_query: str, max_iterations: int = 5):
    # ...
    for i in range(max_iterations):
        # ... execution ...
            
    logger.warning("Max iterations reached without a final answer.")
    return "I am sorry, but I reached the maximum number of iterations."
```

---

### Checkpoint 6: Structured Logging & Traces
**Description:** Using Python's `logging` module to display iteration steps, tool names, passed arguments, and outputs cleanly in the console.

**Code Snippet:**
```python
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Usage Example:
logger.info(f"Iteration {i+1}: Sending request to model...")
logger.info(f"Tool called: {function_name} with arguments: {function_args}")
logger.info(f"Tool output: {function_response}")
logger.info(f"Final Answer synthesized:\n{message.content}")
```
