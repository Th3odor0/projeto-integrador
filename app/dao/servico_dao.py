from app.dao.dao import DAO
from app.models.servico import Servico

class ServicoDAO(DAO):
    def __init__(self, database):
        super().__init__(database)

    def save(self, servico):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    INSERT INTO SERVICOS
                    (
                        NOME,
                        DESCRICAO,
                        VALOR_PADRAO
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s
                    )
                  """
            cursor.execute(
                sql,
                (
                    servico.nome,
                    servico.descricao,
                    servico.valor_padrao
                )
            )

            conexao.commit()

            servico.id = cursor.lastrowid

            return servico

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
                        ID,
                        NOME,
                        DESCRICAO,
                        VALOR_PADRAO
                    FROM
                        SERVICOS
                    ORDER BY
                        NOME
                  """

            cursor.execute(sql)

            registros = cursor.fetchall()

            servicos = []

            for registro in registros:
                servicos.append(
                    Servico(
                        registro[0],
                        registro[1],
                        registro[2],
                        registro[3]
                    )
                )
            return servicos

        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT
                        ID,
                        NOME,
                        DESCRICAO,
                        VALOR_PADRAO
                    FROM
                        SERVICOS
                    WHERE
                        ID = %s
                  """

            cursor.execute(sql, (id,))

            registro = cursor.fetchone()

            if registro:
                return Servico(
                    registro[0],
                    registro[1],
                    registro[2],
                    registro[3]
                )
            else:
                return None

        finally:
            self.desconectar(cursor, conexao)

    def update(self, servico):
        conexao, cursor = self.conectar()
        try:
            sql = """
                   UPDATE SERVICOS
                   SET
                        NOME = %s,
                        DESCRICAO = %s,
                        VALOR_PADRAO = %s
                   WHERE
                        ID = %s
                 """
            cursor.execute(
                sql,
                (
                    servico.nome,
                    servico.descricao,
                    servico.valor_padrao,
                    servico.id
                )
            )
            conexao.commit()
            sucesso = cursor.rowcount > 0
            return sucesso
        except Exception:
            conexao.rollback()
            raise
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    DELETE FROM SERVICOS
                    WHERE ID = %s
                  """
            cursor.execute(sql, (id,))
            conexao.commit()
            sucesso = cursor.rowcount > 0
            return sucesso
        except Exception:
            conexao.rollback()
            raise
        finally:
            self.desconectar(cursor, conexao)