import os
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import doctors, appointments
from app.websocket import ws_manager

# Ensure database tables exist (also managed via Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare Appointment Booking System",
    description=(
        "API for patients to book appointments with doctors with working hours validation "
        "and double-booking prevention."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    servers=[
        {"url": "http://localhost:8000", "description": "Local Healthcare API server"}
    ]
)

# CORS middleware for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(doctors.router)
app.include_router(appointments.router)


@app.get("/", tags=["health"], summary="Health check and service status")
def root():
    return {
        "status": "healthy",
        "service": "Healthcare Appointment Booking System",
        "documentation": "/docs",
        "openapi_spec": "/openapi.json"
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time booking and cancellation updates."""
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive; clients can also send ping
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception:
        ws_manager.disconnect(websocket)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    print(f"Starting Healthcare API server on http://localhost:{port} ...")
    uvicorn.run("main:app", host=host, port=port, reload=False)
