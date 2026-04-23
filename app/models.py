from pydantic import BaseModel, Field, ConfigDict

class MessageRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    message: str
    to: str
    from_: str = Field(..., alias="from")
    timeToLifeSec: int