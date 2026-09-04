class Cliente:
    def __init__(self, id, nome, cpf, telefone, email):
        self._id = id
        self._nome = nome
        self._cpf = cpf
        self._telefone = telefone
        self._email = email

    def atualizar_dados(self, novo_nome, novo_cpf, novo_telefone, novo_email):
        self._nome = novo_nome
        self._cpf = novo_cpf
        self._telefone = novo_telefone
        self._email = novo_email

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, novo_id):
        self._id = novo_id

    @property
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, novo_nome):
        self._nome = novo_nome

    @property
    def cpf(self):
        return self._cpf
    @cpf.setter
    def cpf(self, novo_cpf):
        self._cpf = novo_cpf

    @property
    def telefone(self):
        return self._telefone
    @telefone.setter
    def telefone(self, novo_telefone):
        self._telefone = novo_telefone

    @property
    def email(self):
        return self._email
    @telefone.setter
    def email(self, novo_telefone):
        self._email = novo_telefone

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, novo_email):
        self._email = novo_email
        
    