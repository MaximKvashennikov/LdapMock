from pydantic import BaseModel
from typing import Dict, List

class LdapEntry(BaseModel):
    dn: str
    attributes: Dict[str, List[str] | str]
