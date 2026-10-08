# TRADUÇÃO PT/EN: toda mensagem devolvida à tela passa por t(); mensagens com erro usam f"{t('Erro ...:')} {erro}".
# Troquei os textos entre parênteses (sem t()) por t(...) e traduzi o "Erro ao buscar peças"; a lógica não mudou.
from app.models.pecas import Peca
from app.core.idioma import t


class PecaController:

    def __init__(self, peca_dao):
        self.dao = peca_dao

    def _validar_dados(self, nome, codigo, quantidade_estoque, preco_venda):
        erros = []

        if not nome or not nome.strip():
            erros.append(("O nome da peça é obrigatório."))

        if not codigo or not codigo.strip():
            erros.append(("O código da peça é obrigatório."))

        try:
            if int(quantidade_estoque) < 0:
                erros.append(("A quantidade em estoque não pode ser negativa."))
        except (TypeError, ValueError):
            erros.append(("Quantidade em estoque inválida. Informe um número inteiro."))

        try:
            if float(preco_venda) < 0:
                erros.append(("O preço de venda não pode ser negativo."))
        except (TypeError, ValueError):
            erros.append(("Preço de venda inválido. Informe um valor numérico."))

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
            return False, ("Já existe uma peça cadastrada com esse código.")

        peca = Peca(None, nome.strip(), codigo.strip(), int(quantidade_estoque), float(preco_venda))

        try:
            peca = self.dao.save(peca)
            return True, peca
        except Exception as erro:
            return False, f"{('Erro ao cadastrar peça:')} {erro}"

    def atualizar(self, id, nome, codigo, quantidade_estoque, preco_venda):
        peca = self.dao.get_by_id(id)
        if peca is None:
            return False, ("Peça não encontrada.")

        erros = self._validar_dados(nome, codigo, quantidade_estoque, preco_venda)
        if erros:
            return False, "\n".join(erros)

        existente = self._codigo_ja_cadastrado(codigo)
        if existente and existente.id != id:
            return False, ("Já existe outra peça cadastrada com esse código.")

        peca.atualizar_dados(nome.strip(), codigo.strip(), int(quantidade_estoque), float(preco_venda))

        try:
            sucesso = self.dao.update(peca)
            if sucesso:
                return True, ("Peça atualizada com sucesso.")
            return False, ("Não foi possível atualizar a peça.")
        except Exception as erro:
            return False, f"{('Erro ao atualizar peça:')} {erro}"

    def excluir(self, id):
        if self.dao.get_by_id(id) is None:
            return False, ("Peça não encontrada.")

        try:
            sucesso = self.dao.delete(id)
            if sucesso:
                return True, ("Peça excluída com sucesso.")
            return False, ("Não foi possível excluir a peça.")
        except Exception as erro:
            return False, f"{('Erro ao excluir peça:')} {erro}"

    def buscar_por_id(self, id):
        return self.dao.get_by_id(id)

    def buscar_todos(self):
        try:
            return True, self.dao.get_all()
        except Exception as erro:
            return False, f"{t('Erro ao buscar peças:')} {erro}"

    # dar_baixa_estoque foi removido: o estoque agora é ajustado dentro da
    # transação de OrdemServicoPecaDAO.substituir_pecas_da_ordem_servico
    # (ler, calcular e gravar aqui dava erro quando dois acessos ocorriam juntos).