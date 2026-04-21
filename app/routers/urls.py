from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UrlCreate, UrlResponse
from app.services.url_services import UrlService

router = APIRouter(tags=["urls"])

@router.post("/shorten", response_model=UrlResponse, status_code=201)
def shorten_url(url: UrlCreate, db: Session = Depends(get_db)):
    service = UrlService(db)
    return service.create_short_url(str(url.original_url))

@router.get("/urls")
def list_urls(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    service = UrlService(db)
    return service.get_all(page, limit)

@router.get("/stats/{short_code}", response_model=UrlResponse)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    service = UrlService(db)
    url = service.get_by_short_code(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    service = UrlService(db)
    url = service.increment_clicks(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=url.original_url, status_code=302)

@router.delete("/urls/{short_code}", status_code=204)
def delete_url(short_code: str, db: Session = Depends(get_db)):
    service = UrlService(db)
    url = service.delete(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")