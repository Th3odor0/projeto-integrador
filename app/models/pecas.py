class Pecas:
    def __init__(self, id, nome, codigo, quantidade_estoque, preco_venda):
        self._id = id
        self._nome = nome
        self._codigo = codigo
        self._quantidade_estoque = quantidade_estoque
        self._preco_venda = preco_venda

    def atualizar_dados(self, novo_nome, novo_codigo, nova_quantidade, novo_preço_venda):
        self._nome = novo_nome 
        self._codigo = novo_codigo 
        self._quantidade_estoque = nova_quantidade
        self._preco_venda = novo_preço_venda

    @property
    def id(Self):
        return Self._id
    @id.setter 
    def id(self, novo_id):
        self._id = novo_id

    @property 
    def nome(Self):
        return Self._nome
    @nome.setter
    def nome(self, novo_nome):
        self._nome = novo_nome

    @property
    def codigo(self):
        return self._codigo
    @codigo.setter
    def codigo(self, novo_codigo):
        self._codigo = novo_codigo

    @property
    def quantidade_estoque(self):
        return self.quantidade_estoque
    @quantidade_estoque.setter
    def quantidade_estoque(self, nova_quantidade):
        self._quantidade_estoque = nova_quantidade


    @property
    def preco_venda(Self):
        return Self._preco_venda
    @preco_venda.setter
    def preco_venda(self, novo_preco):
        self._preco_venda = novo_preco