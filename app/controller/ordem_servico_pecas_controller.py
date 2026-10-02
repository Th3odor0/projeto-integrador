


class Ordem_Servico_Peca_Controller:

    def __init__(self, ordem_servico_peca_dao, peca_dao, ordem_servico_dao):
        self.dao = ordem_servico_peca_dao
        self.peca_dao = peca_dao
        self.ordem_servico_dao = ordem_servico_dao

    def listar_pecas_da_ordem(self, ordem_servico_id):
        ordem_servico = self.ordem_servico_dao.get_by_id(ordem_servico_id)
        if ordem_servico is None:
            return False("Ordem de serviço com id {id} não encontrada.", id=ordem_servico_id)

        try:
            pecas = self.dao.get_pecas_por_ordem_servico(ordem_servico)
            return True, pecas
        except Exception as erro:
            return False, f"{('Erro ao buscar peças da ordem:')} {erro}"

    def salvar_pecas_da_ordem(self, ordem_servico_id, itens):
        ordem_servico = self.ordem_servico_dao.get_by_id(ordem_servico_id)
        if ordem_servico is None:
            return False, f"Ordem de serviço com id {ordem_servico_id} não encontrada."

        # O que a ordem já tem reservado: essas unidades já saíram do estoque,
        # então contam como disponíveis para ESTA ordem ao salvar de novo.
        try:
            ja_reservado = {
                p.id: p.quantidade_os
                for p in self.dao.get_pecas_por_ordem_servico(ordem_servico)
            }
        except Exception as erro:
            return False, f"Erro ao buscar peças da ordem: {erro}"

        pecas_preparadas = []
        vistos = set()
        for item in itens:
            peca_id = item.get("peca_id")
            quantidade = item.get("quantidade")
            valor_unitario = item.get("valor_unitario")

            if peca_id in vistos:
                return False, "A mesma peça aparece mais de uma vez na lista."
            vistos.add(peca_id)

            peca = self.peca_dao.get_by_id(peca_id)
            if peca is None:
                return False("Peça com id {id} não encontrada.", id=peca_id)

            try:
                quantidade = int(quantidade)
            except (TypeError, ValueError):
                return False("Quantidade inválida para a peça '{nome}'.", nome=peca.nome)

            if quantidade <= 0:
                return False("A quantidade da peça '{nome}' deve ser maior que zero.", nome=peca.nome)

            disponivel = peca.quantidade_estoque + ja_reservado.get(peca_id, 0)
            if quantidade > disponivel:
                return False, (
                    f"Estoque insuficiente para a peça '{peca.nome}' "
                    f"(disponível: {disponivel})."
                )

            try:
                valor_unitario = float(valor_unitario)
            except (TypeError, ValueError):
                return False("Valor unitário inválido para a peça '{nome}'.", nome=peca.nome)

            if valor_unitario < 0:
                return False("O valor unitário da peça '{nome}' não pode ser negativo.", nome=peca.nome)

            peca.quantidade_os = quantidade
            peca.valor_unitario_os = valor_unitario
            pecas_preparadas.append(peca)

        try:
            # o DAO confere o estoque de novo, dentro da transação (vale o dele)
            self.dao.substituir_pecas_da_ordem_servico(ordem_servico, pecas_preparadas)
            return True, ("Peças da ordem de serviço atualizadas com sucesso.")
        except Exception as erro:
            return False, f"{('Erro ao salvar peças da ordem:')} {erro}"

    def calcular_total_pecas(self, ordem_servico_id):
        sucesso, resultado = self.listar_pecas_da_ordem(ordem_servico_id)
        if not sucesso:
            return False, resultado

        total = sum(peca.quantidade_os * peca.valor_unitario_os for peca in resultado)
        return True, total