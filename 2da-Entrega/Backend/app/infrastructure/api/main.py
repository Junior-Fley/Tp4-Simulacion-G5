from fastapi import FastAPI
from app.infrastructure.api.controllers.SimularController import router as sim_router

app = FastAPI(title="Simulador", version="1.0.0")
app.include_router(sim_router)