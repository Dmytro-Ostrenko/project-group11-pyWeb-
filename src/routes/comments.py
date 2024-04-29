from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import dependencies, schemas, repository
from .database import get_db

router = APIRouter()

@router.get("/comments/{comment_id}", response_model=schemas.Comment)
def read_comment(comment_id: int, db: Session = Depends(dependencies.get_db)):
    repo = repository.CommentRepository(db)
    db_comment = repo.get_comment_by_id(comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.post("/comments/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(dependencies.get_db)):
    repo = repository.CommentRepository(db)
    return repo.create_comment(comment)

@router.put("/comments/{comment_id}", response_model=schemas.Comment)
def update_comment(
    comment_id: int, 
    comment: schemas.CommentCreate, 
    db: Session = Depends(get_db)
):
    db_comment = db.query(models.Comment).get(comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    for key, value in comment.dict().items():
        setattr(db_comment, key, value)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(dependencies.get_db)):
    repo = repository.CommentRepository(db)
    if not repo.delete_comment(comment_id):
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}