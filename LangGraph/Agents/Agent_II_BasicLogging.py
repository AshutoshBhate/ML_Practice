# We'll build an agent that remembers what we said in the previous prompts
# Chatbot with memory
# To create a form of memory for our Agent

from typing import Dict, List, TypedDict, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, ".env")

load_dotenv(dotenv_path=env_path, override=True)

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]  # HumanMessage and AIMessage are datatypes in LangChain and LangGraph


llm = ChatOpenAI(model= "gpt-4o-mini")

def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""

    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")

    print("CURRENT STATE: ", state["messages"])

    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

conversation_history = []

user_input = input("Enter: ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]
    user_input = input("Enter: ")

# One disadvantage of this setup is that after we exit, the memory is essentially
# wiped off. We tackle this by introducing a .txt file

with open("logging.txt", "w") as file:
    file.write("Your Converstaion Log:\n")
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("End of Converstaion")

print("Conversation saved to logging.txt")