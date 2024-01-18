from fastapi import FastAPI

app = FastAPI(
	title="Pony Express API",
	description="API for chat application",
)

app.include_router()