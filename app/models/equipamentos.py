from app.models.clientes import Cliente

class Equipamento:
    def __init__(self, tipo, marca, modelo, numero_serie, id_cliente=Cliente):
        self._id = id
        self._tipo = tipo 
        self._marca = marca
        self._modelo = modelo
        self._numero_serie = numero_serie
        self._id_cliente = id_cliente

    def atualizar_dados(self, novo_tipo, nova_marca, novo_modelo, novo_numero_serie):
        self._tipo = novo_tipo
        self._marca = nova_marca
        self._modelo = novo_modelo
        self._numero_serie = novo_numero_serie

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, novo_id):
        self._id = novo_id
    
    @property
    def tipo(self):
        return self._tipo
    @tipo.setter
    def tipo(self, novo_tipo):
        self._tipo = novo_tipo

    @property
    def marca(self):
        return self._marca 
    @marca.setter
    def marca(self, nova_marca):
        self._marca = nova_marca

    @property
    def modelo(self):
        return self._modelo
    @modelo.setter
    def modelo(self, novo_modelo):
        self._modelo = novo_modelo

    @property
    def numero_serie(self):
        return self._numero_serie
    @numero_serie.setter
    def numero_serie(self, novo_numero):
        self._numero_serie = novo_numero


    @property
    def id_cliente(self):
        return self._id_cliente
    @id_cliente.setter
    def id_cliente(self, novo_id_cliente):
        self._id_cliente = novo_id_cliente    