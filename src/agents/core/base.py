from pydantic import BaseModel
from typing import Type, List, Optional, Union, Tuple
from agents.core.models import StringRequest, StringResponse, StringFeedback, Draft
from agents.providers.bedrock.AnthropicClient import BedrockAnthropicClient
import json
import uuid


class SingleTurnAgent:
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        request_model: Optional[Type[BaseModel]] = StringRequest,
        instructions: Optional[str] = "You are a helpful assistant.",
        response_model: Optional[Type[BaseModel]] = StringResponse,
        feedback_model: Optional[Type[BaseModel]] = StringFeedback,
        provider: Optional[str] = "bedrock_anthropic",
        model_id: Optional[str] = "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    ):
        self.name = name
        self.description = description
        self.request_model = request_model
        self.instructions = instructions
        self.response_model = response_model
        self.feedback_model = feedback_model
        self.provider = provider
        self.model_id = model_id
        self.drafts: List[Draft] = []
        self.trajectory_id: str = str(uuid.uuid4())
        self.client = self.resolve_provider()

    def __repr__(self) -> str:
        return f"Agent(name={self.name}, description={self.description}, request_model={self.request_model.__name__}, response_model={self.response_model.__name__})"

    def resolve_provider(self) -> Union[BedrockAnthropicClient, None]:
        if self.provider == "bedrock_anthropic":
            return BedrockAnthropicClient(model_id=self.model_id)
        else:
            raise ValueError(f"Provider {self.provider} not supported")

    def format_previous_draft(self, previous_draft: Draft) -> str:
        feedback_text = f"""

        Here is the previous attempt at generating the response:

        {json.dumps(previous_draft.draft.model_dump(), indent=2)}

        Here is the feedback for the previous attempt:

        {json.dumps(previous_draft.feedback.model_dump(), indent=2)}

        """
        return feedback_text

    def format_request(
        self, request: BaseModel, previous_draft: Optional[Draft] = None
    ) -> Tuple[List[str], List[str]]:
        cached_content = [self.instructions]
        variable_content = [json.dumps(request.model_dump(), indent=2)]
        if previous_draft is not None:
            variable_content.append(self.format_previous_draft(previous_draft))
        return cached_content, variable_content

    def run(self, request: BaseModel, previous_draft: Optional[Draft] = None) -> Draft:
        cached_content, variable_content = self.format_request(request, previous_draft)
        response, usage = self.client.query(
            cached_content=cached_content,
            variable_content=variable_content,
            schema=self.response_model,
        )
        draft = Draft(
            draft=response, feedback=None, usage=usage, trajectory_id=self.trajectory_id
        )
        self.drafts.append(draft)
        return draft

    def reject_draft(self, draft_id: str, feedback: BaseModel) -> Draft:
        draft = next((d for d in self.drafts if d.id == draft_id), None)
        if draft is None:
            raise ValueError(f"Draft with id {draft_id} not found")
        draft.feedback = feedback
        return draft
