from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.rag_service import generate_embedding_service
from app.router.rag_router import router as rag_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Called automatically FIRST on server startup
    generate_embedding_service()
    yield

app = FastAPI(title="RAG Service API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Allows your Next.js frontend
    allow_credentials=True,
    allow_methods=["*"], # Allows POST, GET, OPTIONS, etc.
    allow_headers=["*"], # Allows all headers
)

# Register endpoint route
app.include_router(rag_router)
