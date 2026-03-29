from sqlalchemy.orm import Session
from src.models.comment import Comment

def create_comment(db: Session, article_id, author_id, body):
    comment = Comment(article_id=article_id, author_id=author_id, body=body)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_comments(db: Session, article_id):
    return db.query(Comment).filter(Comment.article_id == article_id).all()

def delete_comment(db: Session, comment_id):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment