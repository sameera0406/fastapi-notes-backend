from fastapi import FastAPI, Depends, Header,HTTPException
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

# This line MUST exist and be named 'app'
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sameera-db.vercel.app/"], # Replace with your actual Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This creates the tables in Supabase automatically
models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- THE "ONLY MY NOTES" LOGIC ---
@app.get("/")
def home():
    return {"message": "Security Guard is Live!"}
@app.get("/notes")
# By using Header(alias="user_id"), we tell FastAPI exactly what to look for
async def get_notes(user_id: Optional[str] = Header(None, alias="user_id")):
    if not user_id:
        return {"detail": "User ID missing in headers"}
    
    # Debugging: This will show up in your Render Logs
    print(f"Received request for User: {user_id}")
    
    # Your logic to fetch from Supabase...
    return []

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
