#import datetime
from pydantic import BaseModel


class TodoSchema(BaseModel):
    id: int
    name: str
    description: str
    status: any
    #created_at: Optional[datetime]
    #closed_at: Optional[datetime]

    class Config:
        from_attributes = True