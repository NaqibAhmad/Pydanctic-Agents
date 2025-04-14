from utils.deps import SupportDeps
from database.db import DB
from utils.agent import support_agent


async def main():
    deps = SupportDeps(customer_id=123, db=DB())
    result = await support_agent.run("What is my balance?", deps=deps)
    print(result.data)


    result = await support_agent.run("I just lost my card", deps=deps)
    print(result.data)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
