from app.dao.simple_dao import SimpleDAO
from app.models.pecas import Peca


class PecaDAO(SimpleDAO):
    def __init__(self, database):
        super().__init__(
            database,
            tabela="pecas",
            colunas=["nome", "codigo", "quantidade_estoque", "preco_venda"],
            construtor=Peca,
            para_tupla=lambda peca: (
                peca.nome,
                peca.codigo,
                peca.quantidade_estoque,
                peca.preco_venda,
            ),
        )

    def get_all(self):
        # mantém o comportamento original: lista ordenada por nome
        return super().get_all(order_by="nome")