import axios from "./axios.config.js";

const obtenerTodos = async () => {
  const response = await axios.get("/juegos");
  return response.data;
};

// getPorId Obtiene un juego por su ID
const obtenerPorId = async (id) => {
  const response = await axios.get(`/juegos/${id}`);
  return response.data;
};

// post Sirve para crear un nuevo juego en el backend.
const crear = async (juego) => {
  
  const response = await axios.post("/juegos", juego); // el método POST se usa para crear 🔧 nuevos recursos en el backend.
  return response.data;
};

// put Actualizar (todo el objeto)
const actualizar = async (id, juego) => {
  const response = await axios.put(`/juegos/${id}`, juego);
  return response.data;
};

// delete Eliminar un juego por su ID
const eliminar = async (id) => {
  await axios.delete(`/juegos/${id}`);
};

const getUltimosEstrenos = async () => {
  const response = await axios.get("/juegos/top/ultimos");
  return response.data;
};

const getMasPopulares = async () => {
  const response = await axios.get("/juegos/top/populares");
  return response.data;
};

const buscarFiltrado = async (filtros) => {
  const params = new URLSearchParams(filtros).toString();
  const response = await axios.get(`/juegos/filtrar?${params}`);
  return response.data;
};
//ejemplo
// const filtros = {
//   texto: "FIFA",
//   idPlataforma: 2,
//   codigoEsrb: "E"
// };

// new URLSearchParams(filtros).toString(); // Esto convierte ese objeto en una cadena de parámetros de URL.
// texto=FIFA&idPlataforma=2&codigoEsrb=E

//Agregar un nuevo filtro por clasificación ESRB en el formulario de filtros (como select).
const contarFiltrado = async (filtros) => {
  const params = new URLSearchParams(filtros).toString();
  const response = await axios.get(`/juegos/filtrar/contar?${params}`);
  return response.data.cantidad;
};

export default {
  obtenerTodos,
  obtenerPorId,
  crear,
  actualizar,
  eliminar,
  getUltimosEstrenos,
  getMasPopulares,
  buscarFiltrado,
  contarFiltrado,
};
