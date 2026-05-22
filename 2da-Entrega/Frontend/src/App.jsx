// src/App.jsx
import { useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { Container, Navbar, Nav, Button } from "react-bootstrap";
import { VectorEstado } from "./components/vectorEstado";
import { DefVariables } from "./components/defVariables";
import { Resultados } from "./components/Resultados";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  // Aquí se guardarán los datos limpios de i-Fix cuando el usuario los cambie en /variables
  const [formData, setFormData] = useState({
    semilla: 5843427899,
    tiempoSimular: 480,
    iteraciones: 10000,
    mediaLlegada: 45,
    diagMin: 10,
    diagMax: 20,
    mediaReparacion: 90,
    probPresupuesto: 30,
    probAbandono: 50
  });
  
  // Estado para las métricas que calculará tu backend en Python
  const [metricasSimulacion, setMetricasSimulacion] = useState({
    clientesRechazados: 0,
    tiempoPromedioTaller: 0,
    productividadTecnico: 0
  });

  // Esta función solo actualiza los datos en App cuando el usuario escribe en los inputs
  const handleDataFromVariables = (data) => {
    setFormData(data);
    console.log("Parámetros actualizados en App:", data);
  };

  // ¡ESTA ES LA ACCIÓN PRINCIPAL! Se dispara desde la pantalla del Vector de Estado
  const ejecutarSimulacion = () => {
    console.log("🚀 Disparando simulación con estos parámetros hacia Python:", formData);
    
    // NOTA PARA MÁS ADELANTE:
    // Aquí irá el fetch/axios pasándole el formData actual a tu servidor.
    // Cuando Python responda, haremos el setMetricasSimulacion(respuesta)
    
    alert("¡Simulación ejecutada! Los datos del Vector de Estado se actualizarán aquí abajo.");
  };
  

  return (
    <BrowserRouter>
      {/* Barra de navegación superior verde */}
      <Navbar expand="lg" className="mb-4 shadow-sm" style={{ backgroundColor: "#53a084" }}>
        <Container>
          <Navbar.Brand as={Link} to="/" className="text-white font-weight-bold">
            ⚙️ Service "i-Fix" - TP4
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" className="border-white" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto">
              <Nav.Link as={Link} to="/" className="text-white">
                Vector de Estado
              </Nav.Link>
              <Nav.Link as={Link} to="/variables" className="text-white">
                Configurar Parámetros
              </Nav.Link>
              <Nav.Link as={Link} to="/resultados" className="text-white">
                Métricas de Resultados
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container className="text-center">
        <Routes>
          {/* PÁGINA 1: Vector de Estado + EL BOTÓN DE SIMULAR ACÁ */}
          <Route 
            path="/" 
            element={
              <div style={{ width: "100%", marginTop: "20px" }}>
                <h1 className="mb-3">Vector de Estado de la Simulación</h1>

                <div style={{ textAlign: "center", overflowX: "auto" }}>
                  <VectorEstado />
                </div>
                <div className="d-flex justify-content-center mb-4">
                  <Button 
                    variant="success" 
                    size="lg" 
                    onClick={ejecutarSimulacion}
                    style={{ backgroundColor: "#04AA6D", borderColor: "#04AA6D", padding: "12px 40px", fontSize: "1.2rem" }}
                  >
                    Correr Simulación 
                  </Button>
                </div>
              </div>
              
            } 
          />

          {/* PÁGINA 2: Formulario de configuración (Limpio, sin el botón de envío directo) */}
          <Route 
            path="/variables" 
            element={
              <div style={{ width: "90%", left: "5%", position: "relative" }}>
                <h1 className="mb-4">Service de Tecnología "i-Fix"</h1>
                <h4 className="text-muted mb-4">Definición de Parámetros y Valores en Rojo</h4>
                <DefVariables onSendData={handleDataFromVariables} datosActuales={formData} />
              </div>
            } 
          />

          {/* PÁGINA 3: Métricas finales de resultados */}
          <Route 
            path="/resultados" 
            element={
              <div style={{ width: "90%", left: "5%", position: "relative" }}>
                <Resultados metricas={metricasSimulacion} />
              </div>
            } 
          />
        </Routes>
      </Container>
    </BrowserRouter>
  );
}

export default App;