import asyncio
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

sandbox = os.path.abspath("sandbox")
server = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem@2.0.1", sandbox],
)


async def main():
    os.makedirs(sandbox, exist_ok=True)
    file_path = os.path.join(sandbox, "hello.txt")
    sub_dir = os.path.join(sandbox, "subdir")
    new_path = os.path.join(sub_dir, "hello_moved.txt")
    outside_path = os.path.abspath("client.py")

    if os.path.exists(new_path):
        os.remove(new_path)

    with open("server_log.txt", "w") as log:
        async with stdio_client(server, errlog=log) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                tools_result = await session.list_tools()
                print(len(tools_result.tools), "tools")

                result = await session.call_tool("write_file", {"path": file_path, "content": "Hello from my MCP client!"})
                print(result.content[0].text)

                result = await session.call_tool("read_text_file", {"path": file_path})
                print(result.content[0].text)

                result = await session.call_tool("create_directory", {"path": sub_dir})
                print(result.content[0].text)

                result = await session.call_tool("move_file", {"source": file_path, "destination": new_path})
                print(result.content[0].text)

                result = await session.call_tool("search_files", {"path": sandbox, "pattern": "**/*.txt"})
                print(result.content[0].text)

                result = await session.call_tool("read_text_file", {"path": outside_path})
                print(result.is_error)
                print(result.content[0].text)


asyncio.run(main())
