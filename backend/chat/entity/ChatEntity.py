from pydantic import BaseModel


class ChatEntity(BaseModel):
    question: str
    historyId: int
