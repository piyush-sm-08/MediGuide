from fastapi import APIRouter, Depends
from pydantic import BaseModel

from auth.routes import authentication
from chat.chat_query import answer_query

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/")
def chat(
    req: ChatRequest,
    user=Depends(authentication)
):
    return answer_query(
        query=req.query,
        top_k=req.top_k,
        role=user["role"]
    )
