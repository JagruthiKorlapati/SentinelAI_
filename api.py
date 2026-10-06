from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from orchestrator import analyse_incident
from scenarios import SCENARIOS

app = FastAPI(title="Cyber Incident Agents API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class IncidentRequest(BaseModel):
    text: str = Field(default="", max_length=2000)
    use_llm: bool = True


@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/scenarios")
def list_scenarios():
    return SCENARIOS


@app.post("/analyze")
def analyze(req: IncidentRequest):
    return analyse_incident(req.text, use_llm=req.use_llm)