class Funcionarios:
    def __init__(self, id, nome, cpf, cargo):
        
        self._id = id
        self._nome = nome
        self._cpf = cpf
        self._cargo = cargo


    def atualizar_dados(self, novo_nome, novo_cpf, novo_cargo):
        self._nome = novo_nome
        self._cpf = novo_cpf
        self._cargo = novo_cargo

    @property
    def id(self):
        return self._id
    @id.setter
    def id (self, novo_id):
        self._id = novo_id

    @property
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, novo_nome):
        self._nome = novo_nome

    @property
    def cpf(Self):
        return Self._cpf
    @cpf.setter
    def cpf(Self, novo_cpf):
        Self._cpf = novo_cpf

    @property
    def cargo(self):
        return self._cargo
    @cargo.setter
    def cargo(self, novo_cargo):
        self._cargo = novo_cargo