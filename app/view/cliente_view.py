from app.view.crud_view_base import CrudViewBase

class Cliente_View(CrudViewBase):
    TITULO = "Clientes"
    SUBTITULO = "Cadastro de clientes"
    MODULO = "cliente"
    CAMPOS = [
        ("nome", "Nome:"),
        ("email", "Email:"),
        ("telefone", "Telefone:"),
        ("endereco", "Endereço:"),
    ]
    COLUNAS_LARGURA = {
        "nome": 200,
        "email": 200,
        "telefone": 150,
        "endereco": 300,
    }