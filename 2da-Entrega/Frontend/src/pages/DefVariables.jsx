import { useForm } from "react-hook-form";
import { useState } from "react";
import "../App.css";

import simulacionService from "../service/simulacion.service";

const FormularioVar = () => {
  const [mensaje, setMensaje] = useState("");
  const [tipoMensaje, setTipoMensaje] = useState("");
  const [cargando, setCargando] = useState(false);


  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      x_tiempo: 45,
      i_iteraciones: 1000,
      hora_inicio: "10:00",
    },
  });

  const onSubmit = async (data) => {

    // separar horas y minutos
    const [horas, minutos] = data.hora_inicio.split(":");

    // convertir a minutos totales
    const totalMinutos =
      Number(horas) * 60 +
      Number(minutos);

    const parsed = {

      x_tiempo: Number(data.x_tiempo),

      i_iteraciones: Number(data.i_iteraciones),

      j_hora_inicio: totalMinutos,

    };

    console.log(parsed);

    try {

  setCargando(true);

  const response =
    await simulacionService.iniciarSimulacion(parsed);

  console.log("ver: ", response);

  // guardar id
  localStorage.setItem(
    "simId",
    response.id_simulacion
  );

  // guardar lista de simulaciones
  const sims =
    JSON.parse(localStorage.getItem("simulaciones")) || [];

  sims.push({
    id: response.id_simulacion,
  });

  localStorage.setItem(
    "simulaciones",
    JSON.stringify(sims)
  );

  setMensaje("Simulación generada correctamente");

  setTipoMensaje("success");

  // refrescar pantalla automáticamente
  window.location.reload();

} catch (error) {

  console.error(
    "Error al iniciar simulación:",
    error
  );

  setMensaje(
    "Error al generar la simulación"
  );

  setTipoMensaje("danger");

} finally {

  setCargando(false);

}


  };

  const campo = (
    label,
    name,
    type = "number",
    rules = {}
  ) => (

    <div className="mb-3">

      <label className="form-label">
        {label}
      </label>

      <input
        type={type}
        step="any"
        className={`form-control ${
          errors[name] ? "is-invalid" : ""
        }`}
        {...register(name, {
          required: "Campo obligatorio",
          ...rules,
        })}
      />

      {errors[name] && (
        <span className="invalid-feedback">
          {errors[name].message}
        </span>
      )}

    </div>
  );

  return (

    <main className="container mt-5">

  <div className="sim-card">

    <h4 className="sim-title">
      Iniciar Simulación
    </h4>

    {mensaje && (
      <div className={`alert alert-${tipoMensaje}`}>
        {mensaje}
      </div>
    )}

    <form onSubmit={handleSubmit(onSubmit)} className="sim-form">

      <div className="sim-row">

        {campo(
          "Tiempo de Simulación",
          "x_tiempo",
          "number",
          {
            min: { value: 1, message: "Mínimo 1" },
          }
        )}

        {campo(
          "Cantidad de iteraciones",
          "i_iteraciones",
          "number",
          {
            min: { value: 1, message: "Mínimo 1" },
          }
        )}

        {campo(
          "Hora de inicio",
          "hora_inicio",
          "time"
        )}

      </div>

      <div className="sim-actions">
        <button
          type="submit"
          className="btn btn-primary sim-btn"
          disabled={cargando}
        >
          {cargando ? "Generando..." : "Simular"}
        </button>
      </div>

    </form>

  </div>

</main>
  );
};

export default FormularioVar;