from app.models.funcionario import Funcionario


class FuncionarioController:
    """
    Controller responsável por mediar a comunicação entre a View (Tkinter)
    e o Funcionario_DAO.

    Erros de validação ou de "não encontrado" são sinalizados levantando
    ValueError, não retornando tupla (sucesso, mensagem) — é assim que a
    Funcionario_View espera lidar com os erros, no bloco try/except ValueError.
    """

    def __init__(self, funcionario_dao):
        self.dao = funcionario_dao

    # ---------- Validações ----------

    def _validar_dados(self, nome, cpf, cargo):
        if not nome or not nome.strip():
            raise ValueError("O nome é obrigatório.")

        cpf_numeros = "".join(filter(str.isdigit, cpf or ""))
        if len(cpf_numeros) != 11:
            raise ValueError("CPF inválido. Deve conter 11 dígitos.")

        if not cargo or not cargo.strip():
            raise ValueError("O cargo é obrigatório.")

    def _cpf_ja_cadastrado(self, cpf):
        """Retorna o Funcionario com esse CPF, ou None (o DAO não tem busca por CPF)."""
        cpf = (cpf or "").strip()
        for funcionario in self.dao.get_all():
            if funcionario.cpf == cpf:
                return funcionario
        return None

    # ---------- Operações CRUD ----------

    def cadastrar(self, nome, cpf, cargo):
        """Valida e cadastra um novo funcionário. Levanta ValueError se algo for inválido."""
        self._validar_dados(nome, cpf, cargo)

        if self._cpf_ja_cadastrado(cpf):
            raise ValueError("Já existe um funcionário cadastrado com esse CPF.")

        funcionario = Funcionario(None, nome.strip(), cpf.strip(), cargo.strip())
        return self.dao.save(funcionario)

    def atualizar(self, id, nome, cpf, cargo):
        """Valida e atualiza um funcionário existente. Levanta ValueError se algo for inválido."""
        funcionario = self.buscar_por_id(id)  # já levanta ValueError se não existir

        self._validar_dados(nome, cpf, cargo)

        existente = self._cpf_ja_cadastrado(cpf)
        if existente and existente.id != id:
            raise ValueError("Já existe outro funcionário cadastrado com esse CPF.")

        funcionario.atualizar_dados(nome.strip(), cpf.strip(), cargo.strip())
        return self.dao.update(funcionario)

    def excluir(self, id):
        """Exclui um funcionário pelo ID. Levanta ValueError se não existir."""
        self.buscar_por_id(id)  # garante que existe antes de excluir
        self.dao.delete(id)

    def buscar_por_id(self, id):
        """Busca um funcionário pelo ID. Levanta ValueError se não encontrar."""
        funcionario = self.dao.get_by_id(id)
        if funcionario is None:
            raise ValueError(f"Funcionário com id {id} não encontrado.")
        return funcionario

    def listar_todas(self):
        return self.dao.get_all()