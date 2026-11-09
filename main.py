from pathlib import Path
from fastapi import FastAPI
from database import engine, Base
import models
from routers import (
    auth,
    notes,
    admin)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

#Before creating app, we need to create our db.
#this looks at models that are inherited from base and creates tables if they doesnt exist.
# it is safe to run multiple times.
Base.metadata.create_all(bind=engine)


# INITIALIZE app

app = FastAPI(
    title="Secure Notes API",
    description="A secure notes management application",
    version="1.0"
)


BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# REGISTER ROUTERS
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(admin.router)


# HOME ROUTE
@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}