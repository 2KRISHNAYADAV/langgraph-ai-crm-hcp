from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database.database import SessionLocal
from database import crud
from agent.graph import process_chat

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class InteractionSchema(BaseModel):
    hcp_name: Optional[str] = ""
    date: Optional[str] = ""
    product: Optional[str] = ""
    notes: Optional[str] = ""
    sentiment: Optional[str] = ""
    follow_up: Optional[str] = ""

class ChatRequest(BaseModel):
    message: str
    form_state: InteractionSchema

@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    return process_chat(req.message, req.form_state.dict())

@router.post("/save")
def save_interaction(interaction: InteractionSchema, db: Session = Depends(get_db)):
    db_item = crud.create_interaction(db, interaction.dict())
    return {"status": "success", "id": db_item.id}

@router.get("/interactions")
def get_interactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_interactions(db, skip=skip, limit=limit)

@router.put("/edit/{interaction_id}")
def edit_interaction(interaction_id: int, interaction: InteractionSchema, db: Session = Depends(get_db)):
    db_item = crud.update_interaction(db, interaction_id, interaction.dict())
    if db_item is None:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "success", "id": db_item.id}
