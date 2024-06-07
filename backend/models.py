from pydantic import BaseModel


class Translation(BaseModel):
    """Request format"""

    page: str
