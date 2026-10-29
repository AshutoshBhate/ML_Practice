import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server = StdioServerParameters(command="python", args=["server.py"])


async def main():
    with open("server_log.txt", "w") as log:
        async with stdio_client(server, errlog=log) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool("count_notes", {})
                print(result.content[0].text)

                result = await session.call_tool("add_note", {"text": "Book the meeting room"})
                print(result.content[0].text)

                result = await session.call_tool("count_notes", {})
                print(result.content[0].text)

    with open("server_log.txt") as log:
        print(log.read())


asyncio.run(main())
