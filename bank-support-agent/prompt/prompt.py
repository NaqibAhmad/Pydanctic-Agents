from pydantic_ai import RunContext
from utils.deps import SupportDeps

async def add_customer_name(ctx: RunContext[SupportDeps]) -> str:
    """
    System prompt for the support agent.
    """
    customer_name = await ctx.deps.db.customer_name(id=ctx.deps.customer_id)
    if customer_name is None:
        return "Customer not found."
    return f"The customer's name is: {customer_name}"