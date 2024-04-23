from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from mangum import Mangum

# Router imports
from backend.routers.chats import chats_router
from backend.routers.users import users_router
from backend.auth import auth_router
from backend.models.exception import EntityNotFoundException, DuplicateEntityException
from backend.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
	title="Pony Express API",
	description="API for chat application",
    lifespan=lifespan,
)

lambda_handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://nn9l8p1ybb.execute-api.us-east-2.amazonaws.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router list
app.include_router(chats_router)
app.include_router(users_router)
app.include_router(auth_router)

# Setup exception stuff
@app.exception_handler(EntityNotFoundException)
def handle_entity_not_found(
    _request: Request,
    exception: EntityNotFoundException,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": {
                "type": "entity_not_found",
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )

@app.exception_handler(DuplicateEntityException)
def handle_duplicate_entity(
    _request: Request,
    exception: DuplicateEntityException,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "type": "duplicate_entity",
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )