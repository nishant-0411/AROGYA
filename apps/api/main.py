from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Arogya API",
    description="OmniMind medical research assistant backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "arogya-api"}


@app.get("/", tags=["meta"])
async def root() -> dict[str, str]:
    return {"message": "Arogya API is running. See /docs for the OpenAPI spec."}
