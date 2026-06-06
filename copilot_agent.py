import asyncio
import os
import subprocess
from copilot import CopilotClient

async def check_port_status(arguments: dict) -> dict:
    """Custom tool: check if a given port is in use."""
    port = arguments.get("port")
    if not port:
        return {"error": "No port provided"}
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

async def main():
    if "GITHUB_TOKEN" not in os.environ:
        print("⚠️  Please set the GITHUB_TOKEN environment variable")
        return

    print("🚀 Connecting to Copilot Engine...")
    client = CopilotClient()

    # Await the coroutine to get the session, then use it as a context manager
    session = await client.create_session()
    async with session:
        session.register_tool(
            name="check_port",
            description="Checks if a specific TCP port is currently listening on the system.",
            handler=check_port_status
        )

        prompt = "Check if port 8080 is active on this machine right now."
        print(f"💬 Prompting agent: '{prompt}'\n")

        async for event in session.prompt_stream(prompt):
            if event.type == "text":
                print(event.text, end="", flush=True)
            elif event.type == "tool_call":
                print(f"\n🔧 [Agent Action] Invoking tool: {event.tool_name}")

if __name__ == "__main__":
    asyncio.run(main())
