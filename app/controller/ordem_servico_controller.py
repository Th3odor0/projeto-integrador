from app.dao.ordem_servico_dao import Ordem_servico_DAO
from app.models.ordens_servico import Ordem_servico
from app.core.dataUltils import DataUtils


class Ordem_servico_Controller:
    def __init__(self, ordem_servico_dao, cliente_dao, funcionario_dao, equipamento_dao):
        self.ordem_servico_dao = ordem_servico_dao
        self.cliente_dao = cliente_dao
        self.funcionario_dao = funcionario_dao
        self.equipamento_dao = equipamento_dao

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

        if not DataUtils.validar_data(data_entrada_texto):
            raise ValueError("Data de entrada inválida. Use o formato dd/mm/aaaa.")

        # Data de conclusão pode ser opcional (OS ainda em andamento)
        if data_conclusao_texto and not DataUtils.validar_data(data_conclusao_texto):
            raise ValueError("Data de conclusão inválida. Use o formato dd/mm/aaaa.")

        try:
            valor_total = float(valor_total)
        except (TypeError, ValueError):
            raise ValueError("Valor total precisa ser um número.")

        if valor_total < 0:
            raise ValueError("Valor total não pode ser negativo.")

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

        # --- Converte datas de texto para date ---
        data_entrada = DataUtils.string_para_data(data_entrada_texto)
        data_conclusao = DataUtils.string_para_data(data_conclusao_texto)

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
        e salva. Mantém cliente/funcionario/equipamento originais.
        """
        ordem = self.buscar_por_id(id)

        if data_conclusao_texto and not DataUtils.validar_data(data_conclusao_texto):
            raise ValueError("Data de conclusão inválida. Use o formato dd/mm/aaaa.")

        try:
            valor_total = float(valor_total)
        except (TypeError, ValueError):
            raise ValueError("Valor total precisa ser um número.")

        data_conclusao = DataUtils.string_para_data(data_conclusao_texto)

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

        