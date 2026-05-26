import React, { useEffect, useState } from "react";
import { Table } from "react-bootstrap";
import simulacionService from "../service/simulacion.service";
import "../App.css";

export const VectorEstado = () => {

  const [filas, setFilas] = useState([]);
  const [simulaciones, setSimulaciones] = useState([]);

  const [simId, setSimId] = useState(
    localStorage.getItem("simId")
  );

  const [page, setPage] = useState(1);
  const [size, setSize] = useState(50);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  const mostrarValorVacioNAda = (valor) =>
    valor === -1 ? "" : valor;

  // Calcular máximos de clientes y equipos en la página actual
  const maxClientes = filas.length > 0
    ? Math.max(0, ...filas.map(f => f.clientes?.length ?? 0))
    : 0;

  const maxEquipos = filas.length > 0
    ? Math.max(0, ...filas.map(f => f.equipos?.length ?? 0))
    : 0;

  useEffect(() => {
    const sims = JSON.parse(
      localStorage.getItem("simulaciones") || "[]"
    );
    setSimulaciones(sims);
  }, []);

  useEffect(() => {
    const cargarFilas = async () => {
      try {
        if (!simId) return;

        const data = await simulacionService.obtenerListasFilas(
          simId,
          page,
          size
        );

        setFilas(data.items);
        setTotal(data.total ?? 0);
        setTotalPages(data.total_pages ?? 0);

      } catch (error) {
        console.error("Error al obtener filas:", error);
      }
    };

    cargarFilas();
  }, [simId, page, size]);

  return (
    <div className="tabla-page">

      {/* SELECTOR */}
      <div className="mb-4 tabla-selector d-flex align-items-center gap-3 justify-content-center">
        <label className="form-label mb-0 fw-semibold text-slate-700">
          <i className="bi bi-database-fill-gear text-primary me-2"></i>Historial de Simulaciones:
        </label>
        <select
          className="form-select"
          value={simId || ""}
          onChange={(e) => {
            const id = e.target.value;
            setSimId(id);
            localStorage.setItem("simId", id);
            setPage(1);
          }}
        >
          <option value="">Seleccionar simulación...</option>

          {simulaciones.map((sim, index) => (
            <option key={`${sim.id}-${index}`} value={sim.id}>
              Simulación #{sim.id}
            </option>
          ))}
        </select>
      </div>

      {/* CARDS */}
      <div className="kpi-container container mt-2">
        <div className="row g-4 justify-content-center">

          <div className="col-md-4">
            <div className="kpi-card kpi-danger">
              <div className="kpi-icon">
                <i className="bi bi-person-x-fill"></i>
              </div>
              <h6>Clientes No Atendidos por Cierre</h6>
              <h3>
                {filas.length > 0
                  ? filas[filas.length - 1].clientes_no_atendidos
                  : 0}
              </h3>
            </div>
          </div>

          <div className="col-md-4">
            <div className="kpi-card kpi-primary">
              <div className="kpi-icon">
                <i className="bi bi-hourglass-split"></i>
              </div>
              <h6>Permanencia Promedio en Taller (Hf - Hi)</h6>
              <h3>
                {filas.length > 0
                  ? filas[filas.length - 1].tiempo_de_atencion_total
                  : "00:00:00"}
              </h3>
            </div>
          </div>

          <div className="col-md-4">
            <div className="kpi-card kpi-success">
              <div className="kpi-icon">
                <i className="bi bi-tools"></i>
              </div>
              <h6>Porcentaje Técnico: Recep vs Reparación</h6>
              <h3>
                {filas.length > 0
                  ? filas[filas.length - 1].tiempo_de_reparacion_total
                  : "00:00:00"}
              </h3>
            </div>
          </div>

        </div>
      </div>

      {/* TABLA */}
      <div className="tabla-card">

        <div className="tabla-scroll">

          <Table hover bordered className="tabla-vector">

            <thead>
              <tr>
                {/* COLUMNAS FIJAS */}
                <th>Hora</th>
                <th>Evento</th>
                <th>RND Llegada</th>
                <th>T. Entre Llegadas</th>
                <th>Próxima Llegada</th>
                <th>Estado Técnico</th>
                <th>RND Dur. Atención</th>
                <th>Dur. Atención</th>
                <th>Próx. Fin Atención</th>
                <th>RND Presupuesto</th>
                <th>Presupuesto</th>
                <th>RND ¿Deja?</th>
                <th>¿Deja?</th>
                <th>RND Dur. Reparación</th>
                <th>Dur. Reparación</th>
                <th>Cola Atención</th>
                <th>Cola Equipos</th>
                <th>T. Atención</th>
                <th>T. Reparación</th>
                <th>No Atendidos</th>

                {/* COLUMNAS DINÁMICAS — CLIENTES */}
                {Array.from({ length: maxClientes }, (_, i) => (
                  <th key={`ch-cli-${i}`} style={{ minWidth: 130 }}>
                    Cliente {i + 1} — Estado
                  </th>
                ))}

                {/* COLUMNAS DINÁMICAS — EQUIPOS (4 sub-columnas por equipo) */}
                {Array.from({ length: maxEquipos }, (_, i) => (
                  <React.Fragment key={`ch-eq-${i}`}>
                    <th style={{ minWidth: 130 }}>Equipo {i + 1} — Estado</th>
                    <th style={{ minWidth: 110 }}>Equipo {i + 1} — Dejado</th>
                    <th style={{ minWidth: 110 }}>Equipo {i + 1} — Fin</th>
                    <th style={{ minWidth: 110 }}>Equipo {i + 1} — Tiempo</th>
                  </React.Fragment>
                ))}
              </tr>
            </thead>

            <tbody>
              {filas.map((fila, index) => (
                <React.Fragment key={index}>

                  {fila.evento === "Abre_Tienda" && (
                    <tr className="table-primary">
                      <td
                        colSpan={
                          20
                          + maxClientes
                          + maxEquipos * 4
                        }
                        className="text-center fw-bold"
                      >
                        Inicio Nuevo Día de la Simulación
                      </td>
                    </tr>
                  )}

                  <tr>
                    {/* CELDAS FIJAS */}
                    <td>{fila.hora}</td>
                    <td>{fila.evento}</td>
                    <td>{mostrarValorVacioNAda(fila.rnd_llegada)}</td>
                    <td>{fila.tiempo_entre_llegadas}</td>
                    <td>{fila.proxima_llegada}</td>
                    <td>{fila.estado_tecnico}</td>
                    <td>{mostrarValorVacioNAda(fila.rnd_duracion_atencion)}</td>
                    <td>{fila.duracion_atencion}</td>
                    <td>{fila.proximo_fin_atencion}</td>
                    <td>{mostrarValorVacioNAda(fila.rnd_presupuesto)}</td>
                    <td>{fila.presupuesto}</td>
                    <td>{mostrarValorVacioNAda(fila.rnd_deja_equipo)}</td>
                    <td>
                      {fila.deja_equipo == null
                        ? ""
                        : fila.deja_equipo
                        ? "Sí"
                        : "No"}
                    </td>
                    <td>{mostrarValorVacioNAda(fila.rnd_duracion_reparacion)}</td>
                    <td>{fila.duracion_reparacion}</td>
                    <td>{fila.fila_atencion_cantidad}</td>
                    <td>{fila.fila_equipos_cantidad}</td>
                    <td>{fila.tiempo_de_atencion_total}</td>
                    <td>{fila.tiempo_de_reparacion_total}</td>
                    <td>{fila.clientes_no_atendidos}</td>

                    {/* CELDAS DINÁMICAS — CLIENTES */}
                    {Array.from({ length: maxClientes }, (_, i) => (
                      <td key={`fila-${index}-cli-${i}`}>
                        {fila.clientes?.[i]?.estado ?? ""}
                      </td>
                    ))}

                    {/* CELDAS DINÁMICAS — EQUIPOS */}
                    {Array.from({ length: maxEquipos }, (_, i) => (
                      <React.Fragment key={`fila-${index}-eq-${i}`}>
                        <td>{fila.equipos?.[i]?.estado ?? ""}</td>
                        <td>{fila.equipos?.[i]?.hora_dejado ?? ""}</td>
                        <td>{fila.equipos?.[i]?.hora_fin ?? ""}</td>
                        <td>{fila.equipos?.[i]?.tiempo ?? ""}</td>
                      </React.Fragment>
                    ))}
                  </tr>

                </React.Fragment>
              ))}
            </tbody>

          </Table>

        </div>

      </div>

      {/* PAGINACIÓN */}
      <div className="tabla-pagination">

        <button
          className="btn btn-secondary"
          onClick={() => setPage(page - 1)}
          disabled={page === 1}
        >
          Anterior
        </button>

        <span>
          Página {page} {totalPages > 0 ? `de ${totalPages}` : ""}
        </span>

        <button
          className="btn btn-secondary"
          onClick={() => setPage(page + 1)}
          disabled={totalPages > 0 && page >= totalPages}
        >
          Siguiente
        </button>

        <select
          className="form-select tabla-size"
          value={size}
          onChange={(e) => {
            setSize(Number(e.target.value));
            setPage(1);
          }}
        >
          <option value={10}>10</option>
          <option value={50}>50</option>
          <option value={100}>100</option>
          <option value={500}>500</option>
        </select>

      </div>

    </div>
  );
};