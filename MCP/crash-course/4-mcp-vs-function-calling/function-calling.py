import json

from dotenv import load_dotenv
from openai import OpenAI

from tools import add

load_dotenv()

client = OpenAI()
model = "gpt-4o-mini"

tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "First number"},
                    "b": {"type": "integer", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        },
    }
]

messages = [{"role": "user", "content": "Calculate 25 + 17"}]

response = client.chat.completions.create(model=model, messages=messages, tools=tools)
assistant_message = response.choices[0].message
messages.append(assistant_message)

if assistant_message.tool_calls:
    for tool_call in assistant_message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print("The model called:", name, args)

        result = add(args["a"], args["b"])
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(result)})

    final_response = client.chat.completions.create(model=model, messages=messages, tools=tools)
    print(final_response.choices[0].message.content)
else:
    print(assistant_message.content)
