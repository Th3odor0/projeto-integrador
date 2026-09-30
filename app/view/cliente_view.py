from app.view.crud_view_base import CrudViewBase

class Cliente_View(CrudViewBase):
    TITULO = "Clientes"
    SUBTITULO = "Cadastro de clientes"
    MODULO = "cliente"
    # chaves = atributos do model Cliente = colunas de `clientes`
    CAMPOS = [
        ("nome", "Nome:"),
        ("cpf", "CPF:"),
        ("telefone", "Telefone:"),
        ("email", "Email:"),
    ]
    COLUNAS_LARGURA = {
        "nome": 220,
        "cpf": 130,
        "telefone": 130,
        "email": 220,
    }