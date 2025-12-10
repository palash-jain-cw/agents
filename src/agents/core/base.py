from pydantic import BaseModel
from typing import Type, List, Optional
from agents.core.models import StringRequest, StringResponse


class Agent:
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        request_model: Optional[Type[BaseModel]] = StringRequest,
        instructions: Optional[str] = "You are a helpful assistant.",
        response_model: Optional[Type[BaseModel]] = StringResponse,
    ):
        self.name = name
        self.description = description
        self.request_model = request_model
        self.instructions = instructions
        self.response_model = response_model

    def run(self, request: BaseModel) -> BaseModel:
        pass
