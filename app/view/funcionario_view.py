from app.view.crud_view_base import CrudViewBase

class Funcionario_View(CrudViewBase):
    TITULO = "Funcionários"
    SUBTITULO = "Cadastro de funcionários"
    MODULO = "funcionario"
    CAMPOS = [
        ("nome", "Nome:"),
        ("email", "Email:"),
        ("telefone", "Telefone:"),
        ("cargo", "Cargo:"),
    ]
    COLUNAS_LARGURA = {
        "nome": 200,
        "email": 200,
        "telefone": 150,
        "cargo": 150,
    }