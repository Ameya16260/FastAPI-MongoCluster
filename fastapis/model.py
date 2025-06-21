from pydantic import BaseModel
from typing import Optional

class Password(BaseModel):
    name: Optional[str] = None
    url: str
    desc: Optional[str] = None
    password: Optional[str] = None