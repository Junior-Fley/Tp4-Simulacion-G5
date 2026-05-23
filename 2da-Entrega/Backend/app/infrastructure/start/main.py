from fastapi import FastAPI
import uvicorn
from app.infrastructure.api.controllers.SimularController import router as sim_router

app = FastAPI(title="Simulador", version="1.0.0")
app.include_router(sim_router)

if __name__ == "__main__":
    uvicorn.run("app.infrastructure.start.main:app", host="127.0.0.1", port=8000,reload=True)