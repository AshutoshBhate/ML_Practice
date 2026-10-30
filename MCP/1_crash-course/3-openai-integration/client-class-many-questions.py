import asyncio
import json
from contextlib import AsyncExitStack

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI

load_dotenv()


class MCPOpenAIClient:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.openai_client = AsyncOpenAI()
        self.exit_stack = AsyncExitStack()
        self.session = None

    async def connect_to_server(self, server_script_path="server.py"):
        server = StdioServerParameters(command="python", args=[server_script_path])
        log = self.exit_stack.enter_context(open("server_log.txt", "w"))

        read, write = await self.exit_stack.enter_async_context(stdio_client(server, errlog=log))
        self.session = await self.exit_stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()

    async def get_mcp_tools(self):
        tools_result = await self.session.list_tools()

        tools = []
        for tool in tools_result.tools:
            tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.input_schema,
                    },
                }
            )

        return tools

    async def process_query(self, query):
        tools = await self.get_mcp_tools()
        messages = [{"role": "user", "content": query}]

        response = await self.openai_client.chat.completions.create(
            model=self.model,
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

                result = await self.session.call_tool(name, args)
                messages.append(
                    {"role": "tool", "tool_call_id": tool_call.id, "content": result.content[0].text}
                )

            final_response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="none",
            )
            return final_response.choices[0].message.content
        else:
            return assistant_message.content

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    client = MCPOpenAIClient()
    await client.connect_to_server()

    questions = [
        "What is our company's vacation policy?",
        "How many days a week can I work from home?",
        "What is the capital of France?",
    ]
    for question in questions:
        print(question)
        answer = await client.process_query(question)
        print(answer)
        print()

    await client.cleanup()


asyncio.run(main())
