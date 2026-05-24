from typing import List

from fastapi import APIRouter, HTTPException, Query

from app.infrastructure.api.DTO.SimulacionItem import SimulacionItem
from app.infrastructure.api.DTO.SimularRequest import SimularRequest
from app.infrastructure.api.DTO.SimularResponse import SimularResponse
from app.application.useCases.Simular import Simular
from app.infrastructure.database.unit_of_work.uow_factory import uow_factory
from app.application.useCases.QuerySimulaciones import QuerySimulaciones

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
    #coleccion_id = simulador.ejecutar_simulacion()

    import time
    start = time.perf_counter()
    coleccion_id = simulador.ejecutar_simulacion()
    elapsed = time.perf_counter() - start
    print()
    print()
    print()
    print(f"Duración simulación id {coleccion_id}: {elapsed:.4f} segundos")


    return SimulacionCreatedResponse(
        mensaje="Simulación ejecutada correctamente",
        id_simulacion= str(coleccion_id),
        filas_guardadas= 100
    )# TODO CREAR MÉTODO PARA QUE BUSQUE LA CANTIDAD REAL DE FILAS GUARDADAS EN LA SIMULACIÓN


@router.get("/simulaciones/{sim_id}/filas", response_model=SimularResponse)
def listar_filas(sim_id: int, page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=500)):

    query_simular = QuerySimulaciones(uow_factory)
    items, total = query_simular.get_simulaciones(sim_id, page, size)

    if total == 0:
        raise HTTPException(status_code=404, detail=f"Simulación id: {sim_id} no encontrada")

    total_pages = (total + size - 1) // size if total > 0 else 0

    items_dto: List[SimulacionItem] = []

    for simulacion in items:
        simulacion_item = SimulacionItem.from_domain(simulacion)
        items_dto.append(simulacion_item)


    return SimularResponse(items=items_dto, page=page, size=size, total=total, total_pages=total_pages)

#TODO CREAR ENDPOINT PARA OBTENER LAS ESTADÍSTICAS DE LOS ACUMULADORES