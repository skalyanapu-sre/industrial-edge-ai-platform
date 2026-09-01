from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="Industrial Edge AI Inference API",
    description=(
        "Reference API for industrial telemetry validation and predictive-maintenance inference."
    ),
    version="0.1.0",
)


app.include_router(router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "industrial-edge-ai-platform",
        "docs": "/docs",
    }
