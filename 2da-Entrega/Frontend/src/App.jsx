import { useState } from "react";
import "./App.css";
import { VectorEstado } from "./components/vectorEstado";
import { DefVariables } from "./components/defVariables";
import { Container } from "react-bootstrap";
import { Resultados } from "./components/Resultados";

function App() {
  const [formData, setFormData] = useState(null);

  const handleDataFromVariables = (data) => {
    setFormData(data);
    console.log("datos en App", data);
  };
  
  return (
    <>
      <Container className="text-center">
        <div
          style={{
            position: "relative",
            textAlign: "center",
            width: "90%",
            left: "5%",
            top: "0%",
          }}
        >
          <h1>Service de Tecnología "i-Fix"</h1>

          <DefVariables onSendData={handleDataFromVariables}>

          </DefVariables>
        </div>

        <div style={{ position: "relative", width: "100%",
            textAlign: "center",
            overflowX: "auto",
          }}
        >
          <VectorEstado></VectorEstado>
        </div>

        <div style={{ position: "relative", width: "90%", left: "5%" }}>
          <Resultados></Resultados>
        </div>
      </Container>
    </>
  );
}

export default App
