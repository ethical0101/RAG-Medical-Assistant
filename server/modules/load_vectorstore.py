import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINCONE_API_KEY = os.getenv("PINCONE_API_KEY")
PINCONE_ENV = "us-east-1"
PINCONE_INDEX_NAME = "medicalindex"


if not GOOGLE_API_KEY:
	raise ValueError("GOOGLE_API_KEY is not set")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

pc = Pinecone(
    api_key=PINCONE_API_KEY,
)
spec=ServerlessSpec(cloud="aws", region=PINCONE_ENV)

existing_indexes = [i["name"] for i in pc.list_indexes()]

if PINCONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINCONE_INDEX_NAME,
        dimension=768,
        metric="dotproduct",
        spec=spec
    )
    while not pc.describe_index(PINCONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

    print(f"Created Pinecone index: {PINCONE_INDEX_NAME}")

index = pc.index(PINCONE_INDEX_NAME)

#load, split, embed and upsert documents

def load_vectorstore(uploaded_files):
    embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", output_dimensionality=768)
    file_paths=[]

    #1. Upload
    for file in uploaded_files:
        save_path=Path(UPLOAD_DIR)/file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(save_path)

    #2. Load and split
    for file_path in file_paths:
        loader=PyPDFLoader(str(file_path))
        documents=loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        metadata = []
        for chunk in chunks:
            meta = chunk.metadata.copy()
            meta["text"] = chunk.page_content
            metadata.append(meta)
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        #3. Embedding
        print(f"Embedding and upserting {len(chunks)} chunks from {file_path.name}...")
        embeddings = embed_model.embed_documents(texts)

        #4. Upsert
        print(f"Upserting {len(embeddings)} embeddings to Pinecone index...")
        with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
            index.upsert(vectors=zip(ids, embeddings, metadata))
            progress.update(len(embeddings))
        print(f"Upload Complete for {file_path.name}.")
