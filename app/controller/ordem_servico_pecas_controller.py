from app.core.idioma import t


class Ordem_Servico_Peca_Controller:
    """
    Controller para vincular peças usadas a uma Ordem de Serviço.

    Segue o padrão "substituir tudo" do Ordem_Servico_Peca_DAO: a View monta a
    lista completa de peças (com quantidade e valor unitário) da OS e manda
    de uma vez via salvar_pecas_da_ordem — o DAO apaga os vínculos antigos e
    reinsere os novos.

    Todo método público retorna (sucesso: bool, resultado), igual o padrão
    já usado no ClienteController/PecaController.
    """

    def __init__(self, ordem_servico_peca_dao, peca_dao, ordem_servico_dao):
        self.dao = ordem_servico_peca_dao
        self.peca_dao = peca_dao
        self.ordem_servico_dao = ordem_servico_dao

    def listar_pecas_da_ordem(self, ordem_servico_id):
        """
        Retorna (sucesso, lista_de_pecas_ou_mensagem). Cada Peca da lista vem
        com os atributos extras .quantidade_os e .valor_unitario_os, setados
        pelo DAO a partir do JOIN com ordem_servico_pecas.
        """
        ordem_servico = self.ordem_servico_dao.get_by_id(ordem_servico_id)
        if ordem_servico is None:
            return False, t("Ordem de serviço com id {id} não encontrada.", id=ordem_servico_id)

        try:
            pecas = self.dao.get_pecas_por_ordem_servico(ordem_servico)
            return True, pecas
        except Exception as erro:
            return False, f"{t('Erro ao buscar peças da ordem:')} {erro}"

    def salvar_pecas_da_ordem(self, ordem_servico_id, itens):
        """
        Substitui todas as peças vinculadas à ordem de serviço pelas informadas em 'itens'.

        'itens' é uma lista de dicionários no formato:
            {"peca_id": int, "quantidade": int_ou_str, "valor_unitario": float_ou_str}

        Valida cada item (peça existe, quantidade > 0, estoque suficiente,
        valor não negativo) ANTES de persistir qualquer coisa — se um item
        for inválido, nada é salvo (a lista antiga da OS fica intacta).
        """
        ordem_servico = self.ordem_servico_dao.get_by_id(ordem_servico_id)
        if ordem_servico is None:
            return False, t("Ordem de serviço com id {id} não encontrada.", id=ordem_servico_id)

        pecas_preparadas = []
        for item in itens:
            peca_id = item.get("peca_id")
            quantidade = item.get("quantidade")
            valor_unitario = item.get("valor_unitario")

            peca = self.peca_dao.get_by_id(peca_id)
            if peca is None:
                return False, t("Peça com id {id} não encontrada.", id=peca_id)

            try:
                quantidade = int(quantidade)
            except (TypeError, ValueError):
                return False, t("Quantidade inválida para a peça '{nome}'.", nome=peca.nome)

            if quantidade <= 0:
                return False, t("A quantidade da peça '{nome}' deve ser maior que zero.", nome=peca.nome)

            if quantidade > peca.quantidade_estoque:
                return False, t(
                    "Estoque insuficiente para a peça '{nome}' (disponível: {disponivel}).",
                    nome=peca.nome, disponivel=peca.quantidade_estoque,
                )

            try:
                valor_unitario = float(valor_unitario)
            except (TypeError, ValueError):
                return False, t("Valor unitário inválido para a peça '{nome}'.", nome=peca.nome)

            if valor_unitario < 0:
                return False, t("O valor unitário da peça '{nome}' não pode ser negativo.", nome=peca.nome)

            peca.quantidade_os = quantidade
            peca.valor_unitario_os = valor_unitario
            pecas_preparadas.append(peca)

        try:
            self.dao.substituir_pecas_da_ordem_servico(ordem_servico, pecas_preparadas)
            return True, t("Peças da ordem de serviço atualizadas com sucesso.")
        except Exception as erro:
            return False, f"{t('Erro ao salvar peças da ordem:')} {erro}"

    def calcular_total_pecas(self, ordem_servico_id):
        """
        Retorna (sucesso, valor_total_ou_mensagem): soma de quantidade x valor_unitario_os
        de todas as peças da OS. Útil pra mostrar um subtotal na tela. Remova se não precisar.
        """
        sucesso, resultado = self.listar_pecas_da_ordem(ordem_servico_id)
        if not sucesso:
            return False, resultado

        total = sum(peca.quantidade_os * peca.valor_unitario_os for peca in resultado)
        return True, total