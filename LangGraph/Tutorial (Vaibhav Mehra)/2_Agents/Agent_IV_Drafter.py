from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import os

load_dotenv()

# This is the global variable to store document content
document_content = ""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def update(content: str) -> str:
    """Updates the document with the provided content"""

    global document_content
    document_content = content

    return f"Document has been updated successfully! The current content is:\n{document_content}"

@tool
def save(filename: str) -> str:
    """Save the current document to the text file and finish the process.

    Args:
        filename: Name for the text file.
    """

    global document_content

    if not filename.endswith('.txt'):
        filename = f"{filename}.txt"

    file_path = os.path.join(os.path.dirname(__file__), filename)

    try:
        with open(file_path, 'w') as file:
            file.write(document_content)
        print(f"\n Document has been saved to: {filename}")
        return f"Document has been saved successfully to '{filename}'."

    except Exception as e:
        return f"Error saving document: {str(e)}"


tools = [update, save]

model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

def our_agent(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=f"""
    You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.

    - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
    - If the user wants to save and finish, you need to use the 'save' tool.
    - Make sure to always show the current document state after modifications.

    The current document content is:{document_content}
    """)

    messages_to_pass = list(state["messages"])
    user_message = None

    if not messages_to_pass:
        user_input = "I'm ready to help you update a document. What would you like to create?"
        user_message = HumanMessage(content=user_input)
        messages_to_pass.append(user_message)
    elif isinstance(messages_to_pass[-1], ToolMessage):
        pass
    else:
        user_input = input("\nWhat would you like to do with the document? ")
        print(f"\n USER: {user_input}")
        user_message = HumanMessage(content=user_input)
        messages_to_pass.append(user_message)

    all_messages = [system_prompt] + messages_to_pass

    response = model.invoke(all_messages)

    print(f"\n AI: {response.content}")
    if response.tool_calls:
        print(f" USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    if user_message:
        return {"messages": [user_message, response]}
    else:
        return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    """Determine if we should continue or end the conversation."""

    last_message = state["messages"][-1]

    if last_message.name == "save" and "saved successfully" in last_message.content:
        return "end"

    return "continue"

def print_messages(messages):
    """Function I made to print the messages in a more readable format"""
    if messages and isinstance(messages[-1], ToolMessage):
        print(f"\n TOOL RESULT: {messages[-1].content}")


graph = StateGraph(AgentState)

graph.add_node("agent", our_agent)

tool_node = ToolNode(tools= tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("agent")

def should_use_tools(state: AgentState) -> str:
    """Route to tools if the last AI message contains tool calls, else ask user for more input."""
    messages = state["messages"]
    if messages and isinstance(messages[-1], AIMessage) and messages[-1].tool_calls:
        return "tools"
    return "ask_user"

graph.add_conditional_edges(
    "agent",
    should_use_tools,
    {
        "tools": "tools",
        "ask_user": "agent",
    },
)

graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue": "agent",
        "end": END,
    },
)

app = graph.compile()

def run_document_agent():
    print("\n ===== DRAFTER =====")

    state = AgentState(messages=[])

    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])

    print("\n ===== DRAFTER FINISHED =====")

if __name__ == "__main__":
    run_document_agent()