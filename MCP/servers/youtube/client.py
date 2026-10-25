import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server = StdioServerParameters(command="python", args=["server.py"])
video = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


async def main():
    with open("server_log.txt", "w") as log:
        async with stdio_client(server, errlog=log) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool("get_transcript", {"video_url_or_id": video})
                transcript = result.content[0].text
                print(len(transcript), "characters")
                print(transcript[:300])


asyncio.run(main())
