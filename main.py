from fastapi import FastAPI
from database import engine, Base
from app.routes import chat_routes, metrics_routes, health_route
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_routes.router, prefix="/api")
app.include_router(metrics_routes.router)
app.include_router(health_route.router)
