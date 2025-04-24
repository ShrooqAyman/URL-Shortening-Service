from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import crud, schemas, utils
from .database import SessionLocal, engine
from .models import Base


Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/shorten", response_model=schemas.URLResponse)
def shorten_url(request: schemas.URLRequest, db: Session = Depends(get_db)):
    if not utils.validate_url(request.long_url):
        return schemas.URLResponse(status=400, messages=["Invalid URL"])

    db_url = crud.get_url_by_long(db, request.long_url)
    if db_url:
        return schemas.URLResponse(status=200, short_url=db_url.short_url, long_url=db_url.long_url)

    short = utils.generate_short_hash(request.long_url)
    new_url = crud.create_url(db, request.long_url, short)
    return schemas.URLResponse(status=201, short_url=new_url.short_url, long_url=new_url.long_url)


@router.get("/expand/{short_url}", response_model=schemas.URLResponse)
def expand_url(short_url: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_short(db, short_url)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    crud.increment_visit(db, short_url)
    return schemas.URLResponse(status=200, long_url=db_url.long_url)


@router.delete("/delete/{url}", response_model=schemas.URLResponse)
def delete_url(url: str, db: Session = Depends(get_db)):
    success = crud.delete_url(db, url)
    if not success:
        raise HTTPException(status_code=404, detail="URL not found")
    return schemas.URLResponse(status=200, messages=["URL deleted"])


@router.put("/update/{short_url}", response_model=schemas.URLResponse)
def update_url(short_url: str, request: schemas.URLUpdateRequest, db: Session = Depends(get_db)):
    if not utils.validate_url(request.new_long_url):
        return schemas.URLResponse(status=400, messages=["Invalid new URL"])

    updated = crud.update_long_url(db, short_url, request.new_long_url)
    if not updated:
        raise HTTPException(status_code=404, detail="URL not found")
    return schemas.URLResponse(status=200, short_url=short_url, long_url=updated.long_url)


@router.get("/stats/{short_url}", response_model=schemas.URLStatResponse)
def get_stats(short_url: str, db: Session = Depends(get_db)):
    visits = crud.increment_visit(db, short_url)
    if visits is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return schemas.URLStatResponse(status=200, url=short_url, statistic=visits, messages=[])


@router.get("/{short_url}", response_model=schemas.URLResponse, summary="Get statistics on the short URL (e.g., number of times accessed)")
def redirect_to_long_url(short_url: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_short(db, short_url)
    if db_url:
        crud.increment_visit(db, short_url)
        return RedirectResponse(url=db_url.long_url)
    raise HTTPException(status_code=404, detail="Short URL not found")
