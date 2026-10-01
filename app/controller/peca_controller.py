from app.models.pecas import Peca
from app.core import t

class PecaController:

    def __init__(self, peca_dao):
        self.dao = peca_dao

    def _validar_dados(self, nome, codigo, quantidade_estoque, preco_venda):
        erros = []

        if not nome or not nome.strip():
            erros.append(t("O nome da peça é obrigatório."))

        if not codigo or not codigo.strip():
            erros.append(t("O código da peça é obrigatório."))

        try:
            if int(quantidade_estoque) < 0:
                erros.append(t("A quantidade em estoque não pode ser negativa."))
        except (TypeError, ValueError):
            erros.append(t("Quantidade em estoque inválida. Informe um número inteiro."))

        try:
            if float(preco_venda) < 0:
                erros.append(t("O preço de venda não pode ser negativo."))
        except (TypeError, ValueError):
            erros.append(t("Preço de venda inválido. Informe um valor numérico."))

        return erros

    def _codigo_ja_cadastrado(self, codigo):
        codigo = (codigo or "").strip()
        for peca in self.dao.get_all():
            if peca.codigo == codigo:
                return peca
        return None

    def cadastrar(self, nome, codigo, quantidade_estoque, preco_venda):
        erros = self._validar_dados(nome, codigo, quantidade_estoque, preco_venda)
        if erros:
            return False, "\n".join(erros)

        if self._codigo_ja_cadastrado(codigo):
            return False, t("Já existe uma peça cadastrada com esse código.")

        peca = Peca(None, nome.strip(), codigo.strip(), int(quantidade_estoque), float(preco_venda))

        try:
            peca = self.dao.save(peca)
            return True, peca
        except Exception as erro:
            return False, f"{t('Erro ao cadastrar peça:')} {erro}"

    def atualizar(self, id, nome, codigo, quantidade_estoque, preco_venda):
        peca = self.dao.get_by_id(id)
        if peca is None:
            return False, t("Peça não encontrada.")

        erros = self._validar_dados(nome, codigo, quantidade_estoque, preco_venda)
        if erros:
            return False, "\n".join(erros)

        existente = self._codigo_ja_cadastrado(codigo)
        if existente and existente.id != id:
            return False, t("Já existe outra peça cadastrada com esse código.")

        peca.atualizar_dados(nome.strip(), codigo.strip(), int(quantidade_estoque), float(preco_venda))

        try:
            sucesso = self.dao.update(peca)
            if sucesso:
                return True, t("Peça atualizada com sucesso.")
            return False, t("Não foi possível atualizar a peça.")
        except Exception as erro:
            return False, f"{t('Erro ao atualizar peça:')} {erro}"

    def excluir(self, id):
        if self.dao.get_by_id(id) is None:
            return False, t("Peça não encontrada.")

        try:
            sucesso = self.dao.delete(id)
            if sucesso:
                return True, t("Peça excluída com sucesso.")
            return False, t("Não foi possível excluir a peça.")
        except Exception as erro:
            return False, f"{t('Erro ao excluir peça:')} {erro}"

    def buscar_por_id(self, id):
        return self.dao.get_by_id(id)

    def buscar_todos(self):
        try:
            return True, self.dao.get_all()
        except Exception as erro:
            return False, f"Erro ao buscar peças: {erro}"

    # dar_baixa_estoque foi removido: o estoque agora é ajustado dentro da
    # transação de OrdemServicoPecaDAO.substituir_pecas_da_ordem_servico
    # (ler, calcular e gravar aqui dava erro quando dois acessos ocorriam juntos).