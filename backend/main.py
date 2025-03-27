from fastapi import FastAPI, UploadFile, File, Form
from rag_utils import process_document,process_url,query_pinecone

app = FastAPI


@app.post("/upload-doc/")
async def upload_doc(file: UploadFile = File(...), openai_key: str = Form(...)):
    file_bytes = await file.read()
    result = process_document(file.filename,file_bytes,openai_key)
    return {"message": "Document Uploaded Successfully", "result":result}
    
@app.post("/upload-url/")
async def upload_url(url: str = Form(...), openai_key: str = Form(...)):
    result = process_url(url,openai_key)
    return {"message": "Url Processed", "result":result}

@app.get("/get-answer/")
async def get_answer(query: str, openai_key:str):
    answer = query_pinecone(query,openai_key)
    return {"answer":answer}