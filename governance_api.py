"""Adds POST /govern: M1 agents -> governance assessment -> M3 decision."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from governance.pipeline import run_pipeline

router = APIRouter()


class GovernRequest(BaseModel):
    text: str = Field(default="", max_length=2000)
    use_llm: bool = True


@router.post("/govern")
def govern(req: GovernRequest):
    if not req.text.strip():
        raise HTTPException(status_code=422, detail="text must not be empty")
    return run_pipeline(req.text, use_llm=req.use_llm)