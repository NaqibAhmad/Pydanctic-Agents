

class DB:
    """
    Fake database for example purpose
    """
    @classmethod
    async def customer_name(cls,*, id: int) -> str | None:
        if id == 123:
            return "John Doe"
        
    @classmethod
    async def customer_balance(cls,*, id: int, include_pending: bool) -> float | None:
        if id == 123 and include_pending:
            return 1000.0
        else:
            raise ValueError("Customer not found or invalid parameters")
        

        