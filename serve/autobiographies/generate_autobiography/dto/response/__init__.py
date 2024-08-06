from pydantic import BaseModel


class AutobiographyGenerateResponseDto(BaseModel):
    autobiographical_text: str
