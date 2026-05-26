from app.domain.models.EstadoCliente import EstadoCliente


class Cliente:
    def __init__(self, id_cliente: int, estado: EstadoCliente):
        self.id_cliente: int = id_cliente
        self.estado: str = estado.value
