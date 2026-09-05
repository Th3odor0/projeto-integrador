from app.dao.dao import DAO
from app.models.funcionario import Funcionario

class Funcionario_DAO(DAO):
    def __init__(self, database):
        super().__init__(database)

    def save(self, funcionario):
        conexao, cursor = self.conectar()
        try: 
            sql = """
                    INSERT INTO FUNCIONARIOS
                    (
                        NOME,
                        CPF,
                        CARGO
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
                    funcionario.nome,
                    funcionario.cpf,
                    funcionario.cargo
                )
            )
            
            conexao.commit()
            
            funcionario.id = cursor.lastrowid

            return funcionario
        
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
                        CPF,
                        CARGO
                    FROM 
                        FUNCIONARIOS
                    ORDER BY
                        NOME
                  """
            
            conexao.execute(sql)

            registros = cursor.fetchall()

            funcionarios = []

            for registro in registros:
                funcionarios.append(
                    Funcionario( 
                    registro[0],
                    registro[1],
                    registro[2],
                    registro[3]
                    )
                )
            return funcionarios
        
        finally:
            self.desconectar(cursor, conexao)   

    def get_by_id(self, id):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT
                        ID,
                        NOME,
                        CPF,
                        CARGO
                    FROM 
                        FUNCIONARIOS
                    WHERE
                        ID = %s
                  """
            
            cursor.execute(sql, (id,))

            registro = cursor.fetchone()

            if registro:
                return Funcionario(
                    registro[0],
                    registro[1],
                    registro[2],
                    registro[3]
                )
            else:
                return None
        
        finally:
            self.desconectar(cursor, conexao)

    def update(self, funcionario):
        conexao, cursor = self.conectar()
        try:
            sql ="""
                   UPDATE FUNCIONARIOS
                   SET
                        NOME = %s,
                        CPF = %s,
                        CARGO = %s
                   WHERE
                        ID = %s
                 """
            cursor.execute(
                sql,
                (
                    funcionario.nome,
                    funcionario.cpf,
                    funcionario.cargo,
                    funcionario.id
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
                    DELETE FROM FUNCIONARIOS
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