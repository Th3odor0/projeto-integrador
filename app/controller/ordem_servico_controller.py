from app.models.ordem_servico import Ordem_servico
from app.core.dataUltils import DataUtils


class Ordem_servico_Controller:
    def __init__(self, ordem_servico_dao, cliente_dao, funcionario_dao, equipamento_dao):
        self.ordem_servico_dao = ordem_servico_dao
        self.cliente_dao = cliente_dao
        self.funcionario_dao = funcionario_dao
        self.equipamento_dao = equipamento_dao

    # ------------------------------------------------------------------
    # Validações reaproveitadas por cadastrar() e atualizar()
    # ------------------------------------------------------------------

    @staticmethod
    def _validar_valor_total(valor_total):
        try:
            valor_total = float(valor_total)
        except (TypeError, ValueError):
            raise ValueError("Valor total precisa ser um número.")

        if valor_total < 0:
            raise ValueError("Valor total não pode ser negativo.")

        return valor_total

    @staticmethod
    def _validar_dias_garantia(dias_garantia):
        # Campo opcional: vazio vira 0
        if dias_garantia is None or str(dias_garantia).strip() == "":
            return 0

        try:
            dias_garantia = int(dias_garantia)
        except (TypeError, ValueError):
            raise ValueError("Dias de garantia precisa ser um número inteiro.")

        if dias_garantia < 0:
            raise ValueError("Dias de garantia não pode ser negativo.")

        return dias_garantia

    @staticmethod
    def _validar_data_conclusao(data_conclusao_texto):
        # Data de conclusão é opcional (OS ainda em andamento)
        if not data_conclusao_texto:
            return None

        if not DataUtils.validar_data(data_conclusao_texto):
            raise ValueError("Data de conclusão inválida. Use o formato dd/mm/aaaa.")

        return DataUtils.string_para_data(data_conclusao_texto)

    # ------------------------------------------------------------------
    # Operações
    # ------------------------------------------------------------------

    def cadastrar(self, id_cliente, id_funcionario, id_equipamento, data_entrada_texto,
                  data_conclusao_texto, status, problema, diagnostico,
                  valor_total, forma_pagamento, dias_garantia):
        """
        Recebe dados "crus" vindos da tela (Tkinter), valida e converte,
        monta o objeto Ordem_servico e delega o salvamento ao DAO.
        """

        # --- Validações básicas ---
        if not problema or not problema.strip():
            raise ValueError("O campo 'problema' é obrigatório.")

        if not data_entrada or not str(data_entrada_texto).strip():
            raise ValueError("A data de entrada é obrigatória.")
        
        if not DataUtils.validar_data(data_entrada_texto):
            raise ValueError(
                f"Data de entrada inválida: {data_entrada_texto!r}. Use o formato dd/mm/aaaa."
            )

        data_conclusao = self._validar_data_conclusao(data_conclusao_texto)
        valor_total = self._validar_valor_total(valor_total)
        dias_garantia = self._validar_dias_garantia(dias_garantia)

        data_entrada = DataUtils.string_para_data(data_entrada_texto)

        # Conclusão não pode ser anterior à entrada
        if data_conclusao is not None and data_conclusao < data_entrada:
            raise ValueError("Data de conclusão não pode ser anterior à data de entrada.")

        # --- Busca as entidades relacionadas (garante que existem) ---
        cliente = self.cliente_dao.get_by_id(id_cliente)
        if cliente is None:
            raise ValueError(f"Cliente com id {id_cliente} não encontrado.")

        funcionario = self.funcionario_dao.get_by_id(id_funcionario)
        if funcionario is None:
            raise ValueError(f"Funcionário com id {id_funcionario} não encontrado.")

        equipamento = self.equipamento_dao.get_by_id(id_equipamento)
        if equipamento is None:
            raise ValueError(f"Equipamento com id {id_equipamento} não encontrado.")

        # --- Monta o objeto e delega ao DAO ---
        nova_ordem = Ordem_servico(
            id=None,
            data_entrada=data_entrada,
            data_conclusao=data_conclusao,
            status=status,
            problema=problema,
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
            raise ValueError(f"Ordem de serviço com id {id} não encontrada.")
        return ordem

    def atualizar(self, id, status, data_conclusao_texto, problema, diagnostico,
                  valor_total, forma_pagamento, dias_garantia):
        """
        Atualização parcial: busca a ordem existente, aplica os novos dados
        e salva. Mantém cliente/funcionario/equipamento e a data de entrada originais.
        """
        ordem = self.buscar_por_id(id)

        if not problema or not problema.strip():
            raise ValueError("O campo 'problema' é obrigatório.")

        data_conclusao = self._validar_data_conclusao(data_conclusao_texto)
        valor_total = self._validar_valor_total(valor_total)
        dias_garantia = self._validar_dias_garantia(dias_garantia)

        data_entrada = DataUtils.string_para_data(ordem.data_entrada)
        if data_conclusao is not None and data_entrada is not None and data_conclusao < data_entrada:
            raise ValueError("Data de conclusão não pode ser anterior à data de entrada.")

        ordem.atualizar_dados(
            nova_entrada=ordem.data_entrada,   # mantém a data original de entrada
            nova_conclusao=data_conclusao,
            novo_status=status,
            novo_problema=problema,
            novo_diagnostico=diagnostico,
            novo_valor=valor_total,
            novo_pagamento=forma_pagamento,
            nova_garantia=dias_garantia
        )

        return self.ordem_servico_dao.update(ordem)

    def excluir(self, id):
        # Garante que existe antes de tentar excluir (evita exclusão silenciosa de algo inexistente)
        self.buscar_por_id(id)
        self.ordem_servico_dao.delete(id)