import React, { useEffect, useState } from "react";
import { Button, Modal, Table } from "react-bootstrap";
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
  const [detalleFila, setDetalleFila] = useState(null);
  const [detalleAbierto, setDetalleAbierto] = useState(false);

  const mostrarValorVacioNAda = (valor) =>
    valor === -1 ? "" : valor;

  const formatoHoraAmPm = (valor) => {
    if (valor == null || valor === "") return "";
    if (typeof valor === "string" && valor.includes(":")) return valor;

    const totalSeconds = Math.round(Number(valor) * 60);
    if (Number.isNaN(totalSeconds)) return "";

    const hours24 = Math.floor(totalSeconds / 3600) % 24;
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    const ampm = hours24 >= 12 ? "PM" : "AM";
    const hours12 = hours24 % 12 === 0 ? 12 : hours24 % 12;

    const h = String(hours12).padStart(2, "0");
    const m = String(minutes).padStart(2, "0");
    const s = String(seconds).padStart(2, "0");

    return `${h}:${m}:${s} ${ampm}`;
  };

  const abrirDetalle = (fila) => {
    setDetalleFila(fila);
    setDetalleAbierto(true);
  };

  const cerrarDetalle = () => {
    setDetalleAbierto(false);
    setDetalleFila(null);
  };

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
      <div className="mb-3 tabla-selector">
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
          <option value="">Seleccionar simulación</option>

          {simulaciones.map((sim, index) => (
            <option key={`${sim.id}-${index}`} value={sim.id}>
              Simulación #{sim.id}
            </option>
          ))}
        </select>
      </div>

      {/* CARDS */}
      <div className="container mt-3">
        <div className="row g-3 justify-content-center">

          <div className="col-md-3">
            <div className="card shadow-sm border-danger text-center">
              <div className="card-body">
                <h6>Cant de Clientes No Atendidos por cierre</h6>
                <h3>
                  {filas.length > 0
                    ? filas[filas.length - 1].clientes_no_atendidos
                    : 0}
                </h3>
              </div>
            </div>
          </div>

          <div className="col-md-3">
            <div className="card shadow-sm border-primary text-center">
              <div className="card-body">
                <h6>T.promedio de permanecia de equipo en el taller Hf - Hi </h6>
                <h3>
                  {filas.length > 0
                    ? filas[filas.length - 1].tiempo_de_atencion_total
                    : "00:00:00"}
                </h3>
              </div>
            </div>
          </div>

          <div className="col-md-3">
            <div className="card shadow-sm border-success text-center">
              <div className="card-body">
                <h6> Porcentaje del tecnico recep vs reparacion</h6>
                <h3>
                  {filas.length > 0
                    ? filas[filas.length - 1].tiempo_de_reparacion_total
                    : "00:00:00"}
                </h3>
              </div>
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
                <th>Detalle</th>
              </tr>
            </thead>

            <tbody>
              {filas.map((fila, index) => (
                <React.Fragment key={index}>

                  {fila.evento === "Abre_Tienda" && (
                    <tr className="table-primary">
                      <td
                        colSpan={
                          21
                        }
                        className="text-center fw-bold"
                      >
                        Inicio Nuevo Día de la Simulación
                      </td>
                    </tr>
                  )}

                  <tr>
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
                    <td>
                      <Button
                        variant="outline-primary"
                        size="sm"
                        onClick={() => abrirDetalle(fila)}
                      >
                        Ver
                      </Button>
                    </td>
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
        </select>

      </div>

      {/* DETALLE */}
      <Modal
        show={detalleAbierto}
        onHide={cerrarDetalle}
        size="lg"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>Detalle de fila</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="mb-3">
            <h6>Clientes</h6>
            {detalleFila?.clientes?.length ? (
              <ul className="mb-0">
                {detalleFila.clientes.map((cliente, idx) => (
                  <li key={cliente.id ?? `cliente-${idx}`}>
                    Cliente {cliente.id ?? idx + 1} - {cliente.estado ?? ""}
                  </li>
                ))}
              </ul>
            ) : (
              <span>Sin clientes</span>
            )}
          </div>
          <div>
            <h6>Equipos</h6>
            {detalleFila?.equipos?.length ? (
              <ul className="mb-0">
                {detalleFila.equipos.map((equipo, idx) => (
                  <li key={equipo.id ?? `equipo-${idx}`}>
                    Equipo {equipo.id ?? idx + 1} - {equipo.estado ?? ""}
                    {equipo.hora_dejado
                      ? ` - Dejado: ${formatoHoraAmPm(equipo.hora_dejado)}`
                      : ""}
                    {equipo.hora_fin
                      ? ` - Fin: ${formatoHoraAmPm(equipo.hora_fin)}`
                      : ""}
                    {equipo.tiempo != null && equipo.tiempo !== ""
                      ? ` - Tiempo: ${Number(equipo.tiempo).toFixed(2)} min`
                      : ""}
                  </li>
                ))}
              </ul>
            ) : (
              <span>Sin equipos</span>
            )}
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={cerrarDetalle}>
            Cerrar
          </Button>
        </Modal.Footer>
      </Modal>

    </div>
  );
};