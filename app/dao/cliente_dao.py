from app.dao.dao import DAO
from app.models.cliente import Cliente

class Cliente_DAO(DAO):
    def __init__(self, database):
        super().__init__(database)

    def save(self, cliente):
        conexao, cursor = self.conectar()
        try: 
            sql = """
                    INSERT INTO CLIENTES
                    (
                        NOME,
                        CPF,
                        TELEFONE,
                        EMAIL
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s
                    )
                  """
            cursor.execute(
                sql,
                (
                    cliente.nome,
                    cliente.cpf,
                    cliente.telefone,
                    cliente.email
                )
            )
            
            conexao.commit()
            
            cliente.id = cursor.lastrowid

            return cliente
        
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
                        TELEFONE,
                        EMAIL
                    FROM 
                        CLIENTES
                    ORDER BY
                        NOME
                  """
            
            cursor.execute(sql)

            registros = cursor.fetchall()

            clientes = []

            for registro in registros:
                clientes.append(
                    Cliente( 
                    registro[0],
                    registro[1],
                    registro[2],
                    registro[3],
                    registro[4]
                    )
                )
            return clientes
        
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
                        TELEFONE,
                        EMAIL
                    FROM
                        CLIENTES
                    WHERE
                        ID = %s
                  """
            
            cursor.execute(sql, (id,))

            registro = cursor.fetchone()

            if registro is None:
                return None
            
            return Cliente(
                registro[0],
                registro[1],
                registro[2],
                registro[3],
                registro[4]
            )
        
        finally:
            self.desconectar(cursor, conexao)

    def update(self, cliente):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE CLIENTES
                    SET
                        NOME = %s,
                        CPF = %s,
                        TELEFONE = %s,
                        EMAIL = %s
                    WHERE
                        ID = %s
                  """
            
            cursor.execute(
                sql,
                (
                    cliente.nome,
                    cliente.cpf,
                    cliente.telefone,
                    cliente.email,
                    cliente.id
                )
            )

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
            sql ="""
                    DELETE
                    FROM CLIENTES
                    WHERE ID = %s
                 """
            
            cursor.execute(sql, (id,))

            conexao.commit()

            return cursor.rowcount > 0
        
        except Exception:
            conexao.rollback()
            raise

        finally:
            self.desconectar(cursor, conexao)