from app.models.ordem_servico import Ordem_servico
from app.models.servico import Servico


class Ordem_servico_servico:
    def __init__(self, id, valor_cobrado, id_servico=None, id_ordem_servico=None):
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
    def valor_cobrado(self):
        return self._valor_cobrado

    @property
    def id_ordem_servico(self):
        return self._id_ordem_servico

    @property
    def id_servico(self):
        return self._id_servico