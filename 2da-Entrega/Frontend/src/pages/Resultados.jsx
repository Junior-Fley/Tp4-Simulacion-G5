import React from "react";

export const Resultados = ({ metricas }) => {
  const {
    clientesRechazados = 0,
    tiempoPromedioTaller = 0,
    productividadTecnico = 0,
  } = metricas || {};

  const card = {
    background: "#f5f5f5",
    borderRadius: 6,
    padding: "1rem",
  };

  return (
    <div style={{ fontFamily: "sans-serif", padding: "1rem" }}>
      <h3 style={{ color: "#555", marginBottom: "1rem" }}>
        Métricas de Desempeño — i-Fix Taller
      </h3>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
        <div style={card}>
          <p style={{ color: "#888", fontSize: 13, margin: "0 0 6px" }}>Clientes rechazados</p>
          <p style={{ color: "#c0392b", fontSize: 28, fontWeight: 600, margin: 0 }}>{clientesRechazados}</p>
        </div>
        <div style={card}>
          <p style={{ color: "#888", fontSize: 13, margin: "0 0 6px" }}>Tiempo promedio en taller</p>
          <p style={{ fontSize: 28, fontWeight: 600, margin: 0 }}>
            {tiempoPromedioTaller.toFixed(2)} <span style={{ fontSize: 14, fontWeight: 400 }}>min</span>
          </p>
        </div>
        <div style={card}>
          <p style={{ color: "#888", fontSize: 13, margin: "0 0 6px" }}>Productividad del técnico</p>
          <p style={{ color: "#27ae60", fontSize: 28, fontWeight: 600, margin: 0 }}>
            {productividadTecnico.toFixed(1)}<span style={{ fontSize: 14, fontWeight: 400 }}>%</span>
          </p>
          <p style={{ color: "#aaa", fontSize: 11, margin: "4px 0 0" }}>Tiempo en estado 'Reparando'</p>
        </div>
      </div>
    </div>
  );
};

export default Resultados;