import os.path
from langchain_community.document_loaders import PyPDFLoader,TextLoader,Docx2txtLoader, UnstructuredURLLoader
import tempfile

from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.embeddings import HuggingFaceEmbeddings

def process_document(filename:str, file_bytes:bytes):
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
    
def process_url(url:str):
    loader = UnstructuredURLLoader(urls=[url])
    docs = loader.load()
    
def embed_and_store(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n","\n",".","!","?"," ",""]
    )
    chunks = splitter.split_documents(docs)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")