import React, { useState, useEffect } from "react";
import { Row, Col, Form, FloatingLabel, Card } from "react-bootstrap";

export const DefVariables = ({ onSendData, datosActuales }) => {
  // Inicializamos el estado con las variables reales del modelo de simulación i-Fix
  const [formDatos, setFormDatos] = useState({
    // 1. Parámetros de Control de la Simulación
    tiempoSimular: datosActuales?.tiempoSimular || 480,   // X
    iteraciones: datosActuales?.iteraciones || 10000,     // N
    desdeFila: datosActuales?.desdeFila || 0,             // J
    cantVisualizar: datosActuales?.cantVisualizar || 100, // I

    // 2. Parámetros del Modelo (i-Fix)
    mediaLlegada: datosActuales?.mediaLlegada || 45,      // µ llegada
    diagMin: datosActuales?.diagMin || 10,                // A Diagnóstico
    diagMax: datosActuales?.diagMax || 20,                // B Diagnóstico
    mediaReparacion: datosActuales?.mediaReparacion || 90,// µ reparación profunda
    probPresupuesto: datosActuales?.probPresupuesto || 30,// % Presupuesto elevado
    probAbandono: datosActuales?.probAbandono || 50,      // % No repara si es caro

    // 3. Parámetros del Generador Pseudoaleatorio (RND)
    semilla: datosActuales?.semilla || 5843427899,        // X0
    modulo: datosActuales?.modulo || 536870911,           // m
    multiplicador: datosActuales?.multiplicador || 42243011, // a
    incremento: datosActuales?.incremento || 32155522,    // c
  });

  // Cada vez que formDatos cambie localmente, se lo enviamos a App.jsx automáticamente
  useEffect(() => {
    onSendData(formDatos);
  }, [formDatos]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormDatos({
      ...formDatos,
      [name]: value === "" ? "" : parseFloat(value),
    });
  };

  return (
    <Form className="text-start p-2">
      <Row className="g-4">
        
        {/* BLOQUE 1: PARÁMETROS DE CONTROL DE LA SIMULACIÓN */}
        <Col md={4}>
          <Card className="h-100 border-0 shadow-sm">
            <Card.Header className="bg-secondary text-white font-weight-bold">
              ⏱️ Control de la Simulación
            </Card.Header>
            <Card.Body className="bg-light">
              <FloatingLabel controlId="txtTiempo" label="Tiempo total a simular (X min)" className="mb-3">
                <Form.Control type="number" name="tiempoSimular" value={formDatos.tiempoSimular} onChange={handleChange} />
              </FloatingLabel>
              
              <FloatingLabel controlId="txtIteraciones" label="Cantidad máx. iteraciones (N)" className="mb-3">
                <Form.Control type="number" name="iteraciones" value={formDatos.iteraciones} onChange={handleChange} />
              </FloatingLabel>
              
              <FloatingLabel controlId="txtDesde" label="Hora inicio visualización (J)" className="mb-3">
                <Form.Control type="number" name="desdeFila" value={formDatos.desdeFila} onChange={handleChange} />
              </FloatingLabel>
              
              <FloatingLabel controlId="txtCantVis" label="Cantidad a visualizar (I)" className="mb-3">
                <Form.Control type="number" name="cantVisualizar" value={formDatos.cantVisualizar} onChange={handleChange} />
              </FloatingLabel>
            </Card.Body>
          </Card>
        </Col>

        {/* BLOQUE 2: PARÁMETROS DEL MODELO (VALORES EN ROJO) */}
        <Col md={4}>
          <Card className="h-100 border-0 shadow-sm">
            <Card.Header className="bg-primary text-white font-weight-bold">
              ⚙️ Parámetros del Modelo i-Fix
            </Card.Header>
            <Card.Body className="bg-light">
              <FloatingLabel controlId="txtLlegada" label="Media llegada de clientes (min)" className="mb-3">
                <Form.Control type="number" name="mediaLlegada" value={formDatos.mediaLlegada} onChange={handleChange} />
              </FloatingLabel>
              
              <Row className="g-2 mb-3">
                <Col>
                  <FloatingLabel controlId="txtDiagMin" label="Diag. Mín (A)">
                    <Form.Control type="number" name="diagMin" value={formDatos.diagMin} onChange={handleChange} />
                  </FloatingLabel>
                </Col>
                <Col>
                  <FloatingLabel controlId="txtDiagMax" label="Diag. Máx (B)">
                    <Form.Control type="number" name="diagMax" value={formDatos.diagMax} onChange={handleChange} />
                  </FloatingLabel>
                </Col>
              </Row>
              
              <FloatingLabel controlId="txtReparacion" label="Media reparación taller (min)" className="mb-3">
                <Form.Control type="number" name="mediaReparacion" value={formDatos.mediaReparacion} onChange={handleChange} />
              </FloatingLabel>
              
              <FloatingLabel controlId="txtProbPres" label="Prob. presupuesto elevado (%)" className="mb-3">
                <Form.Control type="number" name="probPresupuesto" value={formDatos.probPresupuesto} onChange={handleChange} />
              </FloatingLabel>
              
              <FloatingLabel controlId="txtProbAbandono" label="Prob. de abandono (%)" className="mb-3">
                <Form.Control type="number" name="probAbandono" value={formDatos.probAbandono} onChange={handleChange} />
              </FloatingLabel>
            </Card.Body>
          </Card>
        </Col>

        {/* BLOQUE 3: PARÁMETROS DEL GENERADOR PSEUDOALEATORIO */}
        <Col md={4}>
          <Card className="h-100 border-0 shadow-sm">
            <Card.Header className="bg-dark text-white font-weight-bold">
              🔢 Generador RND (Congruencial)
            </Card.Header>
            <Card.Body className="bg-light">
              <FloatingLabel controlId="txtSemilla" label="Semilla inicial (X0)" className="mb-3">
                <Form.Control type="number" name="semilla" value={formDatos.semilla} onChange={handleChange} />
              </FloatingLabel>
              
              <FloatingLabel controlId="txtModulo" label="Módulo (m)" className="mb-3">
                <Form.Control type="number" name="modulo" value={formDatos.modulo} onChange={handleChange} />
              </FloatingLabel>
              
              <FloatingLabel controlId="txtMultiplicador" label="Multiplicador (a)" className="mb-3">
                <Form.Control type="number" name="multiplicador" value={formDatos.multiplicador} onChange={handleChange} />
              </FloatingLabel>
              
              <FloatingLabel controlId="txtIncremento" label="Constante aditiva / Incremento (c)" className="mb-3">
                <Form.Control type="number" name="incremento" value={formDatos.incremento} onChange={handleChange} />
              </FloatingLabel>
            </Card.Body>
          </Card>
        </Col>

      </Row>
    </Form>
  );
};