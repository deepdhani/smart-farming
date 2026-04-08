# main.py — Smart Farming Assistant
# FastAPI serves both the API and the React frontend build

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn
import os

from config.database import connect_db, disconnect_db
from routes import auth, weather, crops, disease, soil, irrigation, market, alerts


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()


app = FastAPI(
    title="Smart Farming Assistant API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# All API routes prefixed with /api
app.include_router(auth.router,       prefix="/api/auth",           tags=["Auth"])
app.include_router(weather.router,    prefix="/api/weather",        tags=["Weather"])
app.include_router(crops.router,      prefix="/api/crop-recommend", tags=["Crops"])
app.include_router(disease.router,    prefix="/api/disease-detect", tags=["Disease"])
app.include_router(soil.router,       prefix="/api/soil",           tags=["Soil"])
app.include_router(irrigation.router, prefix="/api/irrigation",     tags=["Irrigation"])
app.include_router(market.router,     prefix="/api/market",         tags=["Market"])
app.include_router(alerts.router,     prefix="/api/alerts",         tags=["Alerts"])


@app.get("/api/health")
async def health():
    return {"status": "healthy"}


# Serve React build
BUILD_DIR = os.path.join(os.path.dirname(__file__), "../frontend/build")

if os.path.exists(BUILD_DIR):
    app.mount("/static", StaticFiles(directory=os.path.join(BUILD_DIR, "static")), name="static")

    @app.get("/")
    async def serve_root():
        return FileResponse(os.path.join(BUILD_DIR, "index.html"))

    @app.get("/{full_path:path}")
    async def serve_react(full_path: str):
        if full_path.startswith("api/"):
            return {"detail": "Not found"}
        return FileResponse(os.path.join(BUILD_DIR, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "API running. Build frontend first: cd frontend && npm run build"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
