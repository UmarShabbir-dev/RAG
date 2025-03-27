import os.path
from langchain_community.document_loaders import PyPDFLoader,TextLoader,Docx2txtLoader, UnstructuredURLLoader
import tempfile

from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.embeddings import HuggingFaceEmbeddings

import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PineconeStore

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI


load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME")

def process_document(filename:str, file_bytes:bytes, openai_key:str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(tmp_path)
    elif filename.endswith(".txt"):
        loader = TextLoader(tmp_path)
    elif filename.endswith(".docx"):
        loader = Docx2txtLoader(tmp_path)
    else:
        raise ValueError("Unsupported File Format")
    
    docs = loader.load()
    return embed_and_store(docs, openai_key)
    
def process_url(url:str, openai_key:str):
    loader = UnstructuredURLLoader(urls=[url])
    docs = loader.load()
    return embed_and_store(docs, openai_key)
    
def embed_and_store(docs, openai_key:str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n","\n",".","!","?"," ",""]
    )
    chunks = splitter.split_documents(docs)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    PineconeStore.from_documents(chunks,embeddings, index_name = index_name)
    return f"{len(chunks)} chunks uploaded to pinecone"

def query_pinecone(query:str, openai_key:str):
    embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
    db = PineconeStore.from_existing_index(index_name,embeddings)
    retriever = db.as_retriever()
    llm = ChatOpenAI(temperature = 0, model = "gpt-3.5-turbo", openai_api_key = openai_key)
    qa = RetrievalQA.from_chain_type(llm=llm,retriever = retriever)
    return qa.run(query)