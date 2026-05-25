from fastapi import FastAPI
import uvicorn
from app.infrastructure.api.controllers.SimularController import router as sim_router

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Simulador", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sim_router)

if __name__ == "__main__":
    uvicorn.run("app.infrastructure.start.main:app", host="127.0.0.1", port=8000,reload=True)