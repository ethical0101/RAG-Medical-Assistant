from fastapi import APIRouter, UploadFile, File
from typing import List
from modules.load_vectorstore import load_vectorstore
from fastapi.responses import JSONResponse
from logger import logger


router = APIRouter()

@router.post("/upload_pdfs")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        logger.info(f"Received {len(files)} files for upload.")
        load_vectorstore(files)
        logger.info(f"Document added to vector store successfully.")
        return {"message": f"Successfully uploaded and processed files."}

    except Exception as e:
        logger.exception("Error during pdf upload", exc_info=True)
        return JSONResponse(status_code=500, content={"message": "An error occurred while uploading PDFs."})
