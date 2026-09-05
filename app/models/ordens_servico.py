from app.models.clientes import Cliente
from app.models.funcionarios import Funcionario
from app.models.equipamentos import Equipamento

class Ordem_servico:
    def __init__(self,
                 id,
                 data_entrada,
                 data_conclusao,
                 status,
                 problema,
                 diagnostigo,
                 valor_total,
                 forma_pagamento,
                 dias_garantia,
                 id_cliente=Cliente,
                 id_funcionarios=Funcionario,
                 id_equipamentos=Equipamento):
        self._id = id
        self._data_entrada = data_entrada
        self._data_conclusao = data_conclusao 
        self._status = status
        self._problema = problema
        self._diagnostico = diagnostigo
        self._valor_total = valor_total
        self._forma_pagamento = forma_pagamento
        self._dias_garantia = dias_garantia 
        self._id_cliente = id_cliente
        self._id_funcionarios = id_funcionarios 
        self._id_equipamentos = id_equipamentos

    def atualizar_dados(self,
                        nova_entrada,
                        nova_conclusao,
                        novo_status, 
                        novo_problema,
                        novo_diagnostico,
                        novo_valor,
                        novo_pagamento,
                        nova_garantia):
        self._data_entrada = nova_entrada
        self._data_conclusao = nova_conclusao
        self._status = novo_status
        self._problema = novo_problema
        self._diagnostico = novo_diagnostico 
        self._valor_total = novo_valor
        self._forma_pagamento = novo_pagamento
        self._dias_garantia = nova_garantia


    @property
    def id(self):
        return self._id
    @property
    def id_cliente(self):
        return self._id_cliente
    @property
    def id_funcionario(self):
        return self._id_funcionarios
    @property
    def id_equipamentos(Self):
        Self._id_equipamentos
    

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, novo_status):
        permitidos = ["aberta", "em andamento", "concluida", "cancelada"]
        if novo_status not in permitidos:
            raise ValueError(f"Status inválido: {novo_status}")
        self._status = novo_status