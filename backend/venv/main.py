from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, IPvAnyAddress
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import asyncio

# --- 1. Zero Trust Security ---
API_KEY = "sentinel-secret-123"
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Zero Trust: Password Thappu! Access Denied.")
    return api_key

# --- 2. ORM & Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./incidents.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class IncidentDB(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)
    attack_type = Column(String)
    confidence_score = Column(Float) 
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. Strict Schema Validators & JSON Schema ---
class Incident(BaseModel):
    ip_address: IPvAnyAddress 
    attack_type: str = Field(..., min_length=3, max_length=50)
    confidence_score: float = Field(..., ge=0.0, le=100.0) 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Async Logic (M2 agent timeout check kosam time pencahmu) ---
async def m2_classify(attack):
    # Ekkada time kavalani 5 seconds pettam timeout test cheyadaniki
    await asyncio.sleep(5) 
    if attack == "Malware" or attack == "Hacker": return True
    return False

# --- 4. API Versioning (v1) ---
@app.post("/api/v1/incidents")
async def receive_incident(data: Incident, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    ip_str = str(data.ip_address)
    
    try:
        # Time-bound Fail-safes (3 seconds lopu answer ravali)
        is_danger = await asyncio.wait_for(m2_classify(data.attack_type), timeout=3.0)
        final_status = "Pending Approval" if is_danger else "Allowed"
    except asyncio.TimeoutError:
        # Fallback Policy / Investigatory Mode (Time out aithe attack miss avvakunda save chesthundi)
        final_status = "Investigatory Mode (Timeout)"
        
    # Immutability: Okkasari save ayyaka delete avvadu
    new_incident = IncidentDB(
        ip_address=ip_str, 
        attack_type=data.attack_type, 
        confidence_score=data.confidence_score,
        status=final_status
    )
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    return {"saved_id": new_incident.id, "status": final_status, "confidence": data.confidence_score}

# --- 5. Maker-Checker Policy ---
@app.post("/api/v1/incidents/{incident_id}/approve")
async def approve_incident(incident_id: int, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    incident = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
    if not incident: raise HTTPException(status_code=404, detail="Not Found")
    incident.status = "Approved & Blocked"
    db.commit()
    return {"message": "Admin approved (Maker-Checker)", "status": incident.status}

@app.post("/api/v1/incidents/{incident_id}/reject")
async def reject_incident(incident_id: int, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    incident = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
    if not incident: raise HTTPException(status_code=404, detail="Not Found")
    incident.status = "Rejected (Not Blocked)"
    db.commit()
    return {"message": "Admin rejected (Maker-Checker)", "status": incident.status}

@app.get("/api/v1/incidents/history")
async def get_history(db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    all_incidents = db.query(IncidentDB).all()
    history_list = [{"id": i.id, "ip_address": i.ip_address, "attack_type": i.attack_type, "confidence": i.confidence_score, "status": i.status, "time": i.created_at} for i in all_incidents]
    return {"total_attacks": len(all_incidents), "history": history_list}