import asyncio
from fastmcp import Client, FastMCP

# HTTP server
client = Client("http://127.0.0.1:8000/mcp")

async def main():
    async with client:
        # Basic server interaction
        await client.ping()

        # List available operations
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()

        # Execute operations
        # result = await client.call_tool("example_tool", {"param": "value"})
        print(tools)

asyncio.run(main())