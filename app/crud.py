from sqlalchemy.orm import Session
from app import models


def get_url_by_long(db: Session, long_url):
    url_str = str(long_url)
    return db.query(models.URL).filter(models.URL.long_url == url_str).first()


def get_url_by_short(db: Session, short_url):
    code_str = str(short_url)
    return db.query(models.URL).filter(models.URL.short_url == code_str).first()


def create_url(db: Session, long_url, short_url):
    long_url_str = str(long_url)
    short_url_str = str(short_url)
    db_url = models.URL(long_url=long_url_str, short_url=short_url_str)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def delete_url(db: Session, url):
    url_str = str(url)
    record = db.query(models.URL).filter(
        (models.URL.short_url == url_str) |
        (models.URL.long_url == url_str)
    ).first()
    if record:
        db.delete(record)
        db.commit()
        return True
    return False


def update_long_url(db: Session, short_url, new_long_url):
    code_str = str(short_url)
    new_long_url_str = str(new_long_url)
    record = db.query(models.URL).filter(models.URL.short_url == code_str).first()
    if record:
        record.long_url = new_long_url_str
        db.commit()
        db.refresh(record)
        return record
    return None


def increment_visit(db: Session, short_url):
    code_str = str(short_url)
    record = db.query(models.URL).filter(models.URL.short_url == code_str).first()
    if record:
        record.visits += 1
        db.commit()
        return record.visits
    return None
