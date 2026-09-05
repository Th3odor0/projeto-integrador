from app.models.ordens_servico import Orden_servico
from app.models.servico import Servico

class Ordem_servico_servico:
    def __init__(self, id, valor_cobrado, id_servico=Servico, id_ordem_servico=Orden_servico):
        self._id = id
        self._valor_cobrado = valor_cobrado
        self._id_servico = id_servico 
        self._id_ordem_servico = id_ordem_servico

    def atualizar_dados(self, novo_valor_cobrado):
        self._valor_cobrado = novo_valor_cobrado

    @property
    def id(self):
        return self._id
    @property 
    def id_ordem_servico(self):
        return self._id_ordem_servico
    @property
    def id_servico(self):
        return self._id_servico