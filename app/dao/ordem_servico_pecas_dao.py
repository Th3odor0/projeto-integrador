from app.dao.dao import ConexaoMixin
from app.models.pecas import Peca


class OrdemServicoPecaDAO(ConexaoMixin):
    def __init__(self, database):
        super().__init__(database)

    def get_pecas_por_ordem_servico(self, ordem_servico):
        conexao, cursor = self.conectar()
        try:
            sql = """
                SELECT
                    p.id, p.nome, p.codigo, p.quantidade_estoque, p.preco_venda,
                    osp.quantidade, osp.valor_unitario
                FROM pecas p
                INNER JOIN ordem_servico_pecas osp ON osp.peca_id = p.id
                WHERE osp.ordem_servico_id = %s
                ORDER BY p.nome
            """
            cursor.execute(sql, (ordem_servico.id,))

            pecas = []
            for registro in cursor.fetchall():
                peca = Peca(
                    id=registro[0],
                    nome=registro[1],
                    codigo=registro[2],
                    quantidade_estoque=registro[3],
                    preco_venda=registro[4],
                )
                peca.quantidade_os = registro[5]
                peca.valor_unitario_os = registro[6]
                pecas.append(peca)
            return pecas
        finally:
            self.desconectar(cursor, conexao)

    def substituir_pecas_da_ordem_servico(self, ordem_servico, pecas):
        conexao, cursor = self.conectar()
        try:
            cursor.execute(
                "DELETE FROM ordem_servico_pecas WHERE ordem_servico_id = %s",
                (ordem_servico.id,),
            )

            sql_insert = """
                INSERT INTO ordem_servico_pecas
                (ordem_servico_id, peca_id, quantidade, valor_unitario)
                VALUES (%s, %s, %s, %s)
            """
            for peca in pecas:
                cursor.execute(
                    sql_insert,
                    (
                        ordem_servico.id,
                        peca.id,
                        getattr(peca, "quantidade_os", 1),
                        getattr(peca, "valor_unitario_os", peca.preco_venda),
                    ),
                )

            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            self.desconectar(cursor, conexao)