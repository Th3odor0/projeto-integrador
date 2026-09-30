from app.view.crud_view_base import CrudViewBase


class Servico_View(CrudViewBase):
    TITULO = "Serviços"
    SUBTITULO = "Catálogo de serviços prestados pela oficina"
    MODULO = "servico"
    # chaves = atributos do model Servico = colunas de `servicos`
    CAMPOS = [
        ("nome", "Nome:"),
        ("descricao", "Descrição:"),
        ("valor_padrao", "Valor padrão (R$):"),
    ]
    COLUNAS_LARGURA = {
        "nome": 220,
        "descricao": 300,
        "valor_padrao": 130,
    }