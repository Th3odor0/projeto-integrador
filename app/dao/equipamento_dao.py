from app.dao.dao import DAO
from app.models.equipamento import Equipamento

class EquipamentoDAO(DAO):
    def __init__(self, database, cliente_dao):
        super().__init__(database)
        self._cliente = cliente_dao
        
def save(self, equipamento):
    conexao, cursor = self.conectar()
    try:
        sql = """
                INSERT INTO EQUIPAMENTOS
                (
                    TIPO,
                    MARCA,
                    MODELO,
                    NUMERO_SERIE,
                    CLIENTE_ID
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
                equipamento.tipo,
                equipamento.marca,
                equipamento.modelo,
                equipamento.numero_serie,
                equipamento.cliente_id
            )
        )
        
        conexao.commit()
        
        equipamento.id = cursor.lastrowid

        return equipamento
    
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
                    TIPO,
                    MARCA,
                    MODELO,
                    NUMERO_SERIE,
                    CLIENTE_ID
                FROM
                    EQUIPAMENTOS
                ORDER BY
                    NOME    
              """
        cursor.execute(sql)
        registros = cursor.fetchall()
        equipamentos = []
        for registro in registros:
            cliente_id = self._cliente.dao.get_by_id(
                registro[5]
            )
            equipamentos.append(
                Equipamento(
                    registro[0],
                    registro[1],
                    registro[2],
                    registro[3],
                    registro[4]
                )                
            )
        return equipamentos
    finally:
        self.desconectar(cursor, conexao)

def get_by_id(self, id):
    conexao, cursor = self.conectar()
    try:
        sql = """
                SELECT
                    ID,
                    TIPO,
                    MARCA,
                    MODELO,
                    NUMERO_SERIE,
                    CLIENTE_ID
                FROM
                    EQUIPAMENTOS
                WHERE
                    ID = %s
              """
        cursor.execute(sql, (id,))
        registro = cursor.fetchone()
        if registro:
            cliente_id = self._cliente.dao.get_by_id(
                registro[5]
            )
            return Equipamento(
                registro[0],
                registro[1],
                registro[2],
                registro[3],
                registro[4]
            )
        return None
    finally:
        self.desconectar(cursor, conexao)

def update(self, equipamento):
    conexao, cursor = self.conectar()
    try:
        sql = """
                UPDATE EQUIPAMENTOS
                SET
                    TIPO = %s,
                    MARCA = %s,
                    MODELO = %s,
                    NUMERO_SERIE = %s,
                    CLIENTE_ID = %s
                WHERE
                    ID = %s
              """
        cursor.execute(
            sql,
            (
                equipamento.tipo,
                equipamento.marca,
                equipamento.modelo,
                equipamento.numero_serie,
                equipamento.cliente_id,
                equipamento.id
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
        sql = """
                DELETE FROM EQUIPAMENTOS
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