from typing import List, Optional
from pydantic import BaseModel, Field

class CodeInstruction(BaseModel):
    description: str = Field(description="Brief description of what the code does")
    steps: List[str] = Field(description="Ordered list of implementation steps")
    code_snippets: List[str] = Field(description="Code examples for each step")

class Reference(BaseModel):
    title: str = Field(description="Title of the reference")
    url: Optional[str] = Field(description="URL of the documentation if available")
    content: str = Field(description="Relevant content from the documentation")

class DebugSuggestion(BaseModel):
    issue: str = Field(description="Identified potential issue")
    solution: str = Field(description="Proposed solution")
    explanation: str = Field(description="Explanation of why this might happen")

class InstructionResult(BaseModel):
    instructions: CodeInstruction
    references: List[Reference] = Field(default_factory=list)
    debug_suggestions: List[DebugSuggestion] = Field(default_factory=list)
    summary: str = Field(description="Brief summary of the implementation")

class UserRequest(BaseModel):
    task_description: str = Field(description="Natural language description of the coding task")
    language: str = Field(default="Python", description="Programming language")
    complexity: str = Field(default="intermediate", description="Expected complexity level")
