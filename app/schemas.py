from pydantic import BaseModel, HttpUrl

class URLRequest(BaseModel):
    long_url: HttpUrl

class URLUpdateRequest(BaseModel):
    new_long_url: HttpUrl

class URLResponse(BaseModel):
    status: int
    long_url: str = None
    short_url: str = None
    messages: list[str] = []

class URLStatResponse(BaseModel):
    status: int
    url: str
    statistic: int
    messages: list[str] = []