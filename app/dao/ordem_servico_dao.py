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
                    INSERT INTO ordens_servico
                    (
                        cliente_id,
                        funcionario_id,
                        equipamento_id,
                        data_entrada,
                        data_conclusao,
                        status,
                        problema,
                        diagnostico,
                        valor_total,
                        forma_pagamento,
                        dias_garantia
                    )
                    VALUES
                    (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                  """
            cursor.execute(
                sql,
                (
                    ordem_servico.cliente.id,
                    ordem_servico.funcionario.id,
                    ordem_servico.equipamento.id,
                    ordem_servico.data_entrada,
                    ordem_servico.data_conclusao,
                    ordem_servico.status,
                    ordem_servico.problema,
                    ordem_servico.diagnostico,
                    ordem_servico.valor_total,
                    ordem_servico.forma_pagamento,
                    ordem_servico.dias_garantia
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
                        id,
                        cliente_id,
                        funcionario_id,
                        equipamento_id,
                        data_entrada,
                        data_conclusao,
                        status,
                        problema,
                        diagnostico,
                        valor_total,
                        forma_pagamento,
                        dias_garantia
                    FROM
                        ordens_servico
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
                    data_entrada=resultado[4],
                    data_conclusao=resultado[5],
                    status=resultado[6],
                    problema=resultado[7],
                    diagnostico=resultado[8],
                    valor_total=resultado[9],
                    forma_pagamento=resultado[10],
                    dias_garantia=resultado[11]
                )
                ordens_servico.append(ordem_servico)

            return ordens_servico

        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT
                        id,
                        cliente_id,
                        funcionario_id,
                        equipamento_id,
                        data_entrada,
                        data_conclusao,
                        status,
                        problema,
                        diagnostico,
                        valor_total,
                        forma_pagamento,
                        dias_garantia
                    FROM
                        ordens_servico
                    WHERE
                        id = %s
                  """
            cursor.execute(sql, (id,))
            resultado = cursor.fetchone()

            if resultado:
                return Ordem_servico(
                    id=resultado[0],
                    cliente=self.cliente_dao.get_by_id(resultado[1]),
                    funcionario=self.funcionario_dao.get_by_id(resultado[2]),
                    equipamento=self.equipamento_dao.get_by_id(resultado[3]),
                    data_entrada=resultado[4],
                    data_conclusao=resultado[5],
                    status=resultado[6],
                    problema=resultado[7],
                    diagnostico=resultado[8],
                    valor_total=resultado[9],
                    forma_pagamento=resultado[10],
                    dias_garantia=resultado[11]
                )

            return None

        finally:
            self.desconectar(cursor, conexao)

    def update(self, ordem_servico):
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE ordens_servico
                    SET
                        cliente_id = %s,
                        funcionario_id = %s,
                        equipamento_id = %s,
                        data_entrada = %s,
                        data_conclusao = %s,
                        status = %s,
                        problema = %s,
                        diagnostico = %s,
                        valor_total = %s,
                        forma_pagamento = %s,
                        dias_garantia = %s
                    WHERE
                        id = %s
                  """
            cursor.execute(
                sql,
                (
                    ordem_servico.cliente.id,
                    ordem_servico.funcionario.id,
                    ordem_servico.equipamento.id,
                    ordem_servico.data_entrada,
                    ordem_servico.data_conclusao,
                    ordem_servico.status,
                    ordem_servico.problema,
                    ordem_servico.diagnostico,
                    ordem_servico.valor_total,
                    ordem_servico.forma_pagamento,
                    ordem_servico.dias_garantia,
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
            sql = "DELETE FROM ordens_servico WHERE id = %s"
            cursor.execute(sql, (id,))
            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            self.desconectar(cursor, conexao)