from abc import ABC, abstractmethod


class DAO(ABC):

    def __init__(self, database):
        self._database = database

    def conectar(self):
        conexao = self._database.conectar()
        cursor = conexao.cursor()
        return conexao, cursor

    def desconectar(self, cursor, conexao):
        self._database.desconectar(cursor, conexao)

    @staticmethod
    def _violacao_fk(erro):
        """
        True se o erro é o 1451 do MySQL ("Cannot delete or update a parent
        row"): tentativa de excluir algo que ainda é referenciado por outra
        tabela (as FKs com ON DELETE RESTRICT / sem ação do schema).
        Funciona com mysql-connector (erro.errno) e com pymysql (erro.args[0]).
        """
        codigo = getattr(erro, "errno", None)
        if codigo is None and getattr(erro, "args", None):
            codigo = erro.args[0]
        return codigo == 1451

    @abstractmethod
    def save(self, objeto):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def update(self, objeto):
        pass

    @abstractmethod
    def delete(self, id):
        pass