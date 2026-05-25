from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import Base, engine
from app.routers import categories, comments, locations, posts, users, auth
from app.core.exceptions import AppException
from app.api.error_handler import handle_domain_exception

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI API",
    description=(
        "REST API на FastAPI, воспроизводящий модели Django-блога "
        "(спринты 1–8): Category, Location, Post, Comment, User."
    ),
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(locations.router)
app.include_router(posts.router)
app.include_router(comments.router)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    response = handle_domain_exception(exc)
    return JSONResponse(
        status_code=response.status_code,
        content={"detail": response.detail}
    )

@app.get("/", tags=["Root"], summary="Корневой эндпоинт")
def root():
    return {
        "message": "Blogicum FastAPI работает!",
        "docs": "/docs",
        "redoc": "/redoc",
    }