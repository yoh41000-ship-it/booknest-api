# app/core/dependencies.py
from fastapi import Query


class Pagination:
    def __init__(self, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
        self.page = page
        self.size = size
        self.offset = (page - 1) * size