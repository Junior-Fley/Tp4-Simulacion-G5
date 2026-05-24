
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Encabezado from "./components/Encabezado";
import PiePagina from "./components/PiePagina";

import DefVariables from "./pages/DefVariables";
import { VectorEstado } from "./pages/VectorEstado";
import Resultados from "./pages/Resultados";

function App() {
  return (
    <BrowserRouter>
      {/* <Encabezado /> */}
      <Routes>
        <Route path="/" element={<DefVariables />} />
      </Routes>
      <VectorEstado />
      <PiePagina />
      
    </BrowserRouter>
  );
}

export default App;
