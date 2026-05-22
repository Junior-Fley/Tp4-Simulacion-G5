from fastapi import APIRouter, HTTPException, Query
from typing import Dict
from uuid import uuid4

from app.infrastructure.api.DTO.SimularRequest import SimularRequest
from app.infrastructure.api.DTO.SimularResponse import SimularResponse

from app.infrastructure.api.repositories.SimularRepository import SimularRepository
from app.application.useCases.Simular import Simular

router = APIRouter()

# almacenamiento en memoria de repos (por proceso)
SIMULACIONES: Dict[str, SimularRepository] = {}


# Response simple para POST (lo dejamos aquí para no tocar los DTOs)
from pydantic import BaseModel

class SimulacionCreatedResponse(BaseModel):
    mensaje: str
    id_simulacion: str
    filas_guardadas: int


@router.post("/simulaciones", response_model=SimulacionCreatedResponse)
def iniciar_simulacion(payload: SimularRequest):
    # Crear repo por simulación
    repo = SimularRepository()
    sim_id = str(uuid4())
    SIMULACIONES[sim_id] = repo

    simulador = Simular(repo=repo, x_tiempo=payload.x_tiempo, i_iteraciones=payload.i_iteraciones, j_hora_inicio=payload.j_hora_inicio)

    # Nota: esto ejecuta síncrono la simulación. Si tarda, la petición bloqueará hasta terminar.
    simulador.ejecutar_simulacion()

    return SimulacionCreatedResponse(
        mensaje="Simulación ejecutada correctamente",
        id_simulacion=sim_id,
        filas_guardadas=repo.total_rows()
    )


@router.get("/simulaciones/{sim_id}/filas", response_model= SimularResponse)
def listar_filas(sim_id: str, page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=500)):
    repo = SIMULACIONES.get(sim_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")

    total = repo.total_rows()
    items = repo.get_page(page, size)
    total_pages = (total + size - 1) // size if total > 0 else 0

    return SimularResponse(items=items, page=page, size=size, total=total, total_pages=total_pages)