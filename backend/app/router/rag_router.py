from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.rag_service import query_rag_service

# 1. Define input/output structures right here (No separate schema file needed)
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class QueryResponse(BaseModel):
    query: str
    answer: str

# Define the router
router = APIRouter(prefix="/api/v1/rag", tags=["RAG"])

@router.post("/query", response_model=QueryResponse)
def handle_query(request: QueryRequest):
    try:
        answer = query_rag_service(query=request.query, top_k=request.top_k)
        return QueryResponse(query=request.query, answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))