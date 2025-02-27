from typing import List
from pydantic import BaseModel
from .extractable_content_registry import ExtractableContent
from .pydantic_schemas import CandidateSpreadSheet
from .prompts import (
    EXTRACTION_PROMPT,
)

CANDIDATES_EXTRACTION = ExtractableContent(
    type="extract_names_adress",
    prompt=EXTRACTION_PROMPT,
    schema=CandidateSpreadSheet,
)

# add more 
