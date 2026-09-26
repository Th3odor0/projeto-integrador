from app.dao.dao import DAO
from app.models.equipamento import Equipamento


class EquipamentoDAO(DAO):
    """
    Não vira SimpleDAO porque cada Equipamento carrega o Cliente inteiro
    (não só o id) — é preciso consultar o ClienteDAO pra montar o objeto.
    """

    def __init__(self, database, cliente_dao):
        super().__init__(database)
        self._cliente_dao = cliente_dao

    def _montar_objeto(self, registro):
        cliente = self._cliente_dao.get_by_id(registro[5])
        return Equipamento(
            id=registro[0],
            tipo=registro[1],
            marca=registro[2],
            modelo=registro[3],
            numero_serie=registro[4],
            cliente_id=cliente,
        )

    def save(self, equipamento):
        conexao, cursor = self.conectar()
        try:
            sql = """
                INSERT INTO equipamentos
                (tipo, marca, modelo, numero_serie, cliente_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (
                    equipamento.tipo,
                    equipamento.marca,
                    equipamento.modelo,
                    equipamento.numero_serie,
                    equipamento.id_cliente,
                ),
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
            sql = """
                SELECT id, tipo, marca, modelo, numero_serie, cliente_id
                FROM equipamentos
                ORDER BY tipo
            """
            cursor.execute(sql)
            return [self._montar_objeto(registro) for registro in cursor.fetchall()]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        conexao, cursor = self.conectar()
        try:
            sql = """
                SELECT id, tipo, marca, modelo, numero_serie, cliente_id
                FROM equipamentos
                WHERE id = %s
            """
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
            return self._montar_objeto(registro) if registro else None
        finally:
            self.desconectar(cursor, conexao)

    def update(self, equipamento):
        conexao, cursor = self.conectar()
        try:
            sql = """
                UPDATE equipamentos
                SET tipo = %s, marca = %s, modelo = %s,
                    numero_serie = %s, cliente_id = %s
                WHERE id = %s
            """
            cursor.execute(
                sql,
                (
                    equipamento.tipo,
                    equipamento.marca,
                    equipamento.modelo,
                    equipamento.numero_serie,
                    equipamento.id_cliente,
                    equipamento.id,
                ),
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
            cursor.execute("DELETE FROM equipamentos WHERE id = %s", (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception:
            conexao.rollback()
            raise
        finally:
            self.desconectar(cursor, conexao)