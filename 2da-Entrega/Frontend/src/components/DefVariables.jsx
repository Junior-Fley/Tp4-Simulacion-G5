import React from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import FloatingLabel from "react-bootstrap/FloatingLabel";
import Button from "react-bootstrap/Button";
import { useState } from "react";

export const DefVariables = ({ onSendData }) => {
  const [formDatos, setFormDatos] = useState({
    LlegadaCTS1: 25,
    CantiSerTS1: 3,
    TasaLlegadaTS1: 10,
    LlegadaCTS2: 15,
    CantiSerTS2: 2,
    TasaLlegadaTS2: 7,
    LlegadaCTS3: 30,
    CantiSerTS3: 3,
    TasaLlegadaTS3: 18,
    LlegadaCTS4: 10,
    CantiSerTS4: 2,
    TasaLlegadaTS4: 5,
    LlegadaCTS5: 8,
    CantiSerTS5: 1,
    TasaLlegadaTS5: 3,
  });

  console.log(formDatos);

  const handleChange = (e) => {
    setFormDatos({
      ...formDatos,
      [e.target.name]: parseInt(e.target.value),
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSendData(formDatos);
  };

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <Row>
          <Col>
            <Form.Label>Envio Paquetes:</Form.Label>
            <FloatingLabel
              controlId="floatingInput"
              label="Llegada clientes por hora"
              className="mb-3"
            >
              <Form.Control
                type="number"
                name="LlegadaCTS1"
                onChange={handleChange}
              />
            </FloatingLabel>
            <FloatingLabel
              controlId="floatingInput"
              label="Cantidad Servidores"
              className="mb-3"
            >
              <Form.Control
                name="CantiSerTS1"
                type="number"
                onChange={handleChange}
              />
            </FloatingLabel>
            <FloatingLabel
              controlId="floatingInput"
              label="Tasa Llegada Clientes "
              className="mb-3"
            >
              <Form.Control
                name="TasaLlegadaTS1"
                type="number"
                onChange={handleChange}
              />
            </FloatingLabel>
          </Col>

          <Col>
            <Form.Label>Reclamos y Devoluciones</Form.Label>
            <FloatingLabel
              controlId="floatingInput"
              label="Llegada clientes por hora"
              className="mb-3"
            >
              <Form.Control
                type="number"
                name="LlegadaCTS2"
                onChange={handleChange}
              />
            </FloatingLabel>
            <FloatingLabel
              controlId="floatingInput"
              label="Cantidad Servidores"
              className="mb-3"
            >
              <Form.Control
                type="number"
                name="CantiSerTS2"
                onChange={handleChange}
              />
            </FloatingLabel>
            <FloatingLabel
              controlId="floatingInput"
              label="Tasa Llegada Clientes "
              className="mb-3"
            >
              <Form.Control
                type="number"
                placeholder="TasaLlegadaTS2"
                onChange={handleChange}
              />
            </FloatingLabel>
          </Col>

          <Col>
            <Form.Label>Venta de Sellos y Sobres</Form.Label>
            <FloatingLabel
              controlId="floatingInput"
              label="Llegada clientes por hora"
              className="mb-3"
            >
              <Form.Control
                type="number"
                name="LlegadaCTS3"
                onChange={handleChange}
              />
            </FloatingLabel>
            <FloatingLabel
              controlId="floatingInput"
              label="Cantidad Servidores"
              className="mb-3"
            >
              <Form.Control
                type="number"
                name="CantiSerTS3"
                onChange={handleChange}
              />
            </FloatingLabel>
            <FloatingLabel
              controlId="floatingInput"
              label="Tasa Llegada Clientes "
              className="mb-3"
            >
              <Form.Control
                type="number"
                name="TasaLlegadaTS3"
                onChange={handleChange}
              />
            </FloatingLabel>
          </Col>

          <Col>
            <Form.Label>Atención Empresarial</Form.Label>
            <FloatingLabel
              controlId="floatingInput"
              label="Llegada clientes por hora"
              className="mb-3"
            >
              <Form.Control
                type="number"
                name="LlegadaCTS4"
                onChange={handleChange}
              />
            </FloatingLabel>
            <FloatingLabel
              controlId="floatingInput"
              label="Cantidad Servidores"
              className="mb-3"
            >
              <Form.Control
                type="number"
                name="CantiSerTS4"
                onChange={handleChange}
              />
            </FloatingLabel>
            <FloatingLabel
              controlId="floatingInput"
              label="Tasa Llegada Clientes "
              className="mb-3"
            >
              <Form.Control
                type="number"
                name="TasaLlegadaTS4"
                onChange={handleChange}
              />
            </FloatingLabel>
          </Col>

          <Col>
            <Form.Label style={{ whiteSpace: "nowrap" }}>
              Postales y Envios Especiales
            </Form.Label>
            <FloatingLabel
              controlId="floatingInput"
              label="Llegada clientes por hora"
              className="mb-3"
            >
              <Form.Control
                type="number"
                name="LlegadaCTS5"
                onChange={handleChange}
              />
            </FloatingLabel>
            <FloatingLabel
              controlId="floatingInput"
              label="Cantidad Servidores"
              className="mb-3"
            >
              <Form.Control
                type="number"
                name="CantiSerTS5"
                onChange={handleChange}
              />
            </FloatingLabel>
            <FloatingLabel
              controlId="floatingInput"
              label="Tasa Llegada Clientes "
              className="mb-3"
            >
              <Form.Control
                type="number"
                name="TasaLlegadaTS5"
                onChange={handleChange}
              />
            </FloatingLabel>
          </Col>
        </Row>
        <Button variant="outline-success" type="submit">
          Simular
        </Button>
      </Form>
    </>
  );
};
