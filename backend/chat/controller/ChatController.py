import json

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from chat.service import ChatService
from chat.entity.ChatEntity import ChatEntity
from fastapi import Depends

from common.RolePermission import has_roles

chat_router = APIRouter()

@chat_router.post("/chat")
def chat(chat_entity: ChatEntity, username: dict = Depends(has_roles(["user", "admin"]))):
    def generator():
        for chunk in ChatService.chat(chat_entity.question, chat_entity.historyId,username['username']):
            yield f"data:{json.dumps({'content': chunk})}\n\n"
        yield  f"data:{json.dumps({'content': '[DONE]'})}\n\n"
    return StreamingResponse(
        content=generator(),
        media_type="text/event-stream",
    )
