from app.view.crud_view_base import CrudViewBase

class Peca_View(CrudViewBase):
    TITULO = "Peças"
    SUBTITULO = "Cadastro de peças"
    MODULO = "peca"
    CAMPOS = [
        ("nome", "Nome:"),
        ("descricao", "Descrição:"),
        ("preco", "Preço:"),
    ]
    COLUNAS_LARGURA = {
        "nome": 200,
        "descricao": 300,
        "preco": 100,
    }