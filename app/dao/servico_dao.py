from app.dao.simple_dao import SimpleDAO
from app.models.servico import Servico


class ServicoDAO(SimpleDAO):
    def __init__(self, database):
        super().__init__(
            database,
            tabela="servicos",
            colunas=["nome", "descricao", "valor_padrao"],
            construtor=Servico,
            para_tupla=lambda servico: (
                servico.nome,
                servico.descricao,
                servico.valor_padrao,
            ),
        )

    def get_all(self):
        # mantém o comportamento original: lista ordenada por nome
        return super().get_all(order_by="nome")