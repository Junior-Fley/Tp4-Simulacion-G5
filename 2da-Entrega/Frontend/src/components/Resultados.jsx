import React from "react";
import { Card, Row, Col } from "react-bootstrap";

export const Resultados = ({ metricas }) => {
  // Desestructuramos las tres métricas específicas con valores por defecto
  const {
    clientesRechazados = 0,
    tiempoPromedioTaller = 0,
    productividadTecnico = 0
  } = metricas || {};

  return (
    <Card className="shadow-sm my-4 border-0">
      <Card.Header as="h3" className="bg-dark text-white text-center py-3">
        📊 Métricas de Desempeño del Taller i-Fix
      </Card.Header>
      <Card.Body className="bg-light p-4">
        <Row className="text-center g-4">
          
          {/* Métrica 1: Clientes rechazados por el cierre */}
          <Col md={4}>
            <Card className="h-100 border-0 shadow-sm custom-card-hover">
              <Card.Body className="d-flex flex-column justify-content-center py-4">
                <Card.Title className="text-secondary font-weight-bold mb-3" style={{ fontSize: '1.1rem' }}>
                  Clientes Rechazados por Cierre
                </Card.Title>
                <Card.Text className="display-5 text-danger font-weight-bold m-0">
                  {clientesRechazados}
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          
          {/* Métrica 2: Tiempo promedio de un equipo en taller */}
          <Col md={4}>
            <Card className="h-100 border-0 shadow-sm custom-card-hover">
              <Card.Body className="d-flex flex-column justify-content-center py-4">
                <Card.Title className="text-secondary font-weight-bold mb-3" style={{ fontSize: '1.1rem' }}>
                  Tiempo Promedio en Taller
                </Card.Title>
                <Card.Text className="display-5 text-primary font-weight-bold m-0">
                  {tiempoPromedioTaller.toFixed(2)} <span style={{ fontSize: '1.5rem' }}>min</span>
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          
          {/* Métrica 3: Productividad del técnico */}
          <Col md={4}>
            <Card className="h-100 border-0 shadow-sm custom-card-hover">
              <Card.Body className="d-flex flex-column justify-content-center py-4">
                <Card.Title className="text-secondary font-weight-bold mb-3" style={{ fontSize: '1.1rem' }}>
                  Productividad del Técnico
                </Card.Title>
                <Card.Text className="display-5 text-success font-weight-bold m-0">
                  {productividadTecnico.toFixed(1)}<span style={{ fontSize: '1.5rem' }}>%</span>
                </Card.Text>
                <small className="text-muted mt-2">
                  Porcentaje de tiempo en estado 'Reparando'
                </small>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
};

export default Resultados;

