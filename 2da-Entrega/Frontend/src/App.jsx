
import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PiePagina from "./components/PiePagina";

import DefVariables from "./pages/DefVariables";
import { VectorEstado } from "./pages/VectorEstado";

function App() {
  const [simId, setSimId] = useState(() => localStorage.getItem("simId") || "");

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <DefVariables
              onSimulacionCreada={(nuevoId) => {
                const id = nuevoId == null ? "" : String(nuevoId);
                setSimId(id);
              }}
            />
          }
        />
      </Routes>
      <VectorEstado
        key={simId || "__sin_sim__"}
        simId={simId}
        onSimIdChange={(nuevoId) => {
          const id = nuevoId == null ? "" : String(nuevoId);
          setSimId(id);
        }}
      />
      <PiePagina />
      
    </BrowserRouter>
  );
}

export default App;
