from pydantic import BaseModel, Field, field_validator

class BuildRequest(BaseModel):
    path: str

class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)
    literal_filter: str | None = Field(default=None, max_length=120)
    @field_validator("query")
    @classmethod
    def query_must_contain_text(cls, value):
        if not value.strip(): raise ValueError("Query cannot be empty")
        return value.strip()

    @field_validator("literal_filter")
    @classmethod
    def clean_literal_filter(cls, value):
        return value.strip() if value and value.strip() else None
