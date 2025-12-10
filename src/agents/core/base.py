from pydantic import BaseModel
from typing import Type, List, Optional, Union, Tuple
from agents.core.models import StringRequest, StringResponse
from agents.providers.bedrock.AnthropicClient import BedrockAnthropicClient
import json


class Agent:
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        request_model: Optional[Type[BaseModel]] = StringRequest,
        instructions: Optional[str] = "You are a helpful assistant.",
        response_model: Optional[Type[BaseModel]] = StringResponse,
        provider: Optional[str] = "bedrock_anthropic",
        model_id: Optional[str] = "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    ):
        self.name = name
        self.description = description
        self.request_model = request_model
        self.instructions = instructions
        self.response_model = response_model
        self.provider = provider
        self.model_id = model_id
        self.client = self.resolve_provider()

    def __repr__(self) -> str:
        return f"Agent(name={self.name}, description={self.description}, request_model={self.request_model.__name__}, response_model={self.response_model.__name__})"

    def resolve_provider(self) -> Union[BedrockAnthropicClient, None]:
        if self.provider == "bedrock_anthropic":
            return BedrockAnthropicClient(model_id=self.model_id)
        else:
            raise ValueError(f"Provider {self.provider} not supported")

    def format_request(self, request: BaseModel) -> Tuple[List[str], List[str]]:
        cached_content = [self.instructions]
        variable_content = [json.dumps(request.model_dump(), indent=2)]
        return cached_content, variable_content

    def run(self, request: BaseModel) -> Tuple[BaseModel, dict]:
        cached_content, variable_content = self.format_request(request)
        response, usage = self.client.query(
            cached_content=cached_content,
            variable_content=variable_content,
            schema=self.response_model,
        )
        return response, usage
