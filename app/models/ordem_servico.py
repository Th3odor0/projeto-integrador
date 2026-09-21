class Ordem_servico:
    STATUS_PERMITIDOS = ["aberta", "em andamento", "concluida", "cancelada"]

    def __init__(self,
                 data_entrada,
                 data_conclusao,
                 status,
                 problema,
                 diagnostico,
                 valor_total,
                 forma_pagamento,
                 dias_garantia,
                 cliente,
                 funcionario,
                 equipamento,
                 id=None):
        self._id = id
        self._data_entrada = data_entrada
        self._data_conclusao = data_conclusao
        self.status = status  # passa pela validação do setter
        self._problema = problema
        self._diagnostico = diagnostico
        self._valor_total = valor_total
        self._forma_pagamento = forma_pagamento
        self._dias_garantia = dias_garantia
        self._cliente = cliente
        self._funcionario = funcionario
        self._equipamento = equipamento

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
        self.status = novo_status  # passa pela validação do setter
        self._problema = novo_problema
        self._diagnostico = novo_diagnostico
        self._valor_total = novo_valor
        self._forma_pagamento = novo_pagamento
        self._dias_garantia = nova_garantia

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, novo_id):
        self._id = novo_id

    @property
    def cliente(self):
        return self._cliente

    @property
    def funcionario(self):
        return self._funcionario

    @property
    def equipamento(self):
        return self._equipamento

    @property
    def data_entrada(self):
        return self._data_entrada

    @property
    def data_conclusao(self):
        return self._data_conclusao

    @property
    def problema(self):
        return self._problema

    @property
    def diagnostico(self):
        return self._diagnostico

    @property
    def valor_total(self):
        return self._valor_total

    @property
    def forma_pagamento(self):
        return self._forma_pagamento

    @property
    def dias_garantia(self):
        return self._dias_garantia

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, novo_status):
        if novo_status not in self.STATUS_PERMITIDOS:
            raise ValueError(f"Status inválido: {novo_status}")
        self._status = novo_status