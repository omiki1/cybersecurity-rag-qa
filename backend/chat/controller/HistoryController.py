from fastapi import APIRouter,Depends


from chat.dao import HistoryDao, ChatDao
from chat.entity.ConversationResultEntity import ConversationResultEntity
from chat.service import HistoryService
from common.RolePermission import has_roles

history_router = APIRouter()
@history_router.get(
    path="/queryHistoryMenu",
    summary='查询历史记录',
)
# def query_history_menu(username:str,user: dict = Depends(has_roles(["user", "admin"]))):
def query_history_menu(user: dict = Depends(has_roles(["user", "admin"]))):
    return HistoryService.query_history_menu(user['username'])
@history_router.get(
    path="/conversationLog",
)
def conversation_log(historyId:int,user: dict = Depends(has_roles(["user", "admin"]))):
    return HistoryService.conversation_log(historyId)
@history_router.get("/deleteConversationResult")
def delete_conversation_result(historyId: int,user: dict = Depends(has_roles(["user", "admin"]))):
    return HistoryService.deleteConversation(historyId)
@history_router.post("/saveConversationResult")
def save_conversation_result(conversationResultEntity:ConversationResultEntity,user: dict = Depends(has_roles(["user", "admin"]))):
    return HistoryService.save_conversation_result(conversationResultEntity)