import asyncio
import json

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from openai import AsyncOpenAI

load_dotenv()

openai_client = AsyncOpenAI()
model = "gpt-4o-mini"
url = "http://127.0.0.1:8060/mcp"


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


async def run_conversation(session, messages, tools):
    while True:
        response = await openai_client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
        )
        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            return message.content

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            result = await session.call_tool(name, args)
            print("The model called:", name, args, "->", result.content[0].text)
            messages.append(
                {"role": "tool", "tool_call_id": tool_call.id, "content": result.content[0].text}
            )


async def main():
    async with streamable_http_client(url) as (read, write, get_session_id):
        async with ClientSession(read, write) as session:
            await session.initialize()

            offices = await session.read_resource("zones://offices")
            tools = await get_mcp_tools(session)

            for date in ["2026-10-28", "2026-11-05"]:
                prompt = await session.get_prompt("plan_meeting", {"date": date, "time": "15:00"})
                messages = [
                    {"role": "system", "content": "Our offices and their time zones:\n" + offices.contents[0].text},
                    {"role": "user", "content": prompt.messages[0].content.text},
                ]

                print(date)
                answer = await run_conversation(session, messages, tools)
                print(answer)
                print()


asyncio.run(main())
