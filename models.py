from pydantic import BaseModel

class Translation(BaseModel):
    """request format"""
    page: str
