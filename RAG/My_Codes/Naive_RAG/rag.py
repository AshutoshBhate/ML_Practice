import os
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class NaiveRAG:
    def __init__(self):
        self.vectorstore = None
        self.rag_chain = None
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

        # Build the chain
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        template = """You are a helpful assistant. Answer the question based ONLY on the following context. 
        If you don't know the answer from the context, just say that you don't know.

        Context: {context}

        Question: {question}

        Answer:"""
        prompt = ChatPromptTemplate.from_template(template)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    def ask(self, question: str) -> str:
        if not self.rag_chain:
            raise RuntimeError("RAG chain is not initialized.")
        return self.rag_chain.invoke(question)

rag_engine = NaiveRAG()