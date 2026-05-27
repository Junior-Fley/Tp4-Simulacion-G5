import { useForm } from "react-hook-form";
import { useState } from "react";
import "../App.css";

import simulacionService from "../service/simulacion.service";

const FormularioVar = ({ onSimulacionCreada }) => {
  const [mensaje, setMensaje] = useState("");
  const [tipoMensaje, setTipoMensaje] = useState("");
  const [cargando, setCargando] = useState(false);


  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      x_tiempo: 2500,
      i_iteraciones: 1000,
      hora_inicio: "10:00",
      media_llegada: 45,
      min_atencion: 10,
      max_atencion: 20,
      media_reparacion: 90,
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
      media_llegada: Number(data.media_llegada),
      min_atencion: Number(data.min_atencion),
      max_atencion: Number(data.max_atencion),
      media_reparacion: Number(data.media_reparacion),
    };

    if (parsed.min_atencion > parsed.max_atencion) {
      setMensaje("El mínimo de atención no puede ser mayor que el máximo");
      setTipoMensaje("danger");
      return;
    }

    console.log(parsed);

    try {

  setCargando(true);

  const response = await simulacionService.iniciarSimulacion(parsed);

  console.log("ver: ", response);

  const nuevoId = response?.id_simulacion;

  // guardar id
  if (nuevoId != null) {
    localStorage.setItem("simId", String(nuevoId));
  }

  setMensaje("Simulación generada correctamente");

  setTipoMensaje("success");

  // Notificar al resto de la UI para que cargue la tabla de esta simulación
  if (typeof onSimulacionCreada === "function" && nuevoId != null) {
    onSimulacionCreada(nuevoId);
  }

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
    rules = {},
    icon = ""
  ) => (

    <div className="mb-3">

      <label className="form-label">
        {icon && <i className={`bi ${icon}`}></i>}
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
      <i className="bi bi-cpu"></i> Parámetros del Simulador
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
          },
          "bi-clock-history"
        )}

        {campo(
          "Cantidad de iteraciones",
          "i_iteraciones",
          "number",
          {
            min: { value: 1, message: "Mínimo 1" },
          },
          "bi-arrow-repeat"
        )}

        {campo(
          "Hora de inicio",
          "hora_inicio",
          "time",
          {},
          "bi-hourglass-split"
        )}

        {campo(
          "Media entre llegadas (min)",
          "media_llegada",
          "number",
          {
            min: { value: 0.000001, message: "Debe ser mayor a 0" },
          },
          "bi-people"
        )}

        {/* Distribución uniforme: atención */}
        <div className="mb-3">
          <label className="form-label">
            <i className="bi bi-stopwatch me-1"></i>
            Distribución uniforme de atención (min)
          </label>

          <div className="row g-2">
            <div className="col-6">
              <input
                type="number"
                step="any"
                placeholder="Mín"
                className={`form-control ${errors.min_atencion ? "is-invalid" : ""}`}
                {...register("min_atencion", {
                  required: "Campo obligatorio",
                  min: { value: 0.000001, message: "Debe ser mayor a 0" },
                })}
              />

              {errors.min_atencion && (
                <span className="invalid-feedback">
                  {errors.min_atencion.message}
                </span>
              )}
            </div>

            <div className="col-6">
              <input
                type="number"
                step="any"
                placeholder="Máx"
                className={`form-control ${errors.max_atencion ? "is-invalid" : ""}`}
                {...register("max_atencion", {
                  required: "Campo obligatorio",
                  min: { value: 0.000001, message: "Debe ser mayor a 0" },
                })}
              />

              {errors.max_atencion && (
                <span className="invalid-feedback">
                  {errors.max_atencion.message}
                </span>
              )}
            </div>
          </div>
        </div>

        {campo(
          "Media reparación (min)",
          "media_reparacion",
          "number",
          {
            min: { value: 0.000001, message: "Debe ser mayor a 0" },
          },
          "bi-wrench-adjustable"
        )}

      </div>

      <div className="sim-actions">
        <button
          type="submit"
          className="btn btn-primary sim-btn"
          disabled={cargando}
        >
          {cargando ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Generando...
            </>
          ) : (
            <>
              <i className="bi bi-play-fill"></i> Simular
            </>
          )}
        </button>
      </div>

    </form>

  </div>

</main>
  );
};

export default FormularioVar;