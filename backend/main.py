from fastapi import FastAPI, UploadFile, File, Form


app = FastAPI


@app.post("/upload-doc/")
async def upload_doc(file: UploadFile = File(...), openai_key: str = Form(...)):
    file_bytes = await file.read()
    return {"message": "Document Uploaded Successfully"}
    
@app.post("/upload-url/")
async def upload_url(url: str = Form(...), openai_key: str = Form(...)):
    return {"message": "Url Processed"}

@app.get("/get-answer/")
async def get_answer(query: str, openai_key:str):
    return {"answer"}
    
    