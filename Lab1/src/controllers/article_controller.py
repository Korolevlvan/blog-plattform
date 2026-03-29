from sqlalchemy.orm import Session
from src.models.article import Article
from slugify import slugify

def create_article(db: Session, title, description, body, author_id, tag_list=None):
    slug = slugify(title)
    article = Article(title=title, description=description, body=body, slug=slug, author_id=author_id, tag_list=",".join(tag_list) if tag_list else None)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

def get_articles(db: Session):
    return db.query(Article).all()

def get_article_by_slug(db: Session, slug):
    return db.query(Article).filter(Article.slug == slug).first()

def update_article(db: Session, slug, data):
    article = get_article_by_slug(db, slug)
    if not article:
        return None
    for key, value in data.items():
        setattr(article, key, value)
    db.commit()
    db.refresh(article)
    return article

def delete_article(db: Session, slug):
    article = get_article_by_slug(db, slug)
    if not article:
        return None
    db.delete(article)
    db.commit()
    return article