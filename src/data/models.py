from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Tuple


class LdapEntry(BaseModel):
    dn: str
    attributes: Dict[str, List[str] | str]


class LdapModifyRequest(BaseModel):
    """
    Модель для изменения LDAP-записи.
    Формат: {"attribute_name": [[операция, [значения]]}
    """
    attributes: Dict[
        str, List[
            Tuple[Literal["MODIFY_REPLACE", "MODIFY_ADD", "MODIFY_DELETE"], List[str]]
        ]
    ] = Field(
        examples=[
            {
                "sn": [["MODIFY_REPLACE", ["New Name"]]],
                "telephoneNumber": [["MODIFY_ADD", ["+1234567890"]]]
            }
        ],
        description="Словарь атрибутов и операций для модификации"
    )
