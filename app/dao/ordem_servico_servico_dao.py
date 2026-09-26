from app.dao.dao import DAO
from app.models.ordem_servico_servico import Ordem_servico_servico


class Ordem_servico_Servico_Dao(DAO):
    """
    DAO para a tabela de junção entre Ordem de Serviço e Serviço.

    Tabela: ordem_servico_servicos (plural), colunas ordem_servico_id e
    servico_id. Os atributos do model Python continuam se chamando
    id_servico/id_ordem_servico; só o SQL usa os nomes de coluna reais.
    """

    def __init__(self, database):
        super().__init__(database)

    def get_all(self):
        conexao, cursor = self.conectar()
        try:
            sql = """
                SELECT id, valor_cobrado, servico_id, ordem_servico_id
                FROM ordem_servico_servicos
            """
            cursor.execute(sql)
            linhas = cursor.fetchall()
            return [self._montar_objeto(linha) for linha in linhas]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_ordem_servico(self, ordem_servico_id):
        conexao, cursor = self.conectar()
        try:
            sql = """
                SELECT id, valor_cobrado, servico_id, ordem_servico_id
                FROM ordem_servico_servicos
                WHERE ordem_servico_id = %s
            """
            cursor.execute(sql, (ordem_servico_id,))
            linhas = cursor.fetchall()
            return [self._montar_objeto(linha) for linha in linhas]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        conexao, cursor = self.conectar()
        try:
            sql = """
                SELECT id, valor_cobrado, servico_id, ordem_servico_id
                FROM ordem_servico_servicos
                WHERE id = %s
            """
            cursor.execute(sql, (id,))
            linha = cursor.fetchone()
            return self._montar_objeto(linha) if linha else None
        finally:
            self.desconectar(cursor, conexao)

    def save(self, item):
        conexao, cursor = self.conectar()
        try:
            sql = """
                INSERT INTO ordem_servico_servicos
                (valor_cobrado, servico_id, ordem_servico_id)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (item.valor_cobrado, item.id_servico, item.id_ordem_servico))
            conexao.commit()
            novo_id = cursor.lastrowid
            return Ordem_servico_servico(
                novo_id, item.valor_cobrado, item.id_servico, item.id_ordem_servico
            )
        except Exception:
            conexao.rollback()
            raise
        finally:
            self.desconectar(cursor, conexao)

    def update(self, item):
        conexao, cursor = self.conectar()
        try:
            sql = "UPDATE ordem_servico_servicos SET valor_cobrado = %s WHERE id = %s"
            cursor.execute(sql, (item.valor_cobrado, item.id))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception:
            conexao.rollback()
            raise
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        conexao, cursor = self.conectar()
        try:
            sql = "DELETE FROM ordem_servico_servicos WHERE id = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception:
            conexao.rollback()
            raise
        finally:
            self.desconectar(cursor, conexao)

    @staticmethod
    def _montar_objeto(linha):
        id_, valor_cobrado, servico_id, ordem_servico_id = linha
        return Ordem_servico_servico(id_, float(valor_cobrado), servico_id, ordem_servico_id)