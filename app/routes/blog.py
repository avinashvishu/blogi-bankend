from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from app.routes.auth import oauth2_scheme
from app.utils import decode_access_token
from fastapi import Query


router = APIRouter(prefix="/posts", tags=["Posts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Fetches the current user from JWT token."""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.username == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/")
def create_post(post_data: schemas.PostCreate, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Creates a new blog post."""
    post = models.Post(title=post_data.title, content=post_data.content, user_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# @router.get("/")
# def get_posts(db: Session = Depends(get_db)):
#     """Fetches all blog posts."""
#     return db.query(models.Post).all()

@router.get("/")
def get_posts(
    db: Session = Depends(get_db),
    page: int = Query(1, alias="page", ge=1),
    limit: int = Query(10, alias="limit", le=50),
    search: str = Query(None, alias="search")
):
    """Fetches blog posts with pagination, search, and includes username."""
    query = db.query(models.Post).outerjoin(models.User).add_columns(
        models.Post.id, models.Post.title, models.Post.content, models.Post.user_id, models.User.username
    )

    if search:
        query = query.filter(models.Post.title.ilike(f"%{search}%"))

    total_posts = query.count()  # Get total count for frontend pagination

    posts = query.offset((page - 1) * limit).limit(limit).all()

    # ✅ Format the response to include username
    formatted_posts = [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
            "username": username  # Include username
        }
        for post, username in posts
    ]

    return {"posts": formatted_posts, "totalPages": (total_posts // limit) + (1 if total_posts % limit else 0)}


@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Fetches a single blog post by ID."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}")
def update_post(post_id: int, post_data: schemas.PostCreate, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Updates a blog post."""
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.user_id == user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    
    post.title = post_data.title
    post.content = post_data.content
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}")
def delete_post(post_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Deletes a blog post."""
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.user_id == user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}
