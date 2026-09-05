from app.dao.dao import DAO 
from app.models.pecas import Peca

class PecaDAO(DAO):
    def __init__(self, database):
        super().__init__(database)

def save(self, peca):
        conexao, cursor = self.conectar()
        try: 
            sql = """
                    INSERT INTO PECAS
                    (
                        NOME,
                        CODIGO,
                        QUANTIDADE_ESTOQUE,
                        PRECO_VENDA
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
                    peca.nome,
                    peca.codigo,
                    peca.quantidade_estoque,
                    peca.preco_venda
                )
            )
            
            conexao.commit()
            
            peca.id = cursor.lastrowid

            return peca
        
        except Exception:
            conexao.rollback()
            raise

        finally:
            self.desconectar(cursor, conexao)

def get_all(self):
     conexao, cursor = self.conectar()
     try:
        sql ="""
                SELECT
                    ID,
                    NOME,
                    CODIGO,
                    QUANTIDADE_ESTOQUE,
                    PRECO_VENDA
                FROM
                    PECAS
                ORDER BY
                    NOME
             """
        cursor.execute(sql)
        registros = cursor.fetchall()
        pecas = []
        for registro in registros:
            pecas.append(
                Peca(
                registro[0],
                registro[1],    
                registro[2],
                registro[3],
                registro[4]
                )
            )
        return pecas
     finally:
        self.desconectar(cursor, conexao)

def get_by_id(self, id):
    conexao, cursor = self.conectar()
    try:
        sql = """
                SELECT
                    ID,
                    NOME,
                    CODIGO,
                    QUANTIDADE_ESTOQUE,
                    PRECO_VENDA
                FROM
                    PECAS
                WHERE
                    ID = %s
              """
        cursor.execute(sql, (id,))
        registro = cursor.fetchone()
        if registro:
            return Peca(
                registro[0],
                registro[1],
                registro[2],
                registro[3],
                registro[4]
            )
        else:
            return None
    finally:
        self.desconectar(cursor, conexao)

def update(self, peca):
    conexao, cursor = self.conectar()
    try:
        sql = """
                UPDATE PECAS
                SET
                    NOME = %s,
                    CODIGO = %s,
                    QUANTIDADE_ESTOQUE = %s,
                    PRECO_VENDA = %s
                WHERE
                    ID = %s
              """
        cursor.execute(
            sql,
            (
                peca.nome,
                peca.codigo,
                peca.quantidade_estoque,
                peca.preco_venda,
                peca.id
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
                DELETE
                FROM PECAS
                WHERE
                    ID = %s
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