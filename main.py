from fastapi import FastAPI
import os
import uvicorn
from database import engine, Base
from app.routes import chat_routes, metrics_routes, health_route
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_routes.router, prefix="/api")
app.include_router(metrics_routes.router)
app.include_router(health_route.router)

# Run the app with uvicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)