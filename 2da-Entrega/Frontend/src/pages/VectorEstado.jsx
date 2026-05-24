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

  const columnas_th = [
    "Hora",
    "Evento",
    "RND Llegada",
    "Tiempo entre Llegadas",
    "Próxima Llegada",
    "Estado Técnico",
    "RND Duración Atención",
    "Duración Atención",
    "Próximo Fin Atención",
    "RND Presupuesto",
    "Presupuesto",
    "RND ¿Deja Reparar?",
    "¿Deja Reparar?",
    "RND Duración Reparación",
    "Duración Reparación",
    "Cola Atención",
    "Cola Equipos",
    "Tiempo Atención",
    "Tiempo Reparación",
    "Clientes No Atendidos"
  ];

  const mostrarValorVacioNAda = (valor) =>
    valor === -1 ? "" : valor;

  // cargar lista de simulaciones 
  useEffect(() => {
    const sims = JSON.parse(
      localStorage.getItem("simulaciones") || "[]"
    );
    setSimulaciones(sims);
  }, []);

  // cargar filas según simId VERRRR
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

      } catch (error) {
        console.error("Error al obtener filas:", error);
      }
    };

    cargarFilas();

  }, [simId, page, size]);

  return (
    <div className="tabla-container">

       {/*****************************************************************************/}
      {/* SELECTOR DE SIMULACIONE */}
      <div className="mb-3">

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
          <option value="">
            Seleccionar simulación
          </option>

          {simulaciones.map((sim) => (
            <option key={sim.id} value={sim.id}>
              Simulación #{sim.id}
            </option>
          ))}

        </select>

      </div>

      {/* RESULTADOS */}
      <div className="container mt-4">

        <div className="row g-3">

          <div className="col-md-3">
            <div className="card shadow-sm border-danger">

              <div className="card-body text-center">

                <h6 className="card-title">
                  Clientes No Atendidos
                </h6>

                <h3>
                  {
                    filas.length > 0
                      ? filas[filas.length - 1]
                          .clientes_no_atendidos
                      : 0
                  }
                </h3>

              </div>

            </div>
          </div>

          <div className="col-md-3">
            <div className="card shadow-sm border-primary">

              <div className="card-body text-center">

                <h6 className="card-title">
                  Tiempo Atención Total
                </h6>

                <h3>
                  {
                    filas.length > 0
                      ? filas[filas.length - 1]
                          .tiempo_de_atencion_total
                      : "00:00:00"
                  }
                </h3>

              </div>

            </div>
          </div>

          <div className="col-md-3">
            <div className="card shadow-sm border-success">

              <div className="card-body text-center">

                <h6 className="card-title">
                  Tiempo Reparación Total
                </h6>

                <h3>
                  {
                    filas.length > 0
                      ? filas[filas.length - 1]
                          .tiempo_de_reparacion_total
                      : "00:00:00"
                  }
                </h3>

              </div>

            </div>
          </div>

          <div className="col-md-3">
            <div className="card shadow-sm border-dark">

              <div className="card-body text-center">

                <h6 className="card-title">
                  Estado Final Técnico
                </h6>

                <h3>
                  {
                    filas.length > 0
                      ? filas[filas.length - 1]
                          .estado_tecnico
                      : "-"
                  }
                </h3>

              </div>

            </div>
          </div>

        </div>

      </div>

      {/* TABLA */}
      <Table hover bordered className="tabla-vector">

        <thead>
          <tr>
            {columnas_th.map((col, i) => (
              <th key={i}>{col}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {filas.map((fila, index) => (

            <React.Fragment key={index}>
                  {/* SEPARADOR VISUAL */}
            {fila.evento === "Abre_Tienda" && (
              <tr className="table-primary">
                <td
                  colSpan={columnas_th.length}
                  className="text-center fw-bold"
                >
                  Inicio de nueva simulación
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
              <td>{fila.deja_equipo ? "Sí" : "No"}</td>
              <td>{mostrarValorVacioNAda(fila.rnd_duracion_reparacion)}</td>
              <td>{fila.duracion_reparacion}</td>
              <td>{fila.fila_atencion_cantidad}</td>
              <td>{fila.fila_equipos_cantidad}</td>
              <td>{fila.tiempo_de_atencion_total}</td>
              <td>{fila.tiempo_de_reparacion_total}</td>
              <td>{fila.clientes_no_atendidos}</td>

            </tr>
            </React.Fragment>
          ))}
        </tbody>

      </Table>

      {/* PAGINACIÓN */}
      <div style={{
        marginTop: "20px",
        display: "flex",
        justifyContent: "center",
        gap: "10px"
      }}>

        <button
          className="btn btn-secondary"
          onClick={() => setPage(page - 1)}
          disabled={page === 1}
        >
          Anterior
        </button>

        <span>Página {page}</span>

        <button
          className="btn btn-secondary"
          onClick={() => setPage(page + 1)}
        >
          Siguiente
        </button>

        <select
          className="form-select"
          style={{ width: "120px" }}
          value={size}
          onChange={(e) => setSize(Number(e.target.value))}
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