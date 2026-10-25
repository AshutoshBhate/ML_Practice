# Agentic AI Learning Order

This is the order to study everything in `ML_Practice/` for the Agentic AI side of your resume: OpenAI API calls, agentic workflow patterns, MCP, LangGraph, RAG and preference-based RL. Each step uses only what earlier steps taught, so nothing appears before it's explained.

Where a step has notebooks, read the notebook instead of the bare `.py` file. A **Supplement** notebook is the same code with short explanations. An **Exhaustive** notebook holds the deep-dive notes.

---

## Phase 1: Calling an LLM (Day 1)

Goal: Call an LLM, get structured output back, and let it use tools.

1. **Basic API call:** [Supplement_openai_api_example.ipynb](LLM_Learning_Sandbox/Simple_OpenAI_API_Prompts/Supplement_openai_api_example.ipynb). How `client.chat.completions.create()` works, what the `system` and `user` roles do, and where the answer sits in the response (`completion.choices[0].message.content`).
2. **The same call, cleaner:** [Supplement_1-basic.ipynb](LLM_Learning_Sandbox/Workflow_Patterns_Course/1-introduction/Supplement_1-basic.ipynb), then [Exhaustive_1-basic.ipynb](LLM_Learning_Sandbox/Workflow_Patterns_Course/1-introduction/Exhaustive_1-basic.ipynb).
3. **Structured output:** [Supplement_2-structured.ipynb](LLM_Learning_Sandbox/Workflow_Patterns_Course/1-introduction/Supplement_2-structured.ipynb), then [Exhaustive_2-structured.ipynb](LLM_Learning_Sandbox/Workflow_Patterns_Course/1-introduction/Exhaustive_2-structured.ipynb). `chat.completions.parse()` with a Pydantic class (`CalendarEvent`), so the reply comes back as a typed object instead of free text.
4. **Function calling:** [Supplement_3-tools.ipynb](LLM_Learning_Sandbox/Workflow_Patterns_Course/1-introduction/Supplement_3-tools.ipynb), then [Exhaustive_3-tools.ipynb](LLM_Learning_Sandbox/Workflow_Patterns_Course/1-introduction/Exhaustive_3-tools.ipynb). You describe a `get_weather` tool, the model asks to call it, your code runs it, and the result goes back to the model for the final answer.
5. **Function calling on your own files:** [LocalFileSystem_Interaction.ipynb](LLM_Learning_Sandbox/File_System_Agent/LocalFileSystem_Interaction.ipynb). The same loop with file-reading and file-writing tools. Note that the model only *chooses* the function. Your code is what runs it.
6. **Retrieval as a tool:** [Supplement_4-retrieval.ipynb](LLM_Learning_Sandbox/Workflow_Patterns_Course/1-introduction/Supplement_4-retrieval.ipynb), then [Exhaustive_4-retrieval.ipynb](LLM_Learning_Sandbox/Workflow_Patterns_Course/1-introduction/Exhaustive_4-retrieval.ipynb). A `search_kb` tool reads `kb.json`, and the model decides when to look something up. This is RAG in its smallest form.

After Phase 1 you can explain: Structured output, the tool-calling loop, and why retrieval matters.

---

## Phase 2: Agentic Workflow Patterns (Day 2)

Goal: Know the four patterns for chaining LLM calls together, and when to use each.

7. **Prompt chaining:** [Supplement_1-prompt-chaining.ipynb](LLM_Learning_Sandbox/Workflow_Patterns_Course/2-workflow-patterns/Supplement_1-prompt-chaining.ipynb). Three calls in a row (extract the event, parse its details, write a confirmation), with a gate check that stops the chain early when the request isn't a calendar event.
8. **Routing:** [Supplement_2-routing.ipynb](LLM_Learning_Sandbox/Workflow_Patterns_Course/2-workflow-patterns/Supplement_2-routing.ipynb). One call classifies the request as `new_event`, `modify_event` or `other`, and the code sends it to the matching handler.
9. **Parallelization:** [Supplement_3-parallelization.ipynb](LLM_Learning_Sandbox/Workflow_Patterns_Course/2-workflow-patterns/Supplement_3-parallelization.ipynb). `asyncio.gather()` runs a calendar check and a security check at the same time.
10. **Orchestrator-worker:** [Supplement_4-orchestrator.ipynb](LLM_Learning_Sandbox/Workflow_Patterns_Course/2-workflow-patterns/Supplement_4-orchestrator.ipynb). An orchestrator plans a blog post's sections, workers write each section, and a reviewer polishes the whole post.

After Phase 2 you can explain: The four patterns, when each one fits, and how they combine.

---

## Phase 3: MCP (Days 3–4)

Goal: Build an MCP server, connect clients to it, and explain how MCP differs from plain function calling.

MCP comes right after Phase 1 because it only builds on function calling. It doesn't need LangGraph or RAG.

11. **What MCP is:** [1-understanding-mcp/README.md](MCP/crash-course/1-understanding-mcp/README.md), sections 1 to 3. What MCP is and the problem it solves.
12. **Architecture:** [1-understanding-mcp/README.md](MCP/crash-course/1-understanding-mcp/README.md), sections 4 to 10. Hosts, clients and servers, the messages, and the transports (STDIO, SSE, Streamable HTTP).
13. **Your first server:** [server.ipynb](MCP/crash-course/2-simple-server-setup/server.ipynb), which explains [server.py](MCP/crash-course/2-simple-server-setup/server.py) line by line.
14. **Connecting over STDIO:** [client-stdio.ipynb](MCP/crash-course/2-simple-server-setup/client-stdio.ipynb).
15. **Connecting over Streamable HTTP:** [client-streamable-http.ipynb](MCP/crash-course/2-simple-server-setup/client-streamable-http.ipynb).
16. **Connecting over SSE (legacy, read last):** [client-sse.ipynb](MCP/crash-course/2-simple-server-setup/client-sse.ipynb).
17. **MCP tools inside an OpenAI call:** [server.ipynb](MCP/crash-course/3-openai-integration/server.ipynb) (the knowledge base tool), then [client-simple.ipynb](MCP/crash-course/3-openai-integration/client-simple.ipynb) (one question), then [client.ipynb](MCP/crash-course/3-openai-integration/client.ipynb) (the same client as a class, with several questions over one connection).
18. **MCP versus function calling:** [mcp-vs-function-calling.ipynb](MCP/crash-course/4-mcp-vs-function-calling/mcp-vs-function-calling.ipynb). The same `add` tool used both ways, side by side.
19. **Running a server in Docker:** [docker.ipynb](MCP/crash-course/5-run-with-docker/docker.ipynb). The calculator server in a container over Streamable HTTP, with its `Dockerfile` and a client.
20. **Lifecycle:** [lifecycle.ipynb](MCP/crash-course/6-lifecycle-management/lifecycle.ipynb). How servers and clients start up, run and shut down, with a lifespan that opens and closes a database.
21. **A real client:** [client.ipynb](MCP/mcp_filesystem_client/client.ipynb). Starts the official Node.js filesystem server with `npx` over STDIO, then writes, reads, moves and searches files in a sandbox folder, and shows the server refusing a path outside it.
22. **A server from a tutorial:** [youtube.ipynb](MCP/servers/youtube/youtube.ipynb), then [README.md](MCP/servers/youtube/README.md). A `FastMCP` server with one `get_transcript` tool, rewritten from a tutorial and run over stdio with a Python client. The README shows how to add it to Claude Code or Claude Desktop.

After Phase 3 you can explain: Host, client and server, the three transports, building a server with FastMCP, MCP versus function calling, and running a server in Docker.

---

## Phase 4: LangGraph Basics (Day 5)

Goal: Understand state, nodes, edges, branches and loops.

23. **Hello world:** [Graph_I_HelloWorldAgent.ipynb](LangGraph/Graph_I_HelloWorldAgent.ipynb). A `StateGraph` with an `AgentState(TypedDict)`, one node, and `START → node → END`.
24. **Several state fields:** [Graph_II_MultipleInputs.ipynb](LangGraph/Graph_II_MultipleInputs.ipynb).
25. **Nodes in sequence:** [Graph_III_SequentialGraph.ipynb](LangGraph/Graph_III_SequentialGraph.ipynb). State flows through node A, then B, then C.
26. **Branching:** [Graph_IV_ConditionalGraph.ipynb](LangGraph/Graph_IV_ConditionalGraph.ipynb). `add_conditional_edges()` picks the next node from the state.
27. **Loops:** [Graph_V_LoopingGraph.ipynb](LangGraph/Graph_V_LoopingGraph.ipynb). An edge leads back to an earlier node. Every agent loop (ReAct, Self-RAG) is built on this.

[LangGraph_Slides.pdf](LangGraph/LangGraph_Slides.pdf) is the reference for this phase.

After Phase 4 you can explain: What a StateGraph is, how state moves through nodes, and why agents need loops.

---

## Phase 5: LangGraph Agents (Day 6)

Goal: Build agents with memory and tools in LangGraph.

28. **Simplest agent:** [Agent_I_SimpleAgent.py](LangGraph/Agents/Agent_I_SimpleAgent.py). One node calls `ChatOpenAI`, with no memory: `START → process → END`.
29. **Memory:** [Agent_II_BasicLogging.py](LangGraph/Agents/Agent_II_BasicLogging.py). The state keeps every `HumanMessage` and `AIMessage`, so the model sees the whole conversation. It's saved to `logging.txt` at the end.
30. **ReAct agent (study this one hardest):** [Agent_III_ReActAgent.py](LangGraph/Agents/Agent_III_ReActAgent.py). `@tool` functions, `bind_tools()`, a prebuilt `ToolNode`, and a `should_continue` edge that loops between the model and the tools until the model stops asking for tools.
31. **Human in the loop:** [Agent_IV_Drafter.py](LangGraph/Agents/Agent_IV_Drafter.py). A document editor with `update` and `save` tools. It asks you for input every turn and ends only once the document is saved.

After Phase 5 you can explain: The ReAct pattern, what `bind_tools()` and `ToolNode` do, and how a conditional edge routes to the tools.

---

## Phase 6: RAG Basics and a Naive RAG API (Days 7–8)

Goal: Build the basic RAG pipeline, put it inside an agent, and serve it as an API.

32. **The big picture:** [Advanced_RAG_Pipeline.png](RAG/Main_ArchitectureDiagram/Advanced_RAG_Pipeline.png). Look at it first and come back to it after each later step.
33. **The full basic pipeline:** [RAG_1-4_Indexing_Retrieval_Generation.ipynb](RAG/Tutorial/RAG_1-4_Indexing_Retrieval_Generation.ipynb). Load, split (`RecursiveCharacterTextSplitter`), embed (`OpenAIEmbeddings`), store (Qdrant), retrieve, generate, and LCEL (the `|` syntax that chains the steps).
34. **RAG inside an agent:** [Agent_V_RAG.py](LangGraph/Agents/Agent_V_RAG.py). The Phase 5 agent loop with a retriever tool over a PDF stored in Chroma. Here the tools run by hand through `tools_dict` instead of `ToolNode`.
35. **Mini project, first try:** [Iteration_1.ipynb](RAG/My_Codes/API_Documentation_Helper/Iteration_1.ipynb). Different ways to load web pages: `PlaywrightURLLoader`, then the Jina Reader API.
36. **Mini project, full pipeline:** [Iteration_2.ipynb](RAG/My_Codes/API_Documentation_Helper/Iteration_2.ipynb). `WebBaseLoader`, splitting by tiktoken tokens, Qdrant as the vector store, and an LCEL chain.
37. **Naive RAG as an API:** [naive-rag-api/models.py](RAG/FastAPI/naive-rag-api/models.py), then [rag.py](RAG/FastAPI/naive-rag-api/rag.py), then [main.py](RAG/FastAPI/naive-rag-api/main.py). Iteration 2 turned into a service: a `NaiveRAG` class builds the Qdrant store when the app starts, and `POST /ask` answers questions.

After Phase 6 you can explain: Every stage of the pipeline, how to put retrieval inside an agent, and how to serve RAG with FastAPI. You can also say what naive RAG lacks: nothing checks whether the retrieved documents are any good.

---

## Phase 7: Advanced RAG and Self-RAG (Days 9–10)

Goal: Know the techniques that fix naive RAG, and build Self-RAG with LangGraph.

38. **Better queries:** [RAG_5-9 Query Translation](<RAG/Tutorial/RAG_5-9_(QueryTranslation)_MultiQueryTranslation_RAG-Fusion_Decompostion.ipynb>). Multi-Query, RAG-Fusion (with reciprocal rank fusion), Decomposition (recursive and individual), Step-Back and HyDE.
39. **Picking the source:** [RAG_10-11 Routing and Query Construction](<RAG/Tutorial/RAG_10-11_(Routing_QueryConstruction)_Logical&SemanticRouting_QueryConstruction.ipynb>). Logical routing (the LLM picks the data source), semantic routing (embedding similarity picks it) and query construction (turning a question into a structured query or metadata filter).
40. **Better indexes:** [RAG_12-14 Indexing](<RAG/Tutorial/RAG_12-14_(Indexing)_Multi-RepresentationIndexing_RAPTOR_ColBERT.ipynb>). Multi-representation indexing, RAPTOR (explained, with no code) and ColBERT. The ColBERT cells didn't run, so the notebook falls back to a normal retriever there.
41. **Better retrieval and generation:** [RAG_15-18 Retrieval and Generation](<RAG/Tutorial/RAG_15-18_(Retrieval_Generation)_Retrieval_Re-Ranking_Generation.ipynb>). RAG-Fusion again, Cohere re-ranking, and links to LangChain's CRAG and Self-RAG notebooks and to a talk on the impact of long context. Self-RAG is built for real in item 43.
42. **The concept diagrams:** [Tutorial/Images/](RAG/Tutorial/Images/). Seventeen diagrams, one per technique. Use them as your mental models for interviews.
43. **Self-RAG as an API (your most important file):** [self-rag-langgraph/models.py](RAG/FastAPI/self-rag-langgraph/models.py), then [rag.py](RAG/FastAPI/self-rag-langgraph/rag.py), then [main.py](RAG/FastAPI/self-rag-langgraph/main.py). An `AdvancedSelfRAG` LangGraph graph: retrieve, grade each document with the `GradeDocuments` structured output, then either generate or rewrite the question and retrieve again. A `rewrite_count` in the state caps the retries. It matches the Bitwise internship bullet point.

After Phase 7 you can explain: Five query-translation techniques, routing, RAPTOR and ColBERT, re-ranking, CRAG and Self-RAG, and how the Self-RAG API fixes naive RAG.

---

## Phase 8: Reinforcement Learning and RLHF (Days 11–12)

Goal: Understand preference-based RL, reward models and the Bradley-Terry model.

44. **Gymnasium basics:** [Basic_Syntax.ipynb](ReinforcementLearning/Practice/Basic_Syntax.ipynb). `env.reset()`, `env.step()` and `env.render()`.
45. **PPO on a real task:** [LunarLander-v3.ipynb](ReinforcementLearning/Practice/LunarLander-v3.ipynb). Training and evaluating a Stable-Baselines3 PPO agent.
46. **Storing trajectories:** [CartPole-v1/buffers.py](ReinforcementLearning/Bitwise_Work/CartPole-v1/buffers.py). `TrajectoryBuffer` keeps whole episodes and samples random pairs to compare.
47. **The stand-in human:** [critic.py](ReinforcementLearning/Bitwise_Work/CartPole-v1/critic.py). `AutomatedCritic` scores each trajectory by summing its cart positions and prefers the higher score.
48. **The reward model (study the math):** [reward_model.py](ReinforcementLearning/Bitwise_Work/CartPole-v1/reward_model.py). `RewardNetwork` predicts a reward for each state, and is trained with the Bradley-Terry model, P(A preferred over B) = sigmoid(total reward of A − total reward of B), using `BCEWithLogitsLoss`.
49. **Swapping in the learned reward:** [environment.py](ReinforcementLearning/Bitwise_Work/CartPole-v1/environment.py). `PbRLWrapper` replaces CartPole's own reward with the reward model's prediction and logs every step to the buffer.
50. **The whole loop:** [main.ipynb](ReinforcementLearning/Bitwise_Work/CartPole-v1/main.ipynb). Train PPO on the learned reward, collect trajectory pairs, have the critic label them, update the reward model, and repeat. Then [watch.ipynb](ReinforcementLearning/Bitwise_Work/CartPole-v1/watch.ipynb) to see the trained agent play.
51. **Score-based teacher:** [CliffWalking-v1/MLP/](ReinforcementLearning/Bitwise_Work/CliffWalking-v1/MLP/). The same pipeline on CliffWalking. `teacher.py` gives each segment a number (−100 if it falls off the cliff, otherwise minus its distance to the goal) and prefers the higher one.
52. **Rule-based teacher:** [NonHardcoded_MLP/](ReinforcementLearning/Bitwise_Work/CliffWalking-v1/NonHardcoded_MLP/). `teacher.py` first turns each segment into events (fell off the cliff, reached the goal, moved closer, moved away), then compares them by priority: not dying first, then reaching the goal, then making progress.
53. **A non-neural reward model:** [Random_Forest/](ReinforcementLearning/Bitwise_Work/CliffWalking-v1/Random_Forest/). `reward_model.py` uses scikit-learn's `RandomForestRegressor` instead of a neural network, to compare classic ML with deep learning for reward models.

All three CliffWalking folders share the same files: `config.py`, `buffer.py`, `reward_model.py`, `teacher.py`, `train_rm.py`, `wrappers.py`, `main.ipynb` and `watch.ipynb`.

After Phase 8 you can explain: Preference-based RL, the Bradley-Terry model, how a reward model learns from trajectory comparisons, and how PPO trains on a learned reward. Then link it to LLMs: RLHF for ChatGPT uses the same idea, with human preferences between two answers in place of two trajectories.

---

## Interview Checklist

Tick each one once you can explain it out loud without looking.

**API and patterns**
- [ ] Structured output and function calling ([2-structured.py](LLM_Learning_Sandbox/Workflow_Patterns_Course/1-introduction/2-structured.py), [3-tools.py](LLM_Learning_Sandbox/Workflow_Patterns_Course/1-introduction/3-tools.py))
- [ ] The four workflow patterns, especially prompt chaining with gate checks and orchestrator-worker ([2-workflow-patterns/](LLM_Learning_Sandbox/Workflow_Patterns_Course/2-workflow-patterns/))

**MCP**
- [ ] What MCP is and how it differs from function calling ([4-mcp-vs-function-calling/](MCP/crash-course/4-mcp-vs-function-calling/))
- [ ] Host, client, server and the three transports ([1-understanding-mcp/README.md](MCP/crash-course/1-understanding-mcp/README.md))
- [ ] Building a server with FastMCP ([servers/youtube/server.py](MCP/servers/youtube/server.py))

**LangGraph**
- [ ] What a StateGraph is ([Graph_I_HelloWorldAgent.ipynb](LangGraph/Graph_I_HelloWorldAgent.ipynb))
- [ ] Conditional edges and loops ([Graph_IV_ConditionalGraph.ipynb](LangGraph/Graph_IV_ConditionalGraph.ipynb), [Graph_V_LoopingGraph.ipynb](LangGraph/Graph_V_LoopingGraph.ipynb))
- [ ] The ReAct pattern, `bind_tools()` and `ToolNode` ([Agent_III_ReActAgent.py](LangGraph/Agents/Agent_III_ReActAgent.py))

**RAG**
- [ ] What RAG is, and the pipeline: load, split, embed, store, retrieve, generate ([RAG_1-4](RAG/Tutorial/RAG_1-4_Indexing_Retrieval_Generation.ipynb))
- [ ] Multi-Query, RAG-Fusion and HyDE ([RAG_5-9](<RAG/Tutorial/RAG_5-9_(QueryTranslation)_MultiQueryTranslation_RAG-Fusion_Decompostion.ipynb>))
- [ ] Self-RAG: grading documents and rewriting the question in a loop ([self-rag-langgraph/rag.py](RAG/FastAPI/self-rag-langgraph/rag.py))

**RL**
- [ ] What preference-based RL is ([CartPole-v1/](ReinforcementLearning/Bitwise_Work/CartPole-v1/))
- [ ] The Bradley-Terry model for learning rewards ([reward_model.py](ReinforcementLearning/Bitwise_Work/CartPole-v1/reward_model.py))
- [ ] How this connects to RLHF for LLMs (no file, link CartPole to ChatGPT's training)

Total: About 12 study days at 3–5 hours a day. `TensorFlow/` isn't part of this order, since it isn't Agentic AI.
