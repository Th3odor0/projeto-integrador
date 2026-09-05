from app.models.pecas import Peca


class Ordem_Servico_Peca_DAO:

    def __init__(self, database):
        self._database = database

    def get_pecas_por_ordem_servico(self, ordem_servico):
        conexao = self._database.conectar()
        cursor = conexao.cursor()

        try:
            sql = """
                    SELECT
                        P.id,
                        P.nome,
                        P.codigo,
                        P.quantidade_estoque,
                        P.preco_venda,
                        OSP.quantidade,
                        OSP.valor_unitario
                    FROM
                        pecas P
                    INNER JOIN
                        ordem_servico_pecas OSP
                        ON OSP.peca_id = P.id
                    WHERE
                        OSP.ordem_servico_id = %s
                    ORDER BY
                        P.nome
                  """

            cursor.execute(sql, (ordem_servico.id,))
            registros = cursor.fetchall()

            pecas = []
            for registro in registros:
                peca = Peca(
                    id=registro[0],
                    nome=registro[1],
                    codigo=registro[2],
                    quantidade_estoque=registro[3],
                    preco_venda=registro[4]
                )
                peca.quantidade_os = registro[5]
                peca.valor_unitario_os = registro[6]
                pecas.append(peca)

            return pecas

        finally:
            self._database.desconectar(cursor, conexao)

    def substituir_pecas_da_ordem_servico(self, ordem_servico, pecas):
        conexao = self._database.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                """
                    DELETE FROM ordem_servico_pecas
                    WHERE ordem_servico_id = %s
                """,
                (ordem_servico.id,)
            )

            for peca in pecas:
                cursor.execute(
                    """
                        INSERT INTO ordem_servico_pecas
                        (
                            ordem_servico_id,
                            peca_id,
                            quantidade,
                            valor_unitario
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            %s,
                            %s
                        )
                    """,
                    (
                        ordem_servico.id,
                        peca.id,
                        getattr(peca, 'quantidade_os', 1),
                        getattr(peca, 'valor_unitario_os', peca.preco_venda)
                    )
                )

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            self._database.desconectar(cursor, conexao)