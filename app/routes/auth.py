from fastapi import APIRouter, Depends, HTTPException,Response
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import SessionLocal
from app import models, schemas, utils
from app.utils import decode_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user_data.password)
    user = models.User(username=user_data.username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

@router.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
     user = db.query(models.User).filter(models.User.username == form_data.username).first()
     if not user or not utils.verify_password(form_data.password, user.password):
         raise HTTPException(status_code=400, detail="Invalid credentials")

     access_token = utils.create_access_token({"sub": user.username}, timedelta(minutes=30))

     # ✅ Debugging print statement to confirm token generation
     print(f"Generated Token: {access_token}")

     # ✅ Set HTTP-only cookie (remove "Bearer ")
     response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,  # Prevents JavaScript access for security
        secure=True,    # Use `True` in production (requires HTTPS)
        samesite="None"  # Adjust depending on your needs
     )

     # ✅ Debugging: Print response headers to verify if the cookie is set
     print(f"Response Headers: {response.headers}")

     return {
         "access_token": access_token,  # Still return token in response
         "user": {"id": user.id, "username": user.username}
     }