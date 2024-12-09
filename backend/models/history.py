from pydantic import BaseModel

class History(BaseModel):
    """
    A model representing a single history record.
    """
    id: str
    original: str
    processed: str
