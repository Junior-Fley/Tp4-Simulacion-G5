import axios from "./axios.config.js";

// post.
const iniciarSimulacion = async (simulacion) => {
  
  const response = await axios.post("/simulaciones", simulacion); // el método POST se usa para crear 🔧 nuevos recursos en el backend.
  return response.data;
};

// get.
const listarSimulaciones = async () => {
  const response = await axios.get("/simulaciones");
  return response.data;
};

const obtenerStats = async (sim_id) => {
  const response = await axios.get(`/simulaciones/${sim_id}/stats`);
  return response.data;
};

const obtenerListasFilas = async (sim_id, page, size) => {
  const response = await axios.get(`/simulaciones/${sim_id }/filas?page=${page}&size=${size}`);
  return response.data;
};

const listarFilasFiltradas = async (sim_id, hora_min, page = 1, size = 20) => {
  const response = await axios.get("/simulaciones/filtros", {
    params: {
      sim_id,
      hora_min,
      page,
      size,
    },
  });
  return response.data;
};




export default {
  obtenerListasFilas, 
  iniciarSimulacion,
  listarSimulaciones,
  obtenerStats,
  listarFilasFiltradas,

};
