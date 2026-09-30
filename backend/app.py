from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.routes.alert_routes import router as alert_router
from backend.routes.device_routes import router as device_router
from backend.routes.sensor_routes import router as sensor_router
from backend.routes.watering_routes import router as watering_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Cloud-Connected Smart Plant Care API",
    description=(
        "Backend API for virtual IoT plant monitoring, "
        "automatic watering, alerts, and device management."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# API ROUTES
# ---------------------------------------------------------

app.include_router(sensor_router)
app.include_router(device_router)
app.include_router(watering_router)
app.include_router(alert_router)


# ---------------------------------------------------------
# BASIC ENDPOINTS
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Cloud-Connected Smart Plant Care API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
    }