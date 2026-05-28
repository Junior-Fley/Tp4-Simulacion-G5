import React, { useEffect, useState } from "react";
import { Button, Modal, Table } from "react-bootstrap";
import simulacionService from "../service/simulacion.service";
import "../App.css";

export const VectorEstado = ({ simId, onSimIdChange }) => {
  const TAMANIO_PAGINA = 50;
  const MAX_PAGE_SIZE = 100;

  const [filasBase, setFilasBase] = useState([]);
  const [filas, setFilas] = useState([]);
  const [simulaciones, setSimulaciones] = useState([]);

  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [ultimaFila, setUltimaFila] = useState(null);
  const [stats, setStats] = useState(null);
  const [detalleFila, setDetalleFila] = useState(null);
  const [detalleAbierto, setDetalleAbierto] = useState(false);
  
  const [filtroP, setFiltroP] = useState(String(TAMANIO_PAGINA));
  const [filtroQ, setFiltroQ] = useState("");

  const pageSize = Math.min(
    MAX_PAGE_SIZE,
    Math.max(1, Number(filtroP) || TAMANIO_PAGINA)
  );

  const simIdNormalizado = simId == null ? "" : String(simId);
  const simIdEnLista =
    !!simIdNormalizado &&
    simulaciones.some((s) => String(s?.id) === simIdNormalizado);

  const mostrarValorVacioNAda = (valor) => {
    if (valor === -1 || valor === null || valor === undefined || valor === "") {
      return "";
    }

    // Evitar mostrar "NaN" si llega algo no numérico en un campo esperado como número.
    const num = typeof valor === "number" ? valor : Number(valor);
    if (typeof valor === "number" || (typeof valor === "string" && valor.trim() !== "")) {
      if (Number.isNaN(num)) return "";
    }

    return valor;
  };

  const formatoTiempoEquipo = (valor) => {
    if (valor === null || valor === undefined || valor === "") return "";
    if (typeof valor === "string" && valor.includes(":")) return valor;

    const num = Number(valor);
    if (!Number.isFinite(num)) return "";
    return `${num.toFixed(2)} min`;
  };

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

  const formatoPorcentaje = (valor) => {
    if (valor === null || valor === undefined || valor === "") return "";
    const num = Number(valor);
    if (!Number.isFinite(num)) return "";
    return num.toFixed(2);
  };

  const normalizarEvento = (evento) =>
    typeof evento === "string" ? evento.trim().replace(/\s+/g, "_") : evento;

  const horaASegundos = (valor) => {
    if (valor === null || valor === undefined || valor === "") return null;

    if (typeof valor === "string" && valor.includes(":")) {
      const partes = valor.split(":");
      const horas = Number(partes[0] ?? 0);
      const minutos = Number(partes[1] ?? 0);
      const segundos = Number(partes[2] ?? 0);
      if ([horas, minutos, segundos].some((n) => Number.isNaN(n))) return null;
      return horas * 3600 + minutos * 60 + segundos;
    }

    const num = Number(valor);
    if (!Number.isFinite(num)) return null;
    return Math.round(num * 60);
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
    const cargarSimulaciones = async () => {
      try {
        const data = await simulacionService.listarSimulaciones();

        // El backend puede devolver [1,2] o [{id:1}, ...]
        const normalizadas = Array.isArray(data)
          ? data
              .map((s) => {
                if (s == null) return null;
                if (typeof s === "number" || typeof s === "string") return { id: String(s) };
                if (typeof s === "object" && s.id != null) return { id: String(s.id) };
                return null;
              })
              .filter(Boolean)
          : [];

        setSimulaciones(() => {
          const currentId = simId ? String(simId) : "";
          if (!currentId) return normalizadas;
          if (normalizadas.some((s) => String(s?.id) === currentId)) return normalizadas;
          return [{ id: currentId }, ...normalizadas];
        });
      } catch (error) {
        console.error("Error al listar simulaciones:", error);

        // Fallback: mantener compatibilidad con el flujo anterior
        const simsLocal = JSON.parse(
          localStorage.getItem("simulaciones") || "[]"
        );
        const fromLocal = Array.isArray(simsLocal)
          ? simsLocal
              .map((s) => (s?.id != null ? { id: String(s.id) } : null))
              .filter(Boolean)
          : [];

        setSimulaciones(() => {
          const currentId = simId ? String(simId) : "";
          if (!currentId) return fromLocal;
          if (fromLocal.some((s) => String(s?.id) === currentId)) return fromLocal;
          return [{ id: currentId }, ...fromLocal];
        });
      }
    };

    cargarSimulaciones();
  }, [simId]);

  useEffect(() => {
    const cargarFilas = async () => {
      try {
        if (!simId) {
          setFilasBase([]);
          setFilas([]);
          setUltimaFila(null);
          setTotalPages(0);
          return;
        }

        const primeraRespuesta = await simulacionService.obtenerListasFilas(
          simId,
          1,
          TAMANIO_PAGINA
        );

        const totalPagesRespuesta = Number(primeraRespuesta?.total_pages ?? 0);
        const itemsIniciales = Array.isArray(primeraRespuesta?.items)
          ? primeraRespuesta.items
          : [];

        let acumuladas = [...itemsIniciales];

        for (let pagina = 2; pagina <= totalPagesRespuesta; pagina += 1) {
          const respuestaPagina = await simulacionService.obtenerListasFilas(
            simId,
            pagina,
            TAMANIO_PAGINA
          );

          const itemsPagina = Array.isArray(respuestaPagina?.items)
            ? respuestaPagina.items
            : [];
          acumuladas = acumuladas.concat(itemsPagina);
        }

        setFilasBase(acumuladas);
        setUltimaFila(acumuladas[acumuladas.length - 1] ?? null);
        setPage(1);
      } catch (error) {
        console.error("Error al obtener filas:", error);
        setFilasBase([]);
        setFilas([]);
        setUltimaFila(null);
        setTotalPages(0);
      }
    };

cargarFilas();
  }, [simId]);

  useEffect(() => {
    if (!Array.isArray(filasBase)) {
      setFilas([]);
      setTotalPages(0);
      return;
    }

    let inicio = 0;

    if (filtroQ !== "") {
      const horaObjetivo = horaASegundos(filtroQ);

      if (horaObjetivo === null) {
        setFilas([]);
        setTotalPages(0);
        return;
      }

      inicio = filasBase.findIndex((fila) => {
        const horaFila = horaASegundos(fila.hora);
        return horaFila !== null && horaFila >= horaObjetivo;
      });

      if (inicio === -1) {
        setFilas([]);
        setTotalPages(0);
        return;
      }
    }

    const filasDesdeHora = filasBase.slice(inicio);
    const total = filasDesdeHora.length;
    const paginas = total > 0 ? Math.ceil(total / pageSize) : 0;

    if (page > paginas && paginas > 0) {
      setPage(paginas);
      return;
    }

    const inicioPagina = (page - 1) * pageSize;
    const finPagina = inicioPagina + pageSize;

    setFilas(filasDesdeHora.slice(inicioPagina, finPagina));
    setTotalPages(paginas);
  }, [filasBase, page, pageSize, filtroQ]);

  useEffect(() => {
    const cargarStats = async () => {
      try {
        if (!simId) {
          setStats(null);
          return;
        }

        const data = await simulacionService.obtenerStats(simId);
        setStats(data ?? null);
      } catch (error) {
        console.error("Error al obtener estadísticas:", error);
        setStats(null);
      }
    };

    cargarStats();
  }, [simId]);
  
  const vistaFiltrada = filtroP !== "" || filtroQ !== "";

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
            if (typeof onSimIdChange === "function") {
              onSimIdChange(id);
            }
            localStorage.setItem("simId", id);
            setPage(1);
            setFiltroP("");
            setFiltroQ("");
          }}
        >
          <option value="">Seleccionar simulación...</option>

          {simIdNormalizado && !simIdEnLista && (
            <option value={simIdNormalizado}>
              Simulación #{simIdNormalizado}
            </option>
          )}

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
                {stats?.clientes_no_atendidos ??
                  (ultimaFila ? ultimaFila.clientes_no_atendidos : 0)}
                <span className="ms-2 fs-6 fw-normal text-muted">clientes</span>
              </h3>
            </div>
          </div>

          <div className="col-md-4">
            <div className="kpi-card kpi-primary">
              <div className="kpi-icon">
                <i className="bi bi-hourglass-split"></i>
              </div>
              <h6>Permanencia Promedio en Taller</h6>
              <h3>
                {stats?.promedio_permanencia_equipo ?? "—"}
                <span className="ms-2 fs-6 fw-normal text-muted">hh:mm:ss</span>
              </h3>
            </div>
          </div>

          <div className="col-md-4">
            <div className="kpi-card kpi-success">
              <div className="kpi-icon">
                <i className="bi bi-tools"></i>
              </div>
              <h6>Porcentaje Tiempo: Recepción / Reparación</h6>
              <h3>
                {(() => {
                  const rec = formatoPorcentaje(stats?.porcentaje_tiempo_recepcion);
                  const rep = formatoPorcentaje(stats?.porcentaje_tiempo_reparacion);
                  if (!rec && !rep) return "—";
                  return `${rec || "0.00"}% / ${rep || "0.00"}%`;
                })()}
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
                <th>Hora</th>
                <th>Evento</th>
                <th>RND Llegada</th>
                <th>T. Entre Llegadas (hh:mm:ss)</th>
                <th>Próxima Llegada (hh:mm:ss)</th>
                <th>Estado Técnico</th>
                <th>RND Dur. Atención</th>
                <th>Dur. Atención (hh:mm:ss)</th>
                <th>Próx. Fin Atención (hh:mm:ss)</th>
                <th>RND Presupuesto</th>
                <th>Presupuesto</th>
                <th>RND ¿Deja?</th>
                <th>¿Deja?</th>
                <th>RND Dur. Reparación</th>
                <th>Dur. Reparación (hh:mm:ss)</th>
                <th>Cola Atención (cant.)</th>
                <th>Cola Equipos (cant.)</th>
                <th>T. Atención (hh:mm:ss)</th>
                <th>T. Reparación (hh:mm:ss)</th>
                <th>No Atendidos (cant.)</th>
                <th>Detalle</th>
              </tr>
            </thead>

            <tbody>
              {filas.map((fila, index) => (
                <React.Fragment key={index}>
                  {normalizarEvento(fila.evento) === "Abre_Tienda" && (
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
              
  {ultimaFila && (
    <>
      <tr className="table-secondary">
        <td colSpan={21} className="text-center fw-bold">
          Última fila de la simulación
        </td>
      </tr>

      <tr className="table-warning">
        <td>{ultimaFila.hora}</td>
        <td>{ultimaFila.evento}</td>
        <td>{mostrarValorVacioNAda(ultimaFila.rnd_llegada)}</td>
        <td>{ultimaFila.tiempo_entre_llegadas}</td>
        <td>{ultimaFila.proxima_llegada}</td>
        <td>{ultimaFila.estado_tecnico}</td>
        <td>{mostrarValorVacioNAda(ultimaFila.rnd_duracion_atencion)}</td>
        <td>{ultimaFila.duracion_atencion}</td>
        <td>{ultimaFila.proximo_fin_atencion}</td>
        <td>{mostrarValorVacioNAda(ultimaFila.rnd_presupuesto)}</td>
        <td>{ultimaFila.presupuesto}</td>
        <td>{mostrarValorVacioNAda(ultimaFila.rnd_deja_equipo)}</td>
        <td>
          {ultimaFila.deja_equipo == null ? "" : ultimaFila.deja_equipo ? "Sí" : "No"}
        </td>
        <td>{mostrarValorVacioNAda(ultimaFila.rnd_duracion_reparacion)}</td>
        <td>{ultimaFila.duracion_reparacion}</td>
        <td>{ultimaFila.fila_atencion_cantidad}</td>
        <td>{ultimaFila.fila_equipos_cantidad}</td>
        <td>{ultimaFila.tiempo_de_atencion_total}</td>
        <td>{ultimaFila.tiempo_de_reparacion_total}</td>
        <td>{ultimaFila.clientes_no_atendidos}</td>
        <td>
          <Button
            variant="outline-primary"
            size="sm"
            onClick={() => abrirDetalle(ultimaFila)}
          >
            Ver
          </Button>
        </td>
      </tr>
    </>
  )}
            </tbody>

          </Table>

        </div>

      </div>

      {/* PAGINACIÓN */}
      <div className="tabla-pagination d-flex flex-column align-items-stretch gap-3">
        <div className="d-flex flex-wrap align-items-end justify-content-center gap-3">
          <div className="d-flex flex-column">
            <label className="form-label mb-1 fw-semibold">
              Cantidad de Iteraciones:
            </label>
            <input
              type="number"
              min="1"
              max="100" 
              className="form-control tabla-size"
              placeholder=""
              value={filtroP}
              onChange={(e) => {
                setFiltroP(e.target.value);
                setPage(1);
              }}
            />
          </div>

          <div className="d-flex flex-column">
            <label className="form-label mb-1 fw-semibold">
              Hora de inicio:
            </label>
            <input
              type="time"
              step="1"
              className="form-control tabla-size"
              style={{ width: "600px" }}
              value={filtroQ}
              onChange={(e) => {
                setFiltroQ(e.target.value);
                setPage(1);
              }}
            />
          </div>

          <button
            className="btn btn-outline-secondary"
            onClick={() => {
              setFiltroP("");
              setFiltroQ("");
              setPage(1);
            }}
          >
            Limpiar
          </button>
        </div>

        <div className="d-flex align-items-center justify-content-center gap-3">
          <button
            className="btn btn-secondary"
            onClick={() => setPage((prev) => Math.max(1, prev - 1))}
            disabled={page === 1}
          >
            Anterior
          </button>

          <span>
            Página {page} {totalPages > 0 ? `de ${totalPages}` : ""}
          </span>

          <button
            className="btn btn-secondary"
            onClick={() => setPage((prev) => prev + 1)}
            disabled={totalPages > 0 && page >= totalPages}
          >
            Siguiente
          </button>
        </div>
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
                      ? ` - Hora dejado: ${formatoHoraAmPm(equipo.hora_dejado)}`
                      : ""}
                    {equipo.hora_fin
                      ? ` - Hora Fin: ${formatoHoraAmPm(equipo.hora_fin)}`
                      : ""}
                    {(() => {
                      const t = formatoTiempoEquipo(equipo.tiempo);
                      return t ? ` - Tiempo: ${t} (hh:mm:ss)` : "";
                    })()}
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