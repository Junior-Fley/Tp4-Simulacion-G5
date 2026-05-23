from fastapi import APIRouter, HTTPException, Query
from app.infrastructure.api.DTO.SimularRequest import SimularRequest
from app.infrastructure.api.DTO.SimularResponse import SimularResponse
from app.application.useCases.Simular import Simular
from app.infrastructure.database.unit_of_work.uow_factory import uow_factory
from app.infrastructure.api.controllers.hadcoded_data import MOCK_FILAS_SIMULACION
router = APIRouter()

# almacenamiento en memoria de repos (por proceso)



# Response simple para POST (lo dejamos aquí para no tocar los DTOs)
from pydantic import BaseModel

class SimulacionCreatedResponse(BaseModel):
    mensaje: str
    id_simulacion: str
    filas_guardadas: int


@router.post("/simulaciones", response_model=SimulacionCreatedResponse)
def iniciar_simulacion(payload: SimularRequest):
    # Crear repo por simulación

    simulador = Simular(uow_factory, x_tiempo=payload.x_tiempo, i_iteraciones=payload.i_iteraciones, j_hora_inicio=payload.j_hora_inicio)

    # Nota: esto ejecuta síncrono la simulación. Si tarda, la petición bloqueará hasta terminar.
    simulador.ejecutar_simulacion()

    return SimulacionCreatedResponse(
        mensaje="Simulación ejecutada correctamente",
        id_simulacion= "1" ,
        filas_guardadas= 2
    )# TODO ARREGLAR DATOS PARA QUE SE BUSQUEN EN LA BDD


@router.get("/simulaciones/{sim_id}/filas", response_model=SimularResponse)
def listar_filas(sim_id: str, page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=500)):
    # TODO: reemplazar por lectura desde BDD cuando el repo esté listo.
    # Por ahora devolvemos datos hardcodeados para destrabar al frontend.
    filas = MOCK_FILAS_SIMULACION

    total = len(filas)
    if total == 0:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")

    start = (page - 1) * size
    end = start + size
    items = filas[start:end]
    total_pages = (total + size - 1) // size if total > 0 else 0

    return SimularResponse(items=items, page=page, size=size, total=total, total_pages=total_pages)

"""@router.get("/simulaciones/{sim_id}/filas", response_model= SimularResponse)
def listar_filas(sim_id: str, page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=500)):
    repo = ''
    if not repo:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")

    total = repo.total_rows()
    items = repo.get_page(page, size)
    total_pages = (total + size - 1) // size if total > 0 else 0

    return SimularResponse(items=items, page=page, size=size, total=total, total_pages=total_pages)"""