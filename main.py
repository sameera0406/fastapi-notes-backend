from fastapi import FastAPI, Depends, Header
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

# This line MUST exist and be named 'app'
app = FastAPI()

# This creates the tables in Supabase automatically
models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- THE "ONLY MY NOTES" LOGIC ---

@app.get("/notes")
def get_notes(user_id: str = Header(None), db: Session = Depends(get_db)):
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID missing in headers")
    
    # This is the "Privacy Lock"
    # It ensures the database only returns rows matching this specific UUID
    notes = db.query(models.Note).filter(models.Note.user_id == user_id).all()
    return notes

@app.post("/notes")
def create_note(title: str, user_id: str = Header(...), db: Session = Depends(get_db)):
    # This 'stamps' the note with the user's ID in the DB
    new_note = models.Note(title=title, user_id=user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)
