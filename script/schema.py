from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Define the Attachment schema
class Attachment(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    service: str
    company: str
    pricing_table: dict
    date_signature: datetime
    date_created: datetime
    date_expiration: datetime

# Define the RepairShop schema
class RepairShop(BaseModel):
    repair_shop_name: str
    repair_shop_p_iva: str
    repair_shop_address: str
    attachments: List[Attachment]


