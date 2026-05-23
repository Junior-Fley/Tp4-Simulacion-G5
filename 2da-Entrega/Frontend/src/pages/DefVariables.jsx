import { useForm } from "react-hook-form";

const FormularioVar = ({ onSimular }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      cantidadSimulaciones: 1000,
      mediaLlegadas: 45,
      atencionMin: 10,
      atencionMax: 20,
      mediaReparacion: 90,
      probPresupuestoElevado: 0.3,
      probCompraPresupuestoElevado: 0.5,
      horaApertura: 10,
      horaCierre: 18,
    },
  });

  const onSubmit = (data) => {
    // Convertir strings a números
    const parsed = {
      cantidadSimulaciones:        Number(data.cantidadSimulaciones),
      mediaLlegadas:               Number(data.mediaLlegadas),
      atencionMin:                 Number(data.atencionMin),
      atencionMax:                 Number(data.atencionMax),
      mediaReparacion:             Number(data.mediaReparacion),
      probPresupuestoElevado:      Number(data.probPresupuestoElevado),
      probCompraPresupuestoElevado:Number(data.probCompraPresupuestoElevado),
      horaApertura:                Number(data.horaApertura),
      horaCierre:                  Number(data.horaCierre),
    };
    console.log(parsed);
    onSimular?.(parsed); // llama al padre si existe
  };

  const campo = (label, name, rules = {}) => (
    <div className="mb-3">
      <label className="form-label">{label}</label>
      <input
        type="number"
        step="any"
        className={`form-control ${errors[name] ? "is-invalid" : ""}`}
        {...register(name, { required: "Campo obligatorio", ...rules })}
      />
      {errors[name] && (
        <span className="invalid-feedback">{errors[name].message}</span>
      )}
    </div>
  );

  return (
    <main className="container mt-5">
      <h4 className="mb-4">Parámetros de simulación</h4>
      <form onSubmit={handleSubmit(onSubmit)}>
        {campo("Cantidad de simulaciones",          "cantidadSimulaciones",        { min: { value: 1, message: "Mínimo 1" } })}
        {campo("Media de llegadas (min)",           "mediaLlegadas")}
        {campo("Atención mínima (min)",             "atencionMin")}
        {campo("Atención máxima (min)",             "atencionMax")}
        {campo("Media de reparación (min)",         "mediaReparacion")}
        {campo("Prob. presupuesto elevado (0-1)",   "probPresupuestoElevado",      { min: 0, max: 1 })}
        {campo("Prob. compra si presupuesto alto (0-1)", "probCompraPresupuestoElevado", { min: 0, max: 1 })}
        {campo("Hora de apertura",                  "horaApertura",                { min: 0, max: 23 })}
        {campo("Hora de cierre",                    "horaCierre",                  { min: 0, max: 23 })}

        <button type="submit" className="btn btn-primary mt-2">
          Simular
        </button>
      </form>
    </main>
  );
};

export default FormularioVar;