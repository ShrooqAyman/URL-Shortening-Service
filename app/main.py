from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.database import Base, engine
from app.views import router

# Create database tables
Base.metadata.create_all(bind=engine)
app = FastAPI(title="URL Shortener API")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

app.include_router(router)
