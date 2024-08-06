from pydantic import BaseModel


class ProofreadingRequestDto(BaseModel):
    content: str
