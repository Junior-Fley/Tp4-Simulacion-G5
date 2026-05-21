  import React from "react";
  import { Table } from "react-bootstrap";

  export const VectorEstado = () => {
    const columnas_th = [
  "#",
  "Hora",
  "Evento",
  "RND Llegada",
  "Tiempo entre Llegadas",
  "Próxima Llegada",
  "Estado",
  "RND Duración Atención",
  "Duración Atención",
  "Próximo Fin de la Atención",
  "RND Presupuesto",
  "Presupuesto",
  "RND ¿Deja para reparar?",
  "¿Deja para reparar?",
  "RND Duración Reparación",
  "Duración",
  "Atención",
  "Reparación",
  "Tiempo de Atención",
  "Tiempo de Reparación",
  "Clientes No Atendidos por Cierre",
  "Estado",
  "Estado",
  "Estado",
  "Estado",
  "Estado",
  "Estado",
  "Estado",
  "Hora Dejado en Taller",
  "Hora Fin Reparación",
  "Tiempo Reparación",
];
    return (
      <Table responsive>
        <thead>
          <tr style={{minWidth: "150px", whiteSpace: "nowrap", padding: "8px 16px", backgroundColor: "#04AA6D", color: "white"}}  
          >
                {columnas_th.map((col, index) => (
                  <th key={index}>{col}</th>
                ))}
              </tr>

        </thead>

        <tbody onMouseOver={(e) => {
    if (e.target.closest("tr")) {
      e.target.closest("tr").style.backgroundColor = "coral";
    }
  }}
  onMouseOut={(e) => {
    if (e.target.closest("tr")) {
      e.target.closest("tr").style.backgroundColor = "";
    }
  }}>
          <tr>
            <td>1</td>
            {Array.from({ length: 12 }).map((_, index) => (
              <td key={index}>Table cell {index}</td>
            ))}
          </tr>
          <tr>
            <td>2</td>
            {Array.from({ length: 12 }).map((_, index) => (
              <td key={index}>Table cell {index}</td>
            ))}
          </tr>
          <tr>
            <td>3</td>
            {Array.from({ length: 12 }).map((_, index) => (
              <td key={index}>Table cell {index}</td>
            ))}
          </tr>
        </tbody>
      </Table>
    );
  };
