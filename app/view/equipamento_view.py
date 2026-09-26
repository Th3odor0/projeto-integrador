from app.view.crud_view_base import CrudViewBase


class EquipamentoView(CrudViewBase):
    TITULO = "Equipamentos"
    SUBTITULO = "Aparelhos recebidos para reparo"
    MODULO = "equipamento"
    CAMPOS = [
        {
            "chave": "id_cliente",
            "rotulo": "Cliente:",
            "carregar_opcoes": lambda self: self.cliente_dao.get_all(),
            "texto_opcao": lambda c: f"{c.id} - {c.nome}",
        },
        ("tipo", "Tipo:"),
        ("marca", "Marca:"),
        ("modelo", "Modelo:"),
        ("numero_serie", "Número de série:"),
    ]
    COLUNAS_LARGURA = {"id_cliente": 180, "numero_serie": 140}

    def __init__(self, master, controller, cliente_dao):
        # o cliente_dao precisa existir ANTES de super().__init__, porque o
        # __init__ da base já chama _carregar_opcoes_combos()
        self.cliente_dao = cliente_dao
        super().__init__(master, controller)