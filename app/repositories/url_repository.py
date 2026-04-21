from sqlalchemy.orm import Session
from app.models.models import Url

class UrlRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_short_code(self, short_code: str) -> Url | None:
        return self.db.query(Url).filter(Url.short_code == short_code).first()

    def get_all(self, offset: int, limit: int) -> list[Url]:
        return self.db.query(Url).offset(offset).limit(limit).all()

    def count(self) -> int:
        return self.db.query(Url).count()

    def create(self, original_url: str, short_code: str) -> Url:
        url = Url(original_url=original_url, short_code=short_code)
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    def increment_clicks(self, url: Url) -> None:
        url.clicks += 1
        self.db.commit()

    def delete(self, url: Url) -> None:
        self.db.delete(url)
        self.db.commit()