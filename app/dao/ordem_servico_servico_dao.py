from app.dao.dao import DAO
from app.models.ordem_servico_servico import Ordem_servico_servico

class Ordem_servico_Servico_Dao(DAO):
    def __init__(self, database, servico_dao=None):
        super().__init__(database)
        self.servico_dao = servico_dao

    def save(self, item):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    INSERT INTO ordem_servico_servicos
                    (
                        ordem_servico_id,
                        servico_id,
                        valor_cobrado
                    )
                    VALUES
                    (
                        %s, %s, %s
                    )
                  """
            cursor.execute(
                sql,
                (
                    item.ordem_servico.id if hasattr(item.ordem_servico, 'id') else item.ordem_servico_id,
                    item.servico.id if hasattr(item.servico, 'id') else item.servico_id,
                    item.valor_cobrado
                )
            )

            conexao.commit()
            item.id = cursor.lastrowid
            return item

        except Exception:
            conexao.rollback()
            raise

        finally:
            self.desconectar(cursor, conexao)

    def get_all(self):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT
                        id,
                        ordem_servico_id,
                        servico_id,
                        valor_cobrado
                    FROM
                        ordem_servico_servicos
                  """
            cursor.execute(sql)
            resultados = cursor.fetchall()

            itens = []
            for resultado in resultados:
                servico = self.servico_dao.get_by_id(resultado[2]) if self.servico_dao else resultado[2]
                item = Ordem_servico_servico(
                    id=resultado[0],
                    ordem_servico_id=resultado[1],
                    servico=servico,
                    valor_cobrado=float(resultado[3])
                )
                itens.append(item)

            return itens

        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT
                        id,
                        ordem_servico_id,
                        servico_id,
                        valor_cobrado
                    FROM
                        ordem_servico_servicos
                    WHERE
                        id = %s
                  """
            cursor.execute(sql, (id,))
            resultado = cursor.fetchone()

            if resultado:
                servico = self.servico_dao.get_by_id(resultado[2]) if self.servico_dao else resultado[2]
                return Ordem_servico_servico(
                    id=resultado[0],
                    ordem_servico_id=resultado[1],
                    servico=servico,
                    valor_cobrado=float(resultado[3])
                )

            return None

        finally:
            self.desconectar(cursor, conexao)

    def get_by_ordem_servico(self, ordem_servico_id):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT
                        id,
                        ordem_servico_id,
                        servico_id,
                        valor_cobrado
                    FROM
                        ordem_servico_servicos
                    WHERE
                        ordem_servico_id = %s
                  """
            cursor.execute(sql, (ordem_servico_id,))
            resultados = cursor.fetchall()

            itens = []
            for resultado in resultados:
                servico = self.servico_dao.get_by_id(resultado[2]) if self.servico_dao else resultado[2]
                item = Ordem_servico_servico(
                    id=resultado[0],
                    ordem_servico_id=resultado[1],
                    servico=servico,
                    valor_cobrado=float(resultado[3])
                )
                itens.append(item)

            return itens

        finally:
            self.desconectar(cursor, conexao)

    def update(self, item):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE ordem_servico_servicos
                    SET
                        ordem_servico_id = %s,
                        servico_id = %s,
                        valor_cobrado = %s
                    WHERE
                        id = %s
                  """
            cursor.execute(
                sql,
                (
                    item.ordem_servico.id if hasattr(item.ordem_servico, 'id') else item.ordem_servico_id,
                    item.servico.id if hasattr(item.servico, 'id') else item.servico_id,
                    item.valor_cobrado,
                    item.id
                )
            )

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
            sql = "DELETE FROM ordem_servico_servicos WHERE id = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0

        except Exception:
            conexao.rollback()
            raise

        finally:
            self.desconectar(cursor, conexao)