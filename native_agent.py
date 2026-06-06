import asyncio
import os
import subprocess
import json
import httpx

# 1. Define the actual system execution logic
def check_port_status(port: int) -> dict:
    """Executes a local network sweep to see if a port is listening."""
    try:
        result = subprocess.run(
            ["ss", "-tln"], capture_output=True, text=True, timeout=5
        )
        if f":{port}" in result.stdout:
            return {"status": "in use", "port": port}
        else:
            return {"status": "free", "port": port}
    except Exception as e:
        return {"error": str(e)}

# 2. Map string identifiers to our functional code
AVAILABLE_TOOLS = {
    "check_port": check_port_status
}

# 3. Define the tool schema so the cloud model understands what it can ask for
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "check_port",
            "description": "Checks if a specific TCP port is currently active and listening on this host machine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "port": {
                        "type": "integer",
                        "description": "The port number to check (e.g., 8080, 8085)."
                    }
                },
                "required": ["port"]
            }
        }
    }
]

async def run_autonomous_agent(prompt: str):
    # Fallback to standard OpenAI/Open-Router/Custom endpoints to maintain absolute OS compatibility
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GITHUB_TOKEN")
    base_url = "https://api.openai.com/v1/chat/completions" # Change to your target endpoint/proxy
    model_name = "gpt-4o" # Swap to your preferred available model
    
    if not api_key:
        print("⚠️  Error: Please export an API token into your environment variables.")
        return

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Build the initial execution context payload
    messages = [
        {"role": "system", "content": "You are an autonomous systems engineering agent. Use tools to verify machine states."},
        {"role": "user", "content": prompt}
    ]

    async with httpx.AsyncClient() as client:
        print(f"💬 Dispatching task: '{prompt}'")
        
        # Turn 1: Ask the model what to do
        response = await client.post(
            base_url,
            headers=headers,
            json={"model": model_name, "messages": messages, "tools": TOOLS_SCHEMA},
            timeout=30
        )
        
        response_data = response.json()
        message = response_data["choices"][0]["message"]

        # Check if the model decided it needs to execute a tool
        if "tool_calls" in message and message["tool_calls"]:
            messages.append(message) # Append assistant thought process to history
            
            for tool_call in message["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                tool_args = json.loads(tool_call["function"]["arguments"])
                call_id = tool_call["id"]
                
                print(f"\n🔧 [Agent Request] Wants to run '{tool_name}' with args: {tool_args}")
                
                if tool_name in AVAILABLE_TOOLS:
                    # Execute the tool natively inside Termux
                    execution_result = AVAILABLE_TOOLS[tool_name](tool_args["port"])
                    print(f"📥 [Local Output] Result: {execution_result}")
                    
                    # Feed the real runtime system execution back to the model
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call_id,
                        "name": tool_name,
                        "content": json.dumps(execution_result)
                    })
            
            # Turn 2: Send execution results back so the model can read it and summarize
            final_response = await client.post(
                base_url,
                headers=headers,
                json={"model": model_name, "messages": messages},
                timeout=30
            )
            
            final_data = final_response.json()
            print(f"\n🤖 [Agent Response]:\n{final_data['choices'][0]['message']['content']}")
        else:
            print(f"\n🤖 [Agent Response]:\n{message['content']}")

if __name__ == "__main__":
    # Test task: Let's check port 8080 or change it to 8085 depending on what you're tracking
    asyncio.run(run_autonomous_agent("Check if port 8080 is active right now."))
