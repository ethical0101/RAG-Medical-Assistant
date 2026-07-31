from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.exception_handler import catch_exception_middleware
from routes.uplaod_pdfs import router as upload_router
from routes.ask_question import router as ask_router

app = FastAPI(title="RAG Medical Agent", description="A Retrieval-Augmented Generation (RAG) Medical Agent API", version="1.0.0")

#CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



#Middleware exception Handlers
app.middleware("http")(catch_exception_middleware)

#routers

#1. upload pdfs documents
app.include_router(upload_router, prefix="/api", tags=["Upload PDFs"])
#2. asking query
app.include_router(ask_router, prefix="/api", tags=["Ask Question"])

@app.get("/")
async def root():
    return {"status": "healthy", "message": "RAG Medical Agent API is running"}

