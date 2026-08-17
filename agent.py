import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
                        "description": "The mathematical expression to evaluate, e.g., '2 + 2' or '65 * 1.8 + 32'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# Map names to functions
AVAILABLE_FUNCTIONS = {
    "get_current_location": get_current_location,
    "get_weather": get_weather,
    "calculate": calculate
}

def run_agent(user_query: str, max_iterations: int = 5):
    """Runs the AI agent to answer a user query using tools if necessary."""
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. Use tools when necessary to answer the user's questions. For temperature conversions, you can use the calculate tool."},
        {"role": "user", "content": user_query}
    ]
    
    for i in range(max_iterations):
        logger.info(f"Iteration {i+1}: Sending request to model...")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        messages.append(message)
        
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
            
    logger.warning("Max iterations reached without a final answer.")
    return "I am sorry, but I reached the maximum number of iterations."

if __name__ == "__main__":
    test_queries = [
        "What is the weather in my current location?",
        "What is 25 * 4?",
        "What is the capital of France?"
    ]
    
    for query in test_queries:
        print(f"\n--- Testing Query: {query} ---")
        run_agent(query)
