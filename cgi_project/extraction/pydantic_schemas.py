from typing import List, Literal, Optional
from pydantic import BaseModel

class Candidate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    adress: Optional[str]

class CandidateSpreadSheet(BaseModel):
    candidates: List[Candidate]