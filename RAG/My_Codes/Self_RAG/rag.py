import os
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, List, Any, cast
from langgraph.graph import StateGraph, END

from models import GradeDocuments

class GraphState(TypedDict):
    """The state of the graph."""
    question: str
    documents: list
    generation: str
    rewrite_count: int

class AdvancedSelfRAG:
    def __init__(self):
        self.vectorstore: Any = None
        self.rag_chain: Any = None
        self.question_rewriter: Any = None
        self.retrieval_grader: Any = None
        self.graph: Any = None
        self.retriever: Any = None
        self.db_path = "./qdrant_db"
        self.collection_name = "cohere_docs"

    def initialize(self):
        embeddings_model = OpenAIEmbeddings()

        if os.path.exists(self.db_path):
            print("Found existing database on disk. Skipping scraping")
            
            client = QdrantClient(path=self.db_path)
            self.vectorstore = QdrantVectorStore(
                client=client,
                collection_name=self.collection_name,
                embedding=embeddings_model
            )
            
        else:
            print("No database found. Scraping the web and creating embeddings")
            
            # Load Data
            target_urls = [
                "https://docs.cohere.com/docs/the-cohere-platform",
                "https://docs.cohere.com/docs/get-started-installation",
                "https://docs.cohere.com/docs/rerank",
                "https://docs.cohere.com/docs/cohere-embed"
            ]
            loader = WebBaseLoader(
                web_paths=target_urls,
                bs_kwargs=dict(parse_only=bs4.SoupStrainer("main"))
            )
            docs = loader.load()

            # Split text
            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                model_name="text-embedding-3-small",
                chunk_size=256,
                chunk_overlap=32,
            )
            splits = text_splitter.split_documents(docs)

            # Store on disk
            self.vectorstore = QdrantVectorStore.from_documents(
                documents=splits,
                embedding=embeddings_model,
                path=self.db_path,  
                collection_name=self.collection_name
            )
            print("Scraping complete. Data saved to disk!")

        # Build the Retriever
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        # Setup LLM Grader
        system_prompt = """You are a grader assessing relevance of a retrieved document to a user question. \n 
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
        It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""

        grade_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
            ]
        )

        structured_llm_grader = llm.with_structured_output(GradeDocuments)
        self.retrieval_grader = grade_prompt | structured_llm_grader
        print("LLM Grader initialized!")
        
        # Generation Chain, the old RAG prompt
        template = """You are a helpful assistant. Answer the question based ONLY on the following context. 
        If you don't know the answer from the context, just say that you don't know.

        Context: {context}

        Question: {question}

        Answer:"""
        prompt = ChatPromptTemplate.from_template(template)
        
        self.rag_chain = prompt | llm | StrOutputParser()
        print("Generation Chain initialized!")

        # Rewriter Chain
        rewrite_system = """You are a question re-writer that converts an input question to a better version that is optimized 
        for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning."""
        
        rewrite_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", rewrite_system),
                ("human", "Here is the initial question: \n\n {question} \n Formulate an improved question."),
            ]
        )
        self.question_rewriter = rewrite_prompt | llm | StrOutputParser()
        print("Rewrite Chain initialized!")

        # Compiling the Graph
        workflow = StateGraph(GraphState)

        workflow.add_node("retrieve", self.retrieve_node)
        workflow.add_node("generate", self.generate_node)
        workflow.add_node("rewrite", self.rewrite_node)

        workflow.set_entry_point("retrieve")

        workflow.add_conditional_edges(
            "retrieve",
            self.is_relevant,
            {
                "generate": "generate",
                "rewrite": "rewrite",
            }
        )
        workflow.add_edge("rewrite", "retrieve")
        workflow.add_edge("generate", END)

        self.graph = workflow.compile()
        print("LangGraph Compiled and Ready!")

    # Graph nodes and edges
    def retrieve_node(self, state: GraphState):
        """Retrieves documents based on the question."""
        print("\n Node: Retrieve")
        question = state["question"]

        documents = self.retriever.invoke(question)
        count = state.get("rewrite_count", 0)

        return {"documents": documents, "question": question, "rewrite_count": count}

    def generate_node(self, state: GraphState):
        """Generates the final answer using retrieved documents."""
        print("\n Node: Generate")
        question = state["question"]
        documents = state["documents"]

        doc_txt = "\n\n".join(doc.page_content for doc in documents)
        generation = self.rag_chain.invoke({"context": doc_txt, "question": question})

        return {"generation": generation}

    def rewrite_node(self, state: GraphState):
        """Rewrites the question to get better search results."""
        print("\n Node: Rewrite Question")
        question = state["question"]
        count = state.get("rewrite_count", 0)

        better_question = self.question_rewriter.invoke({"question": question})
        print(f"Original Question: {question}")
        print(f"Rewritten Question: {better_question}")

        return {"question": better_question, "rewrite_count": count + 1}

    def is_relevant(self, state: GraphState) -> str:
        """Conditional Edge: Evaluates if the retrieved documents are relevant."""
        print("\n Edge: Check Relevance")
        question = state["question"]
        documents = state["documents"]
        rewrite_count = state.get("rewrite_count", 0)

        if rewrite_count >= 3:
            print("Edge: Max Rewrites reached, forcing Generation")
            return "generate"

        print("Edge: Grading Documents")
        for doc in documents:
            score = self.retrieval_grader.invoke({"question": question, "document": doc.page_content})
            
            if score.binary_score.lower() == "yes":
                print("Edge: Relevant documents found, routing to Generate")
                return "generate"

        print("Edge: No relevant documents, routing to Rewrite")
        return "rewrite"

    # API Entry Point
    def ask(self, question: str) -> str:
        if not self.graph:
            raise RuntimeError("Graph is not initialized.")
            
        initial_state = cast(GraphState, {"question": question, "rewrite_count": 0})
        final_state = self.graph.invoke(initial_state)
        
        return final_state["generation"]

rag_engine = AdvancedSelfRAG()