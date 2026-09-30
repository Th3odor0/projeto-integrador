from app.dao.simple_dao import SimpleDAO
from app.models.funcionario import Funcionario


class FuncionarioDAO(SimpleDAO):
    def __init__(self, database):
        super().__init__(
            database,
            tabela="funcionarios",
            colunas=["nome", "cpf", "cargo"],
            construtor=Funcionario,
            para_tupla=lambda funcionario: (
                funcionario.nome,
                funcionario.cpf,
                funcionario.cargo,
            ),
        )

    def get_all(self):
        # mantém o comportamento original: lista ordenada por nome
        return super().get_all(order_by="nome")