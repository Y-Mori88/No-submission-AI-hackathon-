from pydantic import BaseModel, Field
from typing import Optional

class EligibilityRequest(BaseModel):
    age: int = Field(ge=0, le=130)
    income_yen: int = Field(ge=0)
    household: int = Field(ge=1)
    occupation: str = Field(min_length=1)
    dependents: Optional[int] = Field(default=None, ge=0)
    municipality: Optional[str] = None
