from app.models.servico import Servico
from app.core.idioma import t


class ServicoController:

    def __init__(self, servico_dao):
        self.dao = servico_dao

    def _validar_dados(self, nome, descricao, valor_padrao):
        erros = []

        if not nome or not nome.strip():
            erros.append (t("O nome do serviço é obrigatório."))

        if not descricao or not descricao.strip():
            erros.append (t("A descrição é obrigatória."))

        try:
            if float(valor_padrao) < 0:
                erros.append(t("O valor padrão não pode ser negativo."))
        except (TypeError, ValueError):
            erros.append(t("Valor padrão inválido. Informe um valor numérico."))

        return erros

    def cadastrar(self, nome, descricao, valor_padrao):
        erros = self._validar_dados(nome, descricao, valor_padrao)
        if erros:
            return False, "\n".join(erros)

        servico = Servico(None, nome.strip(), descricao.strip(), float(valor_padrao))

        try:
            servico = self.dao.save(servico)
            return True, servico
        except Exception as erro:
            return False, f"(t(Erro ao cadastrar serviço: {erro}))"

    def atualizar(self, id, nome, descricao, valor_padrao):
        servico = self.dao.get_by_id(id)
        if servico is None:
            return False, (t("Serviço não encontrado."))

        erros = self._validar_dados(nome, descricao, valor_padrao)
        if erros:
            return False, "\n".join(erros)

        servico.atualizar_dados(nome.strip(), descricao.strip(), float(valor_padrao))

        try:
            sucesso = self.dao.update(servico)
            if sucesso:
                return True, (t("Serviço atualizado com sucesso."))
            return False, (t("Não foi possível atualizar o serviço."))
        except Exception as erro:
            return False, f"(t(Erro ao atualizar serviço: {erro}))"

    def excluir(self, id):
        if self.dao.get_by_id(id) is None:
            return False, "(t(Serviço não encontrado.))"

        try:
            sucesso = self.dao.delete(id)
            if sucesso:
                return True, "Serviço excluído com sucesso."
            return False, "Não foi possível excluir o serviço."
        except Exception as erro:
            return False, f"Erro ao excluir serviço: {erro}"

    def buscar_por_id(self, id):
        return self.dao.get_by_id(id)

    def buscar_todos(self):
        try:
            return True, self.dao.get_all()
        except Exception as erro:
            return False, f"Erro ao buscar serviços: {erro}"