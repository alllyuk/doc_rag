from pydantic import BaseModel, Field


class ResetChatHistoryInput(BaseModel):
    session_id: str = Field(default=None)


class DocumentInput(BaseModel):
    docs_url: str
    session_id: str = Field(default=None)
    config_path: str = Field(default="config")


class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    config_path: str = Field(default="config")


class QueryResponse(BaseModel):
    answer: str
    session_id: str
