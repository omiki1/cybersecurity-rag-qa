from pydantic import BaseModel, Field


class ConversationResultEntity(BaseModel):
    question: str = Field(..., description="问题")
    username: str = Field(..., description="用户名")
    parentId: int = Field(..., description="父会话 id（0 表示新会话第一问）")
    answer: str = Field(..., description="回答")