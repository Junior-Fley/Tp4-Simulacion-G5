from app.domain.models.event.Evento import Evento

class AbreTienda(Evento):
    def __init__(self):
        super().__init__("Abre_Tienda")
