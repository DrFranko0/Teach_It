from dataclasses import dataclass
from typing import List

from pydantic_ai import Agent, RunContext
from models.schemas import DebugSuggestion, CodeInstruction, UserRequest
from config import MODEL_NAME

@dataclass
class DebugDependencies:
    request: UserRequest
    instructions: CodeInstruction

debug_agent = Agent(
    MODEL_NAME,
    deps_type=DebugDependencies,
    output_type=List[DebugSuggestion],
    system_prompt=(
        "You are a coding expert specializing in debugging and identifying potential issues. "
        "Review the code instructions and identify common pitfalls, edge cases, or errors that "
        "might occur. Provide helpful suggestions to prevent these issues."
    )
)

@debug_agent.system_prompt
async def add_language_context(ctx: RunContext[DebugDependencies]) -> str:
    language = ctx.deps.request.language or "Python"
    return f"Focus on common issues in {language} code."

async def generate_debug_suggestions(request: UserRequest, instructions: CodeInstruction) -> List[DebugSuggestion]:
    deps = DebugDependencies(request=request, instructions=instructions)
    result = await debug_agent.run(
        f"Identify potential issues and provide debugging tips for this coding task: {instructions.description}",
        deps=deps
    )
    return result.output
