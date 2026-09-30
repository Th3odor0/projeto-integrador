from app.view.crud_view_base import CrudViewBase


class Funcionario_View(CrudViewBase):
    TITULO = "Funcionários"
    SUBTITULO = "Cadastro de funcionários"
    MODULO = "funcionario"
    # chaves = atributos do model Funcionario = colunas de `funcionarios`
    CAMPOS = [
        ("nome", "Nome:"),
        ("cpf", "CPF:"),
        ("cargo", "Cargo:"),
    ]
    COLUNAS_LARGURA = {
        "nome": 220,
        "cpf": 130,
        "cargo": 160,
    }