from app.models.ordem_servico import Ordem_servico
from app.models.pecas import Peca

class Ordem_servico_peca:
    def __init__(self,
                 id,
                 quantidade,
                 valor_unitario,
                 id_ordem_servico=Ordem_servico,
                 id_peca=Peca):
        self._id = id
        self._quantidade = quantidade
        self._valor_unitario = valor_unitario
        self._id_ordem_servico = id_ordem_servico
        self._id_peca = id_peca

    def atualizar_dados(self, nova_quantidade, novo_valor):
        self._quantidade = nova_quantidade 
        self._valor_unitario = novo_valor

    @property
    def id(self):
        return self._id
    @property
    def id_ordem_servico(self):
        return self._id_ordem_servico
    @property
    def id_peca(self):
        return self._id_peca
    