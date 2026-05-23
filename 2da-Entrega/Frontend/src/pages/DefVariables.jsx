import { useForm } from "react-hook-form";
import simulacionService from "../service/simulacion.service";

const FormularioVar = () => {

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      x_tiempo: 45,
      i_iteraciones: 1000,
      j_hora_inicio: 600,
    },
  });

  const onSubmit = async (data) => {

    const parsed = {

      x_tiempo: Number(data.x_tiempo),

      i_iteraciones: Number(data.i_iteraciones),

      j_hora_inicio: Number(data.j_hora_inicio),

    };

    console.log(parsed);

    try {

      const response = await simulacionService.iniciarSimulacion(parsed);

      console.log(response);

      // guardar id de la simulación creada
      localStorage.setItem("simId", response.id);

      // refrescar
      window.location.reload();

    } catch (error) {

      console.error("Error al iniciar simulación:", error);

    }
  };

  const campo = (label, name, rules = {}) => (

    <div className="mb-3">

      <label className="form-label">
        {label}
      </label>

      <input
        type="number"
        step="any"
        className={`form-control ${errors[name] ? "is-invalid" : ""}`}
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

      <h4 className="mb-4">
        Iniciar Simulación
      </h4>

      <form onSubmit={handleSubmit(onSubmit)}>

        {campo(
          "Tiempo entre llegadas",
          "x_tiempo",
          {
            min: {
              value: 1,
              message: "Mínimo 1",
            },
          }
        )}

        {campo(
          "Cantidad de iteraciones",
          "i_iteraciones",
          {
            min: {
              value: 1,
              message: "Mínimo 1",
            },
          }
        )}

        {campo(
          "Hora de inicio (en minutos)",
          "j_hora_inicio",
          {
            min: {
              value: 0,
              message: "Mínimo 0",
            },
          }
        )}

        <button
          type="submit"
          className="btn btn-primary mt-2"
        >
          Simular
        </button>

      </form>

    </main>
  );
};

export default FormularioVar;