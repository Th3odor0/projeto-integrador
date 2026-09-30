from app.core.idioma import t
from app.models.ordem_servico_servico import Ordem_servico_servico


class Ordem_servico_Servico_Controller:
    """
    Controller para vincular serviços prestados a uma Ordem de Serviço.

    Segue a mesma convenção do Cliente_controller (usada por Cliente_view):
    todo método público retorna (sucesso: bool, resultado) e nunca levanta
    exceção pra fora — a view só precisa checar o booleano.
    """

    def __init__(self, ordem_servico_servico_dao, servico_dao, ordem_servico_dao):
        self.dao = ordem_servico_servico_dao
        self.servico_dao = servico_dao
        self.ordem_servico_dao = ordem_servico_dao

    def buscar_por_ordem(self, ordem_servico_id):
        """
        A view usa item.servico.nome pra montar a Treeview, mas a model só
        guarda id_servico — então resolvemos o objeto Servico aqui e o
        penduramos como atributo dinâmico antes de devolver.
        """
        try:
            itens = self.dao.get_by_ordem_servico(ordem_servico_id)
        except Exception as erro:
            return False, f"{t('Erro ao buscar serviços da ordem:')} {erro}"

        for item in itens:
            item.servico = self.servico_dao.get_by_id(item.id_servico)

        return True, itens

    def cadastrar(self, ordem_servico_id, servico_id, valor_cobrado):
        if self.ordem_servico_dao.get_by_id(ordem_servico_id) is None:
            return False, t("Ordem de serviço com id {id} não encontrada.", id=ordem_servico_id)

        if self.servico_dao.get_by_id(servico_id) is None:
            return False, t("Serviço com id {id} não encontrado.", id=servico_id)

        try:
            valor_cobrado = float(valor_cobrado)
        except (TypeError, ValueError):
            return False, t("Valor cobrado precisa ser um número.")

        if valor_cobrado < 0:
            return False, t("Valor cobrado não pode ser negativo.")

        novo_item = Ordem_servico_servico(
            id=None,
            valor_cobrado=valor_cobrado,
            id_servico=servico_id,
            id_ordem_servico=ordem_servico_id,
        )

        try:
            item = self.dao.save(novo_item)
            return True, item
        except Exception as erro:
            return False, f"{t('Erro ao adicionar serviço:')} {erro}"

    def atualizar(self, id, valor_cobrado):
        """Só o valor cobrado é editável — o serviço vinculado não muda depois de criado."""
        item = self.dao.get_by_id(id)
        if item is None:
            return False, t("Item não encontrado.")

        try:
            valor_cobrado = float(valor_cobrado)
        except (TypeError, ValueError):
            return False, t("Valor cobrado precisa ser um número.")

        if valor_cobrado < 0:
            return False, t("Valor cobrado não pode ser negativo.")

        item.atualizar_dados(valor_cobrado)

        try:
            sucesso = self.dao.update(item)
            if sucesso:
                return True, t("Valor atualizado com sucesso.")
            return False, t("Não foi possível atualizar o valor.")
        except Exception as erro:
            return False, f"{t('Erro ao atualizar:')} {erro}"

    def deletar(self, id):
        if self.dao.get_by_id(id) is None:
            return False, t("Item não encontrado.")

        try:
            sucesso = self.dao.delete(id)
            if sucesso:
                return True, t("Serviço removido com sucesso.")
            return False, t("Não foi possível remover o serviço.")
        except Exception as erro:
            return False, f"{t('Erro ao remover:')} {erro}"