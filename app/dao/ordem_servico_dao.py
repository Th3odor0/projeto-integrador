from app.dao.dao import DAO
from app.models.ordens_servico import Ordem_servico

class Ordem_servico_DAO(DAO):
    def __init__(self, database, cliente_dao, funcionario_dao, equipamento_dao):
        super().__init__(database)
        self.cliente_dao = cliente_dao
        self.funcionario_dao = funcionario_dao
        self.equipamento_dao = equipamento_dao

    def save(self, ordem_servico):
        conexao, cursor = self.conectar()
        try: 
            sql = """
                    INSERT INTO ORDEM_SERVICO
                    (
                        ID_CLIENTE,
                        ID_FUNCIONARIO,
                        ID_EQUIPAMENTO,
                        DATA_ABERTURA,
                        DATA_FECHAMENTO,
                        STATUS,
                        DESCRICAO
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                  """
            cursor.execute(
                sql,
                (
                    ordem_servico.cliente.id,
                    ordem_servico.funcionario.id,
                    ordem_servico.equipamento.id,
                    ordem_servico.data_abertura,
                    ordem_servico.data_fechamento,
                    ordem_servico.status,
                    ordem_servico.descricao
                )
            )
            
            conexao.commit()
            
            ordem_servico.id = cursor.lastrowid

            return ordem_servico
        
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
                        ID_CLIENTE,
                        ID_FUNCIONARIO,
                        ID_EQUIPAMENTO,
                        DATA_ABERTURA,
                        DATA_FECHAMENTO,
                        STATUS,
                        DESCRICAO
                    FROM
                        ORDEM_SERVICO
                  """
            cursor.execute(sql)
            resultados = cursor.fetchall()

            ordens_servico = []
            for resultado in resultados:
                ordem_servico = Ordem_servico(
                    id=resultado[0],
                    cliente=self.cliente_dao.get_by_id(resultado[1]),
                    funcionario=self.funcionario_dao.get_by_id(resultado[2]),
                    equipamento=self.equipamento_dao.get_by_id(resultado[3]),
                    data_abertura=resultado[4],
                    data_fechamento=resultado[5],
                    status=resultado[6],
                    descricao=resultado[7]
                )
                ordens_servico.append(ordem_servico)

            return ordens_servico

        except Exception:
            raise

        finally:
            self.desconectar(cursor, conexao)                                   

    def get_by_id(self, id):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT
                        ID,
                        ID_CLIENTE,
                        ID_FUNCIONARIO,
                        ID_EQUIPAMENTO,
                        DATA_ABERTURA,
                        DATA_FECHAMENTO,
                        STATUS,
                        DESCRICAO
                    FROM
                        ORDEM_SERVICO
                    WHERE
                        ID = %s
                  """
            cursor.execute(sql, (id,))
            resultado = cursor.fetchone()

            if resultado:
                ordem_servico = Ordem_servico(
                    id=resultado[0],
                    cliente=self.cliente_dao.get_by_id(resultado[1]),
                    funcionario=self.funcionario_dao.get_by_id(resultado[2]),
                    equipamento=self.equipamento_dao.get_by_id(resultado[3]),
                    data_abertura=resultado[4],
                    data_fechamento=resultado[5],
                    status=resultado[6],
                    descricao=resultado[7]
                )
                return ordem_servico

            return None

        except Exception:
            raise

        finally:
            self.desconectar(cursor, conexao)                                   

    def update(self, ordem_servico):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE ORDEM_SERVICO
                    SET
                        ID_CLIENTE = %s,
                        ID_FUNCIONARIO = %s,
                        ID_EQUIPAMENTO = %s,
                        DATA_ABERTURA = %s,
                        DATA_FECHAMENTO = %s,
                        STATUS = %s,
                        DESCRICAO = %s
                    WHERE
                        ID = %s
                  """
            cursor.execute(
                sql,
                (
                    ordem_servico.cliente.id,
                    ordem_servico.funcionario.id,
                    ordem_servico.equipamento.id,
                    ordem_servico.data_abertura,
                    ordem_servico.data_fechamento,
                    ordem_servico.status,
                    ordem_servico.descricao,
                    ordem_servico.id
                )
            )
            
            conexao.commit()

            return ordem_servico
        
        except Exception:
            conexao.rollback()
            raise

        finally:
            self.desconectar(cursor, conexao)


    def delete(self, id):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    DELETE FROM ORDEM_SERVICO
                    WHERE ID = %s
                  """
            cursor.execute(sql, (id,))
            
            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            self.desconectar(cursor, conexao)