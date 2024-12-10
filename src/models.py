from pydantic import BaseModel
from typing import List

class DocumentPayload(BaseModel):
    payload: str | List[str]