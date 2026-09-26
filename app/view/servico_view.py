from app.view.crud_view_base import CrudViewBase

class Servico_View(CrudViewBase):
    TITULO = "Serviços"
    SUBTITULO = "Cadastro de serviços"
    MODULO = "servico"
    CAMPOS = [
        ("nome", "Nome"),
        ("descricao", "Descrição"),
        ("preco", "Preço"),
    ]
    COLUNAS_LARGURA = {
        "nome": 200,
        "descricao": 300,
        "preco": 100,
    }