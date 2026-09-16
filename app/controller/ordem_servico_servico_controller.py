from app.models.ordem_servico_servico import Ordem_servico_servico


class Ordem_servico_Servico_Controller:
    """
    Controller para vincular serviços prestados a uma Ordem de Serviço.

    Segue a convenção "levanta exceção" (igual Ordem_servico_Controller),
    porque é assim que Ordem_servico_Servico_View trata os erros — com
    try/except ValueError/Exception em volta de controller.adicionar().
    """

    def __init__(self, ordem_servico_servico_dao, servico_dao, ordem_servico_dao):
        self.dao = ordem_servico_servico_dao
        self.servico_dao = servico_dao
        self.ordem_servico_dao = ordem_servico_dao

    def listar_por_ordem(self, ordem_servico_id):
        """
        A view usa item.servico.nome pra montar a Treeview, mas a model só
        guarda id_servico — então resolvemos o objeto Servico aqui e o
        penduramos como atributo dinâmico antes de devolver.
        """
        itens = self.dao.get_by_ordem_servico(ordem_servico_id)
        for item in itens:
            item.servico = self.servico_dao.get_by_id(item.id_servico)
        return itens

    def adicionar(self, ordem_servico_id, servico_id, valor_cobrado):
        if self.ordem_servico_dao.get_by_id(ordem_servico_id) is None:
            raise ValueError(f"Ordem de serviço com id {ordem_servico_id} não encontrada.")

        servico = self.servico_dao.get_by_id(servico_id)
        if servico is None:
            raise ValueError(f"Serviço com id {servico_id} não encontrado.")

        try:
            valor_cobrado = float(valor_cobrado)
        except (TypeError, ValueError):
            raise ValueError("Valor cobrado precisa ser um número.")

        if valor_cobrado < 0:
            raise ValueError("Valor cobrado não pode ser negativo.")

        novo_item = Ordem_servico_servico(
            id=None,
            valor_cobrado=valor_cobrado,
            id_servico=servico_id,
            id_ordem_servico=ordem_servico_id,
        )
        return self.dao.save(novo_item)

    def remover(self, id):
        if self.dao.get_by_id(id) is None:
            raise ValueError(f"Item com id {id} não encontrado.")
        self.dao.delete(id)