# Ajuste os imports abaixo conforme o caminho real dos seus arquivos no projeto
from app.models.pecas import Peca


class PecaController:


    def __init__(self, peca_dao):
        self.dao = peca_dao

 

    def _validar_dados(self, nome, codigo, quantidade_estoque, preco_venda):
        erros = []

        if not nome or not nome.strip():
            erros.append("O nome da peça é obrigatório.")

        if not codigo or not codigo.strip():
            erros.append("O código da peça é obrigatório.")

        try:
            if int(quantidade_estoque) < 0:
                erros.append("A quantidade em estoque não pode ser negativa.")
        except (TypeError, ValueError):
            erros.append("Quantidade em estoque inválida. Informe um número inteiro.")

        try:
            if float(preco_venda) < 0:
                erros.append("O preço de venda não pode ser negativo.")
        except (TypeError, ValueError):
            erros.append("Preço de venda inválido. Informe um valor numérico.")

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
            return False, "Já existe uma peça cadastrada com esse código."

        peca = Peca(None, nome.strip(), codigo.strip(), int(quantidade_estoque), float(preco_venda))

        try:
            peca = self.dao.save(peca)
            return True, peca
        except Exception as erro:
            return False, f"Erro ao cadastrar peça: {erro}"

    def atualizar(self, id, nome, codigo, quantidade_estoque, preco_venda):
       
        peca = self.dao.get_by_id(id)
        if peca is None:
            return False, "Peça não encontrada."

        erros = self._validar_dados(nome, codigo, quantidade_estoque, preco_venda)
        if erros:
            return False, "\n".join(erros)

        existente = self._codigo_ja_cadastrado(codigo)
        if existente and existente.id != id:
            return False, "Já existe outra peça cadastrada com esse código."

        peca.atualizar_dados(nome.strip(), codigo.strip(), int(quantidade_estoque), float(preco_venda))

        try:
            sucesso = self.dao.update(peca)
            if sucesso:
                return True, "Peça atualizada com sucesso."
            return False, "Não foi possível atualizar a peça."
        except Exception as erro:
            return False, f"Erro ao atualizar peça: {erro}"

    def excluir(self, id):
        """Exclui uma peça pelo ID."""
        if self.dao.get_by_id(id) is None:
            return False, "Peça não encontrada."

        try:
            sucesso = self.dao.delete(id)
            if sucesso:
                return True, "Peça excluída com sucesso."
            return False, "Não foi possível excluir a peça."
        except Exception as erro:
            return False, f"Erro ao excluir peça: {erro}"

    def buscar_por_id(self, id):
        return self.dao.get_by_id(id)

    def listar_todos(self):
        return self.dao.get_all()

    # ---------- Regra de negócio adicional (opcional) ----------

    def dar_baixa_estoque(self, id, quantidade_utilizada):
        """
        Reduz a quantidade em estoque de uma peça, útil quando ela é usada
        numa ordem de serviço (tabela ordem_servico_pecas). Remova se não precisar.
        """
        peca = self.dao.get_by_id(id)
        if peca is None:
            return False, "Peça não encontrada."

        try:
            quantidade_utilizada = int(quantidade_utilizada)
        except (TypeError, ValueError):
            return False, "Quantidade inválida."

        if quantidade_utilizada <= 0:
            return False, "A quantidade utilizada deve ser maior que zero."

        if quantidade_utilizada > peca.quantidade_estoque:
            return False, "Estoque insuficiente para essa quantidade."

        nova_quantidade = peca.quantidade_estoque - quantidade_utilizada
        peca.atualizar_dados(peca.nome, peca.codigo, nova_quantidade, peca.preco_venda)

        try:
            self.dao.update(peca)
            return True, f"Baixa de estoque realizada. Restam {nova_quantidade} unidades."
        except Exception as erro:
            return False, f"Erro ao atualizar estoque: {erro}"