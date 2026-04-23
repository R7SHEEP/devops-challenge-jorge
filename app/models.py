from pydantic import BaseModel, Field
 
 
class MessageRequest(BaseModel):
    message: str
    to: str
    from_: str = Field(..., alias="from")
    timeToLifeSec: int
 
    class Config:
        populate_by_name = True
 