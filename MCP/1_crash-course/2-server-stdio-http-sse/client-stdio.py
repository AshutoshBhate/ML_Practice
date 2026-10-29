import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server = StdioServerParameters(command="python", args=["server.py", "stdio"])


async def main():
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            tool = tools_result.tools[0]
            print(tool.name)
            print(tool.description)

            result = await session.call_tool("add", {"a": 2, "b": 3})
            print(result.content[0].text)


asyncio.run(main())
