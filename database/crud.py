from sqlalchemy.orm import Session
from database import models

def get_interactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Interaction).offset(skip).limit(limit).all()

def create_interaction(db: Session, interaction_data: dict):
    db_interaction = models.Interaction(**interaction_data)
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

def update_interaction(db: Session, interaction_id: int, interaction_data: dict):
    db_interaction = db.query(models.Interaction).filter(models.Interaction.id == interaction_id).first()
    if db_interaction:
        for key, value in interaction_data.items():
            setattr(db_interaction, key, value)
        db.commit()
        db.refresh(db_interaction)
    return db_interaction
