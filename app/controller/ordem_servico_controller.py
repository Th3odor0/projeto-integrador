from datetime import datetime
from app.core.idioma import t
from app.models.ordem_servico import Ordem_servico
from app.core.dataUltils import DataUtils


class Ordem_servico_Controller:
    def __init__(self, ordem_servico_dao, cliente_dao, funcionario_dao, equipamento_dao):
        self.ordem_servico_dao = ordem_servico_dao
        self.cliente_dao = cliente_dao
        self.funcionario_dao = funcionario_dao
        self.equipamento_dao = equipamento_dao

    @staticmethod
    def _so_data(valor):
        """
        As colunas data_entrada / data_conclusao são DATETIME no banco, mas a
        tela trabalha com datas (dd/mm/aaaa). Comparar date com datetime dá
        TypeError, então normalizamos tudo para date antes de comparar.
        """
        if isinstance(valor, datetime):
            return valor.date()
        return valor

    @staticmethod
    def _validar_valor_total(valor_total):
        try:
            valor_total = float(valor_total)
        except (TypeError, ValueError):
            raise ValueError(t("Valor total precisa ser um número."))

        if valor_total < 0:
            raise ValueError(t("Valor total não pode ser negativo."))

        return valor_total

    @staticmethod
    def _validar_dias_garantia(dias_garantia):
        if dias_garantia is None or str(dias_garantia).strip() == "":
            return 0

        try:
            dias_garantia = int(dias_garantia)
        except (TypeError, ValueError):
            raise ValueError(t("Dias de garantia precisa ser um número inteiro."))

        if dias_garantia < 0:
            raise ValueError(t("Dias de garantia não pode ser negativo."))

        return dias_garantia

    @staticmethod
    def _validar_data_conclusao(data_conclusao_texto):
        if not data_conclusao_texto:
            return None

        if not DataUtils.validar_data(data_conclusao_texto):
            raise ValueError(t("Data de conclusão inválida. Use o formato dd/mm/aaaa."))

        return DataUtils.string_para_data(data_conclusao_texto)

    def _checar_datas(self, data_entrada, data_conclusao):
        if data_conclusao is None or data_entrada is None:
            return
        if self._so_data(data_conclusao) < self._so_data(data_entrada):
            raise ValueError("Data de conclusão não pode ser anterior à data de entrada.")

    def _buscar_entidades_relacionadas(self, id_cliente, id_funcionario, id_equipamento):
        """Busca cliente/funcionário/equipamento e garante que todos existem.
        As três colunas (cliente_id, funcionario_id, equipamento_id) são
        NOT NULL no banco, então id vazio também é erro aqui."""
        if id_cliente is None:
            raise ValueError("Selecione o cliente.")
        if id_funcionario is None:
            raise ValueError("Selecione o funcionário.")
        if id_equipamento is None:
            raise ValueError("Selecione o equipamento.")

        cliente = self.cliente_dao.get_by_id(id_cliente)
        if cliente is None:
            raise ValueError(f"Cliente com id {id_cliente} não encontrado.")

        funcionario = self.funcionario_dao.get_by_id(id_funcionario)
        if funcionario is None:
            raise ValueError(f"Funcionário com id {id_funcionario} não encontrado.")

        equipamento = self.equipamento_dao.get_by_id(id_equipamento)
        if equipamento is None:
            raise ValueError(f"Equipamento com id {id_equipamento} não encontrado.")

        return cliente, funcionario, equipamento

    def cadastrar(self, id_cliente, id_funcionario, id_equipamento, data_entrada_texto,
                  data_conclusao_texto, status, problema, diagnostico,
                  valor_total, forma_pagamento, dias_garantia):

        if not problema or not problema.strip():
            raise ValueError("O campo 'problema' é obrigatório.")

        # coluna `problema` é VARCHAR(255)
        if len(problema.strip()) > 255:
            raise ValueError("O problema deve ter no máximo 255 caracteres.")

        if not data_entrada_texto or not str(data_entrada_texto).strip():
            raise ValueError(t("A data de entrada é obrigatória."))

        if not DataUtils.validar_data(data_entrada_texto):
            raise ValueError(
                t("Data de entrada inválida: {data}. Use o formato dd/mm/aaaa.", data=repr(data_entrada_texto))
            )

        data_conclusao = self._validar_data_conclusao(data_conclusao_texto)
        valor_total = self._validar_valor_total(valor_total)
        dias_garantia = self._validar_dias_garantia(dias_garantia)

        data_entrada = DataUtils.string_para_data(data_entrada_texto)
        self._checar_datas(data_entrada, data_conclusao)

        cliente, funcionario, equipamento = self._buscar_entidades_relacionadas(
            id_cliente, id_funcionario, id_equipamento
        )

        nova_ordem = Ordem_servico(
            id=None,
            data_entrada=data_entrada,
            data_conclusao=data_conclusao,
            status=status,
            problema=problema.strip(),
            diagnostico=diagnostico,
            valor_total=valor_total,
            forma_pagamento=forma_pagamento,
            dias_garantia=dias_garantia,
            cliente=cliente,
            funcionario=funcionario,
            equipamento=equipamento
        )

        return self.ordem_servico_dao.save(nova_ordem)

    def listar_todas(self):
        return self.ordem_servico_dao.get_all()

    def buscar_por_id(self, id):
        ordem = self.ordem_servico_dao.get_by_id(id)
        if ordem is None:
            raise ValueError(t("Ordem de serviço com id {id} não encontrada.", id=id))
        return ordem

    def atualizar(self, id, id_cliente, id_funcionario, id_equipamento, status,
                  data_conclusao_texto, problema, diagnostico,
                  valor_total, forma_pagamento, dias_garantia):
        """
        Atualização da ordem. Cliente, funcionário e equipamento são editáveis;
        só a data de entrada continua vindo da ordem original.
        """
        ordem = self.buscar_por_id(id)

        if not problema or not problema.strip():
            raise ValueError("O campo 'problema' é obrigatório.")

        if len(problema.strip()) > 255:
            raise ValueError("O problema deve ter no máximo 255 caracteres.")

        data_conclusao = self._validar_data_conclusao(data_conclusao_texto)
        valor_total = self._validar_valor_total(valor_total)
        dias_garantia = self._validar_dias_garantia(dias_garantia)

        self._checar_datas(ordem.data_entrada, data_conclusao)

        cliente, funcionario, equipamento = self._buscar_entidades_relacionadas(
            id_cliente, id_funcionario, id_equipamento
        )

        ordem.atualizar_dados(
            nova_entrada=ordem.data_entrada,
            nova_conclusao=data_conclusao,
            novo_status=status,
            novo_problema=problema.strip(),
            novo_diagnostico=diagnostico,
            novo_valor=valor_total,
            novo_pagamento=forma_pagamento,
            nova_garantia=dias_garantia
        )
        # atualizar_dados não cobre cliente/funcionario/equipamento
        ordem.cliente = cliente
        ordem.funcionario = funcionario
        ordem.equipamento = equipamento

        return self.ordem_servico_dao.update(ordem)

    def excluir(self, id):
        self.buscar_por_id(id)
        self.ordem_servico_dao.delete(id)