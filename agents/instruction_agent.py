from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from models.schemas import CodeInstruction, UserRequest
from config import model

@dataclass
class InstructionDependencies:
    request: UserRequest

instruction_agent = Agent(
    model,
    deps_type=InstructionDependencies,
    output_type=CodeInstruction,
    system_prompt=(
        "You are an expert coding instructor that generates clear, step-by-step instructions "
        "for completing coding tasks. Your instructions should be detailed enough for a programmer "
        "to follow, with code examples for each step. Focus on best practices and clarity."
    )
)

@instruction_agent.system_prompt
async def add_language_context(ctx: RunContext[InstructionDependencies]) -> str:
    language = ctx.deps.request.language or "Python"
    return f"The user is working with {language}. Provide code examples in {language}."

@instruction_agent.system_prompt
async def add_complexity_context(ctx: RunContext[InstructionDependencies]) -> str:
    complexity = ctx.deps.request.complexity or "intermediate"
    return f"The user's skill level is {complexity}. Adjust your instructions accordingly."

async def generate_instructions(request: UserRequest) -> CodeInstruction:
    deps = InstructionDependencies(request=request)
    result = await instruction_agent.run(
        f"Generate step-by-step instructions for: {request.task_description}",
        deps=deps
    )
    return result.output
