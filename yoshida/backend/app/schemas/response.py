from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Level = Literal["high", "medium", "low", "unknown"]

class Evidence(BaseModel):
    page: int = Field(ge=0)
    source_url: str
    snippet: str

class Reason(BaseModel):
    text: str
    evidence_ref: int = Field(ge=0)

class Deadline(BaseModel):
    date: Optional[str]  # "YYYY-MM-DD" or None
    evidence_ref: Optional[int] = None

class Todo(BaseModel):
    text: str
    evidence_ref: int = Field(ge=0)

class ProgramResult(BaseModel):
    program_id: str
    program_name: str
    level: Level
    confidence: float = Field(ge=0.0, le=1.0)
    reasons: List[Reason]
    deadline: Deadline
    todo: List[Todo]
    evidence: List[Evidence]

class Meta(BaseModel):
    model: str
    version: str

class EligibilityResponse(BaseModel):
    municipality: str
    results: List[ProgramResult]
    meta: Meta
