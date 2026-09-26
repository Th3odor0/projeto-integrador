from app.dao.dao import DAO
from app.models.ordem_servico_servico import Ordem_servico_servico


class Ordem_servico_Servico_Dao(DAO):
    def __init__(self, database):
        super().__init__(database)

    def _montar_objeto(self, resultado):
        return Ordem_servico_servico(
            id=resultado[0],
            id_ordem_servico=resultado[1],
            id_servico=resultado[2],
            valor_cobrado=float(resultado[3]),
        )

    def _buscar(self, where_sql="", parametros=()):
        conexao, cursor = self.conectar()
        try:
            sql = f"""
                SELECT id, ordem_servico_id, servico_id, valor_cobrado
                FROM ordem_servico_servicos
                {where_sql}
            """
            cursor.execute(sql, parametros)
            return [self._montar_objeto(r) for r in cursor.fetchall()]
        finally:
            self.desconectar(cursor, conexao)

    @staticmethod
    def _valores(item):
        return item.id_ordem_servico, item.id_servico, item.valor_cobrado

    def get_all(self):
        return self._buscar()

    def get_by_id(self, id):
        resultados = self._buscar("WHERE id = %s", (id,))
        return resultados[0] if resultados else None

    def get_by_ordem_servico(self, ordem_servico_id):
        return self._buscar("WHERE ordem_servico_id = %s", (ordem_servico_id,))

    def save(self, item):
        conexao, cursor = self.conectar()
        try:
            sql = """
                INSERT INTO ordem_servico_servicos
                (ordem_servico_id, servico_id, valor_cobrado)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, self._valores(item))
            conexao.commit()
            item.id = cursor.lastrowid
            return item
        except Exception:
            conexao.rollback()
            raise
        finally:
            self.desconectar(cursor, conexao)

    def update(self, item):
        conexao, cursor = self.conectar()
        try:
            sql = """
                UPDATE ordem_servico_servicos
                SET ordem_servico_id = %s, servico_id = %s, valor_cobrado = %s
                WHERE id = %s
            """
            cursor.execute(sql, self._valores(item) + (item.id,))
            conexao.commit()
            return item
        except Exception:
            conexao.rollback()
            raise
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        conexao, cursor = self.conectar()
        try:
            cursor.execute("DELETE FROM ordem_servico_servicos WHERE id = %s", (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception:
            conexao.rollback()
            raise
        finally:
            self.desconectar(cursor, conexao)