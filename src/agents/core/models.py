from pydantic import BaseModel, Field


class StringRequest(BaseModel):
    request: str = Field(description="The request to the agent.")

class StringResponse(BaseModel):
    response: str = Field(description="The response to the user's request.")