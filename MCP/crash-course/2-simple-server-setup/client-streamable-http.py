import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

url = "http://127.0.0.1:8050/mcp"


async def main():
    async with streamable_http_client(url) as (read, write, get_session_id):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print(get_session_id())

            tools_result = await session.list_tools()
            tool = tools_result.tools[0]
            print(tool.name)
            print(tool.description)

            result = await session.call_tool("add", {"a": 2, "b": 3})
            print(result.content[0].text)


asyncio.run(main())
