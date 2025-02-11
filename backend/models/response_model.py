from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    api_key: str
