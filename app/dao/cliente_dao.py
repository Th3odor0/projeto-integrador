from app.dao.simple_dao import SimpleDAO
from app.models.cliente import Cliente


class ClienteDAO(SimpleDAO):
    def __init__(self, database):
        super().__init__(
            database,
            tabela="clientes",
            colunas=["nome", "cpf", "telefone", "email"],
            construtor=Cliente,
            para_tupla=lambda cliente: (
                cliente.nome,
                cliente.cpf,
                cliente.telefone,
                cliente.email,
            ),
        )

    def get_all(self):
        # mantém o comportamento original: lista sempre ordenada por nome
        return super().get_all(order_by="nome")