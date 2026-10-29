import asyncio
import json

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI()
model = "gpt-4o-mini"
server = StdioServerParameters(command="python", args=["server.py"])


async def main():
    with open("server_log.txt", "w") as log:
        async with stdio_client(server, errlog=log) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                tools_result = await session.list_tools()
                tools = []
                for tool in tools_result.tools:
                    tools.append(
                        {
                            "type": "function",
                            "function": {
                                "name": tool.name,
                                "description": tool.description,
                                "parameters": tool.inputSchema,
                            },
                        }
                    )

                messages = [{"role": "user", "content": "Calculate 25 + 17"}]

                response = await client.chat.completions.create(model=model, messages=messages, tools=tools)
                assistant_message = response.choices[0].message
                messages.append(assistant_message)

                if assistant_message.tool_calls:
                    for tool_call in assistant_message.tool_calls:
                        name = tool_call.function.name
                        args = json.loads(tool_call.function.arguments)
                        print("The model called:", name, args)

                        result = await session.call_tool(name, args)
                        messages.append(
                            {"role": "tool", "tool_call_id": tool_call.id, "content": result.content[0].text}
                        )

                    final_response = await client.chat.completions.create(model=model, messages=messages, tools=tools)
                    print(final_response.choices[0].message.content)
                else:
                    print(assistant_message.content)


asyncio.run(main())
