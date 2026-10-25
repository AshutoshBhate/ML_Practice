import asyncio
import json

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI

load_dotenv()

openai_client = AsyncOpenAI()
model = "gpt-4o-mini"
server = StdioServerParameters(command="python", args=["server.py"])


async def get_mcp_tools(session):
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

    return tools


async def process_query(session, query):
    tools = await get_mcp_tools(session)
    messages = [{"role": "user", "content": query}]

    response = await openai_client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
    )
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

        final_response = await openai_client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="none",
        )
        return final_response.choices[0].message.content
    else:
        return assistant_message.content


async def main():
    with open("server_log.txt", "w") as log:
        async with stdio_client(server, errlog=log) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                query = "What is our company's vacation policy?"
                print(query)
                answer = await process_query(session, query)
                print(answer)


asyncio.run(main())
