from models.schemas import InstructionResult, UserRequest
from agents.instruction_agent import generate_instructions
from agents.reference_agent import find_references
from agents.debug_agent import generate_debug_suggestions

async def orchestrate_instruction_generation(request: UserRequest) -> InstructionResult:
    instructions = await generate_instructions(request)
    
    references = await find_references(request, instructions)
    
    debug_suggestions = await generate_debug_suggestions(request, instructions)
    
    summary = f"Generated {len(instructions.steps)} steps for {request.task_description} in {request.language}"
    
    return InstructionResult(
        instructions=instructions,
        references=references,
        debug_suggestions=debug_suggestions,
        summary=summary
    )
