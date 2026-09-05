from app.models.cliente import Cliente

class ClienteController:

    def __init__(self, cliente_dao):
        self.dao = cliente_dao

    def _validar_dados(self, nome, cpf, email):
        erros = []

        if not nome or not nome.strip():
            erros.append("O nome é obrigatório.")

            cpf_numeros = "".join(filter(str.isdigit, cpf or ""))
            if len(cpf_numeros) != 11:
                erros.append("CPF inválido. Deve conter 11 dígitos.")
                email_valido = self._validar_email(email)
                if not email_valido:
                    erros.append("O email é inválido.")
        return erros

    def _validar_email(self, email):
        if not email or not email.strip():
            return False
        if "@" not in email or "." not in email:
            return False
        return True

    def _cpf_ja_cadastrado(self, cpf):  

        cpf = (cpf or "").strip()
        for cliente in self.dao.get_all():
            if cliente.cpf == cpf:
                return cliente
        return None

    def cadastrar(self, nome, cpf, email):
        erros = self._validar_dados(nome, cpf, email)
        if erros:
            return False, "\n".join(erros)

        if self._cpf_ja_cadastrado(cpf):
            return False, "CPF já cadastrado."

        cliente = Cliente(None, nome.strip(), cpf.strip(), email.strip())

        try:
            cliente = self.dao.save(cliente)
            return True, cliente
        except Exception as erro:
            return False, f"Erro ao cadastrar cliente: {erro}"

    def atualizar(self, id, nome, cpf, email):
        cliente = self.dao.get_by_id(id)
        if cliente is None:
            return False, "Cliente não encontrado."

        erros = self._validar_dados(nome, cpf, email)
        if erros:
            return False, "\n".join(erros)

        cliente.nome = nome.strip()
        cliente.cpf = cpf.strip()
        cliente.email = email.strip()

        try:
            cliente = self.dao.update(cliente)
            return True, cliente
        except Exception as erro:
            return False, f"Erro ao atualizar cliente: {erro}" 

    def deletar(self, id):
        cliente = self.dao.get_by_id(id)
        if cliente is None:
            return False, "Cliente não encontrado."

        try:
            sucesso = self.dao.delete(id)
            if sucesso:
                return True, "Cliente deletado com sucesso."
            else:
                return False, "Falha ao deletar cliente."
        except Exception as erro:
            return False, f"Erro ao deletar cliente: {erro}"

    def buscar_por_id(self, id):
        cliente = self.dao.get_by_id(id)
        if cliente is None:
            return False, "Cliente não encontrado."
        return True, cliente

    def buscar_todos(self):
        try:
            clientes = self.dao.get_all()
            return True, clientes
        except Exception as erro:
            return False, f"Erro ao buscar clientes: {erro}"