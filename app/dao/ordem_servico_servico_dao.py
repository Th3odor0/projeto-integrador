from app.models.ordem_servico_servico import Ordem_servico_servico


class Ordem_servico_Servico_Dao:
    """
    DAO para a tabela de junção entre Ordem de Serviço e Serviço.

    Ajuste nome de tabela/colunas conforme o schema real do seu banco —
    usei 'ordem_servico_servico' com as colunas (id, valor_cobrado,
    id_servico, id_ordem_servico) como um palpite razoável baseado na model.
    """

    def __init__(self, conexao):
        self.conexao = conexao

    def get_by_ordem_servico(self, ordem_servico_id):
        cursor = self.conexao.cursor()
        cursor.execute(
            "SELECT id, valor_cobrado, id_servico, id_ordem_servico "
            "FROM ordem_servico_servico WHERE id_ordem_servico = %s",
            (ordem_servico_id,),
        )
        linhas = cursor.fetchall()
        cursor.close()
        return [self._montar_objeto(linha) for linha in linhas]

    def get_by_id(self, id):
        cursor = self.conexao.cursor()
        cursor.execute(
            "SELECT id, valor_cobrado, id_servico, id_ordem_servico "
            "FROM ordem_servico_servico WHERE id = %s",
            (id,),
        )
        linha = cursor.fetchone()
        cursor.close()
        return self._montar_objeto(linha) if linha else None

    def save(self, item):
        cursor = self.conexao.cursor()
        cursor.execute(
            "INSERT INTO ordem_servico_servico (valor_cobrado, id_servico, id_ordem_servico) "
            "VALUES (%s, %s, %s)",
            (item.valor_cobrado, item.id_servico, item.id_ordem_servico),
        )
        self.conexao.commit()
        novo_id = cursor.lastrowid
        cursor.close()
        return Ordem_servico_servico(novo_id, item.valor_cobrado, item.id_servico, item.id_ordem_servico)

    def update(self, item):
        cursor = self.conexao.cursor()
        cursor.execute(
            "UPDATE ordem_servico_servico SET valor_cobrado = %s WHERE id = %s",
            (item.valor_cobrado, item.id),
        )
        self.conexao.commit()
        sucesso = cursor.rowcount > 0
        cursor.close()
        return sucesso

    def delete(self, id):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM ordem_servico_servico WHERE id = %s", (id,))
        self.conexao.commit()
        sucesso = cursor.rowcount > 0
        cursor.close()
        return sucesso

    @staticmethod
    def _montar_objeto(linha):
        id, valor_cobrado, id_servico, id_ordem_servico = linha
        return Ordem_servico_servico(id, float(valor_cobrado), id_servico, id_ordem_servico)