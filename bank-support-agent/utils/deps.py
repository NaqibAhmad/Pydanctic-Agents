from dataclasses import dataclass
from database.db import DB

@dataclass
class SupportDeps:
    customer_id: int
    db: DB