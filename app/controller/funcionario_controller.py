from app.core.idioma import t
from app.models.funcionario import Funcionario


class FuncionarioController:

    def __init__(self, funcionario_dao):
        self.dao = funcionario_dao

    def _validar_dados(self, nome, cpf, cargo):
        erros = []

        if not nome or not nome.strip():
            erros.append(t("O nome é obrigatório."))

        cpf_numeros = "".join(filter(str.isdigit, cpf or ""))
        if len(cpf_numeros) != 11:
            erros.append(t("CPF inválido. Deve conter 11 dígitos."))

        if not cargo or not cargo.strip():
            erros.append(t("O cargo é obrigatório."))

        return erros

    def _cpf_ja_cadastrado(self, cpf):
        cpf = (cpf or "").strip()
        for funcionario in self.dao.get_all():
            if funcionario.cpf == cpf:
                return funcionario
        return None

    def cadastrar(self, nome, cpf, cargo):
        erros = self._validar_dados(nome, cpf, cargo)
        if erros:
            return False, "\n".join(erros)

        if self._cpf_ja_cadastrado(cpf):
            return False, t("CPF já cadastrado.")

        funcionario = Funcionario(None, nome.strip(), cpf.strip(), cargo.strip())

        try:
            funcionario = self.dao.save(funcionario)
            return True, funcionario
        except Exception as erro:
            return False, f"{t('Erro ao cadastrar funcionário:')} {erro}"

    def atualizar(self, id, nome, cpf, cargo):
        funcionario = self.dao.get_by_id(id)
        if funcionario is None:
            return False, t("Funcionário não encontrado.")

        erros = self._validar_dados(nome, cpf, cargo)
        if erros:
            return False, "\n".join(erros)

        existente = self._cpf_ja_cadastrado(cpf)
        if existente and existente.id != id:
            return False, t("CPF já cadastrado.")

        funcionario.atualizar_dados(nome.strip(), cpf.strip(), cargo.strip())

        try:
            sucesso = self.dao.update(funcionario)
            if sucesso:
                return True, t("Funcionário atualizado com sucesso.")
            return False, t("Não foi possível atualizar o funcionário.")
        except Exception as erro:
            return False, f"{t('Erro ao atualizar funcionário:')} {erro}"

    def excluir(self, id):
        funcionario = self.dao.get_by_id(id)
        if funcionario is None:
            return False, t("Funcionário não encontrado.")

        try:
            sucesso = self.dao.delete(id)
            if sucesso:
                return True, t("Funcionário excluído com sucesso.")
            return False, t("Não foi possível excluir o funcionário.")
        except Exception as erro:
            return False, f"{t('Erro ao excluir funcionário:')} {erro}"

    def buscar_por_id(self, id):
        funcionario = self.dao.get_by_id(id)
        if funcionario is None:
            return False, t("Funcionário não encontrado.")
        return True, funcionario

    def buscar_todos(self):
        try:
            return True, self.dao.get_all()
        except Exception as erro:
            return False, f"{t('Erro ao buscar funcionários:')} {erro}"