from fastapi import FastAPI, Depends, Header, HTTPException
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sameera-db.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"status": "online", "message": "Security Guard is Live!"}

# --- THE FIX: convert_underscores=False ---
@app.get("/notes")
def get_notes(
    # We set convert_underscores=False so it looks for 'user_id' exactly
    user_id: str = Header(None, convert_underscores=False), 
    db: Session = Depends(get_db)
):
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="The security guard returned: User ID header missing"
        )

    notes = db.query(models.Note).filter(models.Note.user_id == user_id).all()
    return notes

@app.post("/notes")
def create_note(
    title: str, 
    user_id: str = Header(..., convert_underscores=False), 
    db: Session = Depends(get_db)
):
    new_note = models.Note(title=title, user_id=user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note
