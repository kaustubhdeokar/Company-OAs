from pydantic import BaseModel

class PageRange(BaseModel):
    from_page: int
    to_page: int