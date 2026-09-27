from fastapi import Query
from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional
from math import ceil

T = TypeVar("T")


class PaginationParams:
    """Dependency for injecting standard pagination query parameters into endpoints."""

    def __init__(
            self,
            page: int = Query(1, ge=1, description="Page number, starting at 1"),
            size: int = Query(20, ge=1, le=100, description="Number of items per page (max 100)")
    ):
        self.page = page
        self.size = size
        self.offset = (page - 1) * size


class PaginatedResponse(BaseModel, Generic[T]):
    """Standardized response structure for paginated lists."""
    items: List[T]
    total: int
    page: int
    size: int
    total_pages: int
    has_next: bool
    has_previous: bool


def paginate_query(query, pagination: PaginationParams):
    """
    Applies offset and limit to a SQLAlchemy query and returns
    the items alongside total count and pagination metadata.
    """
    total = query.count()
    items = query.offset(pagination.offset).limit(pagination.size).all()

    total_pages = ceil(total / pagination.size) if total > 0 else 1

    return {
        "items": items,
        "total": total,
        "page": pagination.page,
        "size": pagination.size,
        "total_pages": total_pages,
        "has_next": pagination.page < total_pages,
        "has_previous": pagination.page > 1
    }