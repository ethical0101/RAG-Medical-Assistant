from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from langchain_core import documents
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from pydantic import Field
from typing import List, Optional
from logger import logger
import os

router = APIRouter()

@router.post("/ask")
async def ask_question(
    question: str = Form(...),
    top_k: int = Form(3),
    retriever: Optional[BaseRetriever] = None
):
    try:
        logger.info(f"User query: {question}")

        #Embed model + pinecone setup
        pc=Pinecone(api_key=os.environ.get("PINCONE_API_KEY"))
        index=pc.Index(os.environ.get("PINCONE_INDEX_NAME", "medicalindex"))
        embed_model=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", output_dimensionality=768)
        embedded_query=embed_model.embed_query(question)
        res = index.query(vector=embedded_query, top_k=top_k, include_metadata=True)

        docs = [
            Document(
                page_content=match["metadata"].get("text"), metadata=match["metadata"]
            ) for match in res["matches"]
            if match.get("metadata") and match["metadata"].get("text")
        ]

        class SimpleRetriever(BaseRetriever):
            docs: List[Document]

            def _get_relevant_documents(self, query: str) -> List[Document]:
                return self.docs

        retriever = SimpleRetriever(docs=docs)
        chain = get_llm_chain(retriever)
        result = query_chain(chain, question)

        logger.info("Query processed successfully.")
        return result

    except Exception as e:
        logger.exception("Error during processing question", exc_info=True)
        return JSONResponse(status_code=500, content={"message": "An error occurred while processing the question."})
