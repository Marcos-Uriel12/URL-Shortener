from sqlalchemy.orm import Session
from app.repositories.url_repository import UrlRepository
from app.utils import generate_short_code
from math import ceil

class UrlService:
    def __init__(self, db: Session):
        self.repo = UrlRepository(db)

    def create_short_url(self, original_url: str):
        code = generate_short_code()
        while self.repo.get_by_short_code(code):
            code = generate_short_code()
        return self.repo.create(original_url, code)

    def get_by_short_code(self, short_code: str):
        return self.repo.get_by_short_code(short_code)

    def increment_clicks(self, short_code: str):
        url = self.repo.get_by_short_code(short_code)
        if url:
            self.repo.increment_clicks(url)
        return url

    def get_all(self, page: int, limit: int):
        total = self.repo.count()
        offset = (page - 1) * limit
        urls = self.repo.get_all(offset, limit)
        return {
            "urls": urls,
            "total": total,
            "page": page,
            "total_pages": ceil(total / limit),
            "limit": limit
        }

    def delete(self, short_code: str):
        url = self.repo.get_by_short_code(short_code)
        if url:
            self.repo.delete(url)
        return url