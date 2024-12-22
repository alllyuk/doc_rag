from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
from src.scrape import start_scrapy
import os
import uuid
import logging
import shutil

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Initialize FastAPI app
app = FastAPI(title="RAG Pipeline API", description="API LLM-приложения для работы с документацией")


@app.post("/upload-doc")
async def upload_and_index_document(docs_url: str):
    documents = start_scrapy(docs_url)
    # тут место для генерации вашего милвуса 

    try:
        # Save the uploaded file to a temporary file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_id = insert_document_record(file.filename)
        success = index_document_to_chroma(temp_file_path, file_id)

        if success:
            return {"message": f"File {file.filename} has been successfully uploaded and indexed.", "file_id": file_id}
        else:
            delete_document_record(file_id)
            raise HTTPException(status_code=500, detail=f"Failed to index {file.filename}.")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    session_id = query_input.session_id or str(uuid.uuid4())
    logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, Model: {query_input.model.value}")


    chat_history = get_chat_history(session_id) #тут мы забираем историю запросов пользователя
    rag_chain = get_rag_chain(query_input.model.value) #а тут мы запускаем пайплайн
    answer = rag_chain.invoke({
        "input": query_input.question,
        "chat_history": chat_history
    })['answer']

    logging.info(f"Session ID: {session_id}, AI Response: {answer}")
    return QueryResponse(answer=answer, session_id=session_id)


@app.post("/delete-doc")