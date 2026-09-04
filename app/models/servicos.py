class Servicos:
    def __init__(self,  id, nome, descricao, valor_padrao):
        self._id = id
        self._nome = nome 
        self._descricao = descricao
        self._valor_padrao = valor_padrao

    def atualiazar_dados(self, novo_nome, nova_descricao, novo_valor):
        self._nome = novo_nome
        self._descricao = nova_descricao
        self._valor_padrao = novo_valor

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
    def descricao(self):
        return self._descricao
    @descricao.setter
    def descricao(self, nova_descricao):
        self._descricao = nova_descricao

    @property
    def valor_padrao(self):
        return self._valor_padrao
    @valor_padrao.setter
    def valor_padrao(self, novo_valor):
        self._valor_padrao = novo_valor

