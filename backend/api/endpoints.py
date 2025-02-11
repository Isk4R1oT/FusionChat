from fastapi.routing import APIRouter, HTTPException
from backend.services.ChatBot import ChatBot
from backend.models.response_model import QueryRequest

router = APIRouter()
chat_bot = ChatBot()

@router.post('/chat')
async def chat_endpoint(request: QueryRequest):
    try:
        response = chat_bot.process_query(request.query)
        return {'response':response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))