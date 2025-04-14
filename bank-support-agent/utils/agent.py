from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from utils.deps import SupportDeps
from prompt.prompt import add_customer_name
import logfire
from utils.tools.tools import customer_balance_tool

logfire.configure()
class SupportResult(BaseModel):
    """
    A class representing the result of a support agent's response.
    """
    support_advice: str = Field(..., description="The advice provided by the support agent to the customer.")
    block_card: bool = Field(..., description="Indicates whether the customer's card should be blocked or not.")
    risk: int = Field(..., description="The risk level associated with the customer's request.", ge=0, le=10)

support_agent = Agent(
    model="gpt-4o",
    deps_type=SupportDeps,
    result_type = SupportResult,
    instrument=True,
    system_prompt="""
    You are a bank support agent. Your task is to assist customers with their banking inquiries.
    Reply using the customer's name and provide a clear and concise response to their request.
    """
)

support_agent.system_prompt(add_customer_name)
support_agent.tool(customer_balance_tool)

