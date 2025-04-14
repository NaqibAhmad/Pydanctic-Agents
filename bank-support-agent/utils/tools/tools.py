from pydantic_ai import RunContext
from utils.deps import SupportDeps

async def customer_balance_tool(ctx: RunContext[SupportDeps], include_pending: bool) -> str:
    """
    System prompt for the support agent.
    """
    try:
        customer_balance = await ctx.deps.db.customer_balance(id=ctx.deps.customer_id, include_pending=include_pending)
        if customer_balance is None:
            return "Customer not found."
        return f"Customer balance: ${customer_balance:.2f}"
    except ValueError as e:
        return str(e)  # Handle error gracefully and return the error message