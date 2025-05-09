from dataclasses import dataclass
from typing import List

from pydantic_ai import Agent, RunContext, Tool
from models.schemas import Reference, CodeInstruction, UserRequest
from config import model

@dataclass
class ReferenceDependencies:
    request: UserRequest
    instructions: CodeInstruction

reference_agent = Agent(
    model,
    deps_type=ReferenceDependencies,
    output_type=List[Reference],
    system_prompt=(
        "You are a technical documentation specialist. Your task is to find relevant "
        "documentation and sources that support the implementation of a coding task. "
        "Provide references that help understand the concepts and techniques used in the solution."
    )
)

@reference_agent.tool
async def search_documentation(ctx: RunContext[ReferenceDependencies], query: str) -> str:
    language = ctx.deps.request.language.lower()
    
    if "python" in language:
        if "flask" in query.lower():
            return "Flask Documentation: https://flask.palletsprojects.com/ - Flask is a lightweight WSGI web application framework in Python."
        elif "django" in query.lower():
            return "Django Documentation: https://docs.djangoproject.com/ - Django is a high-level Python web framework that encourages rapid development."
        else:
            return f"Python Documentation: https://docs.python.org/ - Official documentation for Python {language}."
    elif "javascript" in language:
        return "JavaScript MDN Documentation: https://developer.mozilla.org/en-US/docs/Web/JavaScript - The MDN Web Docs site provides information about JavaScript."
    else:
        return f"Documentation for {language}: Please refer to the official {language} documentation."

async def find_references(request: UserRequest, instructions: CodeInstruction) -> List[Reference]:
    deps = ReferenceDependencies(request=request, instructions=instructions)
    result = await reference_agent.run(
        f"Find documentation references for: {request.task_description} in {request.language}",
        deps=deps
    )
    return result.output
