from typing import Annotated, Sequence, TypedDict
# Annotated: lets you attach metadata/extra info to a type hint (e.g. Annotated[str, "some rule"])
# Sequence: read-only ordered collection type hint (accepts list, tuple, etc.)
# TypedDict: lets you define a dictionary with fixed keys and specific value types

from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage
# BaseMessage: the parent class for all message types (HumanMessage, AIMessage, etc.)
# Used as a type hint when you want to accept ANY kind of message

from langchain_core.messages import ToolMessage
# ToolMessage: represents the result/response returned by a tool after it is called by the AI

from langchain_core.messages import SystemMessage
# SystemMessage: the system-level instruction message sent to the LLM (e.g. "You are a helpful assistant")

from langchain_core.messages import AIMessage

from langchain_openai import ChatOpenAI

from langchain_core.tools import tool
# @tool: a decorator that converts a regular Python function into a LangChain-compatible tool
# that the LLM can decide to call during a conversation

from langgraph.graph.message import add_messages
# add_messages: a reducer function that tells LangGraph HOW to update the messages list in state
# instead of replacing the list, it APPENDS new messages to the existing ones

from langgraph.graph import StateGraph, END
# StateGraph: the main graph class in LangGraph — you build your AI workflow as a graph of nodes and edges
# END: a special constant that marks the terminal/exit point of the graph (where execution stops)

from langgraph.prebuilt import ToolNode
# ToolNode: a pre-built LangGraph node that automatically handles tool execution
# when the LLM decides to call a tool, ToolNode runs it and returns a ToolMessage

import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, ".env")

load_dotenv(dotenv_path=env_path, override=True)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(a: int, b: int):
    """This is an addition function that adds two functions together"""

    return a + b

@tool
def subtract(a: int, b: int):
    """This is a subtraction function that subtracts two functions together"""

    return a - b

@tool
def multiply(a: int, b: int):
    """This is a multiplication function that multiplies two functions together"""

    return a * b

tools = [add, subtract, multiply]

model = ChatOpenAI(model = "gpt-4o-mini").bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content= 
        "You are my AI assistant, please answer my query to the best of your ability."
    )
    response = model.invoke([system_prompt] + list(state["messages"]))
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    last_message = messages[-1]

    if isinstance(last_message, AIMessage) and last_message.tool_calls:

        return "continue"
    else:
        return "end"

graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools = tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    }
)

graph.add_edge("tools", "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs: AgentState =  {"messages": [HumanMessage(content="Add 34 + 21. Multiply 5 * 6")]}
# OR inputs = AgentState(messages=[HumanMessage(content="Add 3 + 4.")])

print_stream(app.stream(inputs, stream_mode= "values"))