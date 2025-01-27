from typing import List, Optional

from pydantic import BaseModel



class ServiceItem(BaseModel):
    id: int
    title: str
    price: str
    warning: Optional[str] = None


class Services(BaseModel):
   services: List[ServiceItem]
   balance: str