from app.view.crud_view_base import CrudViewBase

class Peca_View(CrudViewBase):
    TITULO = "Peças"
    SUBTITULO = "Estoque de peças utilizadas nos reparos"
    MODULO = "peca"
    # chaves = atributos do model Peca = colunas de `pecas`
    CAMPOS = [
        ("nome", "Nome:"),
        ("codigo", "Código:"),
        ("quantidade_estoque", "Qtd. em estoque:"),
        ("preco_venda", "Preço de venda (R$):"),
    ]
    COLUNAS_LARGURA = {
        "nome": 220,
        "codigo": 110,
        "quantidade_estoque": 120,
        "preco_venda": 130,
    }