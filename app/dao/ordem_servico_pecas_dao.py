# TRADUÇÃO PT/EN: a mensagem "Estoque insuficiente para a peça '{nome}'." agora passa por t() na hora do erro.
# Única alteração: import do t e a linha do raise ValueError em substituir_pecas_da_ordem_servico(); o resto é igual.
from app.core.idioma import t
from app.models.pecas import Peca


class OrdemServicoPecaDAO:
    def __init__(self, database):
        self.database = database

    def _conectar(self):
        conexao = self.database.conectar()
        cursor = conexao.cursor()
        return conexao, cursor

    def _desconectar(self, cursor, conexao):
        self.database.desconectar(cursor, conexao)

    def get_pecas_por_ordem_servico(self, ordem_servico):
        conexao, cursor = self._conectar()
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
            self._desconectar(cursor, conexao)

    def substituir_pecas_da_ordem_servico(self, ordem_servico, pecas):
        """
        Grava a lista de peças da ordem E acerta o estoque, tudo na mesma
        transação: ou salva tudo, ou não muda nada.

        O estoque é ajustado pela DIFERENÇA entre o que a ordem já tinha e o
        que está sendo salvo agora:
          - peça nova ou quantidade maior  -> sai do estoque a diferença
          - peça removida ou quantidade menor -> a diferença volta ao estoque
        O UPDATE é feito no próprio banco, com a condição estoque >= 0, então
        duas ordens salvando ao mesmo tempo não conseguem vender a mesma peça
        duas vezes.
        """
        conexao, cursor = self._conectar()
        try:
            # o que a ordem já reservou (trava essas linhas até o commit)
            cursor.execute(
                "SELECT peca_id, quantidade FROM ordem_servico_pecas "
                "WHERE ordem_servico_id = %s FOR UPDATE",
                (ordem_servico.id,),
            )
            antigas = {peca_id: quantidade for peca_id, quantidade in cursor.fetchall()}

            novas = {}
            nomes = {}
            for peca in pecas:
                quantidade = peca.quantidade_os
                novas[peca.id] = 1 if quantidade is None else quantidade
                nomes[peca.id] = peca.nome

            # ordem fixa de peça: evita deadlock entre duas ordens salvando juntas
            for peca_id in sorted(set(antigas) | set(novas)):
                diferenca = novas.get(peca_id, 0) - antigas.get(peca_id, 0)
                if diferenca == 0:
                    continue
                cursor.execute(
                    "UPDATE pecas SET quantidade_estoque = quantidade_estoque - %s "
                    "WHERE id = %s AND quantidade_estoque - %s >= 0",
                    (diferenca, peca_id, diferenca),
                )
                if cursor.rowcount == 0:
                    nome = nomes.get(peca_id, f"id {peca_id}")
                    raise ValueError(t("Estoque insuficiente para a peça '{nome}'.", nome=nome))  # TRADUÇÃO

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
                # Peca declara quantidade_os / valor_unitario_os como None,
                # então getattr(..., padrão) não serve mais: trata None aqui.
                quantidade = 1 if peca.quantidade_os is None else peca.quantidade_os
                valor = peca.preco_venda if peca.valor_unitario_os is None else peca.valor_unitario_os
                cursor.execute(sql_insert, (ordem_servico.id, peca.id, quantidade, valor))

            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            self._desconectar(cursor, conexao)