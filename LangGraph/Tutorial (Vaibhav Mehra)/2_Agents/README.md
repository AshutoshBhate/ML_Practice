# LangGraph Agents, File by File

Read the files in order, I to V. Each name is explained once, in the first file that uses it. Later files only cover what's new.

All five use `gpt-4o-mini` and run in `RAG_env`. Run them with `python Agent_N_....py`. They ask for input in the terminal, and you type `exit` to stop (Agent III takes no input, and Agent IV ends when it saves).

---

## Agent I: Simple Agent ([Agent_I_SimpleAgent.py](Agent_I_SimpleAgent.py))

**The key point:** One node sends your message to the model and prints the reply. Nothing is kept between turns, so it forgets everything you said before.

<pre style="font-size: 0.85em; line-height: 1.35; white-space: pre; overflow-x: auto;">
you type ──► invoke({"messages": [your message]}) ──► process ──► print
    ▲                                                               │
    └───────────── the next turn starts from scratch ◄──────────────┘
</pre>

- **`TypedDict`** (from `typing`): A dict with fixed keys and a type for each value. `AgentState` uses it, so LangGraph knows which keys the state has.
- **`List`** (from `typing`): The type hint for a list. `List[HumanMessage]` means "a list of `HumanMessage` objects".
- **`HumanMessage`** (from `langchain_core.messages`): The message you typed. LangChain wraps every message in a class that says who sent it: `HumanMessage` (you), `AIMessage` (the model), `SystemMessage` (instructions) and `ToolMessage` (a tool's result).
- **`ChatOpenAI`** (from `langchain_openai`): LangChain's wrapper around OpenAI's chat API. `llm.invoke(messages)` sends the list and returns an `AIMessage`, whose text is in `.content`.
- **`StateGraph`, `START`, `END`** (from `langgraph.graph`): `StateGraph(AgentState)` creates the graph. `START` and `END` are its built-in entry and exit points, so `add_edge(START, "process")` means "run `process` first".
- **`load_dotenv()`** (from `dotenv`): Reads `OPENAI_API_KEY` from a `.env` file into the environment, where `ChatOpenAI` looks for it. With no arguments it starts in the script's folder and walks up until it finds one, here `LangGraph/.env`.
- **Why it forgets:** The API keeps nothing between calls. Each call only sees the messages sent in that call, and the loop sends a new one-message list every turn.

---

## Agent II: Memory ([Agent_II_Memory.py](Agent_II_Memory.py))

**The key point:** It's the same graph as Agent I, but the conversation lives in `conversation_history`, outside the graph. Every turn sends the whole history in and takes the longer history back out, so the model "remembers".

<pre style="font-size: 0.85em; line-height: 1.35; white-space: pre; overflow-x: auto;">
turn 1:  [You1]               ──► process ──► [You1, AI1]
turn 2:  [You1, AI1, You2]    ──► process ──► [You1, AI1, You2, AI2]
            ▲ conversation_history = result["messages"] after each turn
</pre>

- **`Union[HumanMessage, AIMessage]`** (from `typing`): "Either of these types". The list now holds your messages and the model's.
- **`AIMessage`** (from `langchain_core.messages`): The model's reply, stored next to your messages.
- **`append(AIMessage(content=response.content))`:** `response` is already an `AIMessage`, but it also carries token counts, the model name and request IDs. Copying only the text into a fresh `AIMessage` keeps the history short.
- **`print("Messages in state:", len(state["messages"]))`:** `len` counts the messages in the list, so the count grows by two each turn: 2 after the first turn, 4 after the second.
- **Gone after `exit`:** `conversation_history` is an ordinary Python list, so the memory lives only while the program runs.

---

## Agent III: ReAct Agent ([Agent_III_ReActAgent.py](Agent_III_ReActAgent.py))

**The key point:** The model can now ask for tools. The graph loops model → tools → model until the model answers without asking for one. This loop is the ReAct pattern: Reason, act, repeat.

<pre style="font-size: 0.85em; line-height: 1.35; white-space: pre; overflow-x: auto;">
START ──► our_agent ──► should_continue ──"continue"──► tools (ToolNode)
             ▲               │                              │
             │             "end"                            │
             │               ▼                              │
             │              END                             │
             └──────────────────────────────────────────────┘
</pre>

- **`Annotated`** (from `typing`): Attaches extra information to a type hint, as `Annotated[type, extra]`. Python ignores the extra part, but LangGraph reads it.
- **`Sequence`** (from `typing`): A read-only ordered collection, such as a list or a tuple. Since it might be a tuple, `model_call` writes `list(state["messages"])` before adding the system message with `+`.
- **`BaseMessage`** (from `langchain_core.messages`): The parent class of every message type, so `Sequence[BaseMessage]` means "any kind of message".
- **`add_messages`** (from `langgraph.graph.message`): A reducer, which tells LangGraph how to merge what a node returns into the state. Without it, `return {"messages": [response]}` would replace the whole list. With it, the new message is appended. That's why the nodes return only the new message.
  - Read `messages: Annotated[Sequence[BaseMessage], add_messages]` as "a list of messages, merged with `add_messages`".
- **`SystemMessage`** (from `langchain_core.messages`): Instructions for the model. `model_call` puts it in front of the history on every call and never stores it in the state.
- **`@tool`** (from `langchain_core.tools`): Turns a Python function into a tool the model can ask for. The function name becomes the tool's name, the type hints become its arguments, and the docstring becomes the description the model reads to decide when to use it. That's why each docstring says exactly what the tool does.
- **`.bind_tools(tools)`:** Returns a copy of the model that sends the tool descriptions with every request. The model still never runs code. It replies with `tool_calls`: Which tool, with which arguments.
- **`ToolNode`** (from `langgraph.prebuilt`): A ready-made node. It reads the last message's `tool_calls`, runs each tool, and returns one `ToolMessage` per call.
- **`should_continue`:** The edge that makes the loop. Only an `AIMessage` has `tool_calls`, so `isinstance(last_message, AIMessage)` first checks the message's class: It's `True` only if the last message is an `AIMessage`. If its `tool_calls` list isn't empty it returns "continue" (go to tools), otherwise "end". `add_conditional_edges` maps each word to the next node.
- **`set_entry_point("our_agent")`:** The same as `add_edge(START, "our_agent")`.
- **`app.stream(inputs, stream_mode="values")`:** Runs the graph like `invoke`, but hands you the full state after every node instead of only at the end. `print_stream` prints the newest message each time with `pretty_print()`, LangChain's readable printout.
  - **Note:** The model asks for `add` and `multiply` in one reply, so `ToolNode` adds two `ToolMessage`s in one step and only the last one (`multiply` → 30) gets printed. The `add` result (55) is still in the state, and the final answer uses both.
- **`inputs: AgentState = {...}`:** `AgentState(messages=[...])` builds the same dict.

---

## Agent IV: Drafter ([Agent_IV_Drafter.py](Agent_IV_Drafter.py))

**The key point:** A ReAct loop with you inside it. The agent node asks you what to do, the model edits a document through two tools, and the run ends only after a successful save.

<pre style="font-size: 0.85em; line-height: 1.35; white-space: pre; overflow-x: auto;">
START ──► agent ──► should_use_tools ──"tools"──► tools ──► should_continue
            ▲              │                                  │        │
            │         "ask_user"                         "continue"  "end"
            │              │                                  │        ▼
            └──────────────┴──────────────────────────────────┘       END
</pre>

- **`document_content` (a global):** The tools need one place to keep the document between calls. `update` overwrites it (`global` lets a function change a variable defined outside it), and `save` writes it to a file. The system prompt is rebuilt every turn with the current text, so the model always sees the latest version.
- **The `Args:` part of `save`'s docstring:** `@tool` reads it too, so the model knows what `filename` is for.
- **The `try/except` in `save`:** By default, `ToolNode` only catches bad tool arguments. Any other error, like a failed file write, would crash the program. The `try/except` turns a failure into a normal message that the model reads and tells you about.
- **The three cases at the top of `our_agent`:**
  1. **Empty state (the first turn):** A fixed opening message, "I'm ready to help you update a document...", so the model greets you first. It's written in the AI's voice but sent as a `HumanMessage`.
  2. **The last message is a `ToolMessage`:** A tool just ran, so the model reads its result before you're asked anything.
  3. **Anything else:** `input()` asks you.
- **`return {"messages": [user_message, response]}`:** The node built your message itself, so it returns both and `add_messages` appends them. `user_message` stays `None` when there was nothing new from you.
- **`should_use_tools`, after the agent:** Go to tools if the reply asked for one, otherwise back to the agent, which asks you again.
- **`should_continue`, after the tools:** End only if the last tool was `save` and it said "saved successfully". The name alone isn't enough, because the `try/except` makes a failed save look like a normal message.
- **`print_messages`:** Prints a tool result when the newest message is one, which happens right after the tools node runs. As in Agent III, only the newest message is printed.
- **`if __name__ == "__main__":`** Python sets `__name__` to `"__main__"` in the file you run directly. So `run_document_agent()` runs when you start this file, but not if another file imports it.
- **`os.path.dirname(__file__)`:** Python sets `__file__` to this script's path, and `dirname` cuts off the file name. So `save` writes the file next to the script, wherever you run it from. Git ignores it (`LangGraph/Tutorial (Vaibhav Mehra)/2_Agents/*.txt` in `.gitignore`).

---

## Agent V: RAG Agent ([Agent_V_RAG.py](Agent_V_RAG.py))

**The key point:** Retrieval as a tool. The PDF is split into chunks and stored in Chroma once, and the model calls `retriever_tool` to look things up before it answers. Unlike Agent III, the tools here run in a hand-written node instead of `ToolNode`.

<pre style="font-size: 0.85em; line-height: 1.35; white-space: pre; overflow-x: auto;">
once:      PDF ──► 9 pages ──► 24 chunks ──► embeddings ──► chroma_db/

each question:
START ──► llm ──► should_continue ──True──► retriever_agent (take_action)
           ▲            │                          │
           │          False                        │
           │            ▼                          │
           │           END                         │
           └───────────────────────────────────────┘
</pre>

- **`temperature=0`:** Makes the model pick its most likely words, so answers vary less and stick closer to the retrieved text. gpt-5 models don't accept it, and LangChain quietly drops it for them.
- **`OpenAIEmbeddings(model="text-embedding-3-small")`:** Turns text into a list of 1536 numbers, so texts with similar meanings get similar numbers. The rule is to use the same embedding model to store the chunks and to search them. It doesn't have to match the chat model.
- **`folder = os.path.dirname(__file__)`:** As in Agent IV, the PDF and the database are found next to the script, wherever you run it from.
- **`if os.path.exists(persist_directory)`:** Build the store once, then reuse it. Calling `Chroma.from_documents` on a saved folder adds every chunk again, so each later run would return each chunk twice. `chroma_db/` is in `.gitignore`.
- **`PyPDFLoader(pdf_path).load()`** (from `langchain_community`): One `Document` per PDF page.
- **`RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)`** (from `langchain_text_splitters`): Splits the pages into chunks of up to 1000 characters. Neighbouring chunks share 200 characters, so a sentence cut at a boundary still appears whole in one of them.
- **`Chroma`** (from `langchain_chroma`): The vector database. `Chroma.from_documents(...)` embeds every chunk and saves it, and `Chroma(...)` opens what's already saved.
- **`as_retriever(search_kwargs={"k": 5})`:** A retriever returns the `k` chunks closest to the query, here 5.
- **`retriever_tool`:** Labels the chunks "Document 1" to "Document 5", so the model can cite them, as the system prompt asks.
- **`add_messages`:** Imported from LangGraph, as in Agent III. The old line imported Python's `operator.add` under the name `add_messages`. That also works as a reducer (it just joins the two lists), but the name pretended it was LangGraph's.
- **`should_continue`:** Returns `True` or `False`, and `{True: "retriever_agent", False: END}` maps those to the next node directly.
- **`tools_dict = {our_tool.name: our_tool for our_tool in tools}`:** Finds a tool by the name the model asked for.
- **`take_action` (the "retriever agent" node):** Does by hand what `ToolNode` did in Agent III. For each tool call it checks that the name exists, runs the tool with `invoke(t["args"])`, and wraps the result in a `ToolMessage` with the same `tool_call_id`, so the model can match each result to its call.
- **`running_agent`:** Each question starts a new state holding only that question, so this agent doesn't remember earlier questions. Agent II's memory idea isn't used here.
