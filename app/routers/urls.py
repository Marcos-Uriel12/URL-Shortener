from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Url
from app.schemas import UrlCreate, UrlResponse
from app.utils import generate_short_code
from math import ceil
router = APIRouter(tags=["urls"])

@router.get("/urls")
def list_urls(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    total = db.query(Url).count()
    offset = (page - 1) * limit
    urls = db.query(Url).offset(offset).limit(limit).all()
    
    return {
        "urls": urls,
        "total": total,
        "page": page,
        "total_pages": ceil(total / limit),
        "limit": limit
    }

@router.post("/shorten", response_model=UrlResponse, status_code=201)
def shorten_url(url: UrlCreate, db: Session = Depends(get_db)):
    code = generate_short_code()
    while db.query(Url).filter(Url.short_code == code).first():
        code = generate_short_code()
    
    new_url = Url(
        original_url=str(url.original_url),
        short_code=code
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(Url).filter(Url.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    url.clicks += 1
    db.commit()
    return RedirectResponse(url=url.original_url, status_code=302)


@router.get("/stats/{short_code}", response_model=UrlResponse)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    url = db.query(Url).filter(Url.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url


@router.delete("/urls/{short_code}", status_code=204)
def delete_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(Url).filter(Url.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    db.delete(url)
    db.commit()