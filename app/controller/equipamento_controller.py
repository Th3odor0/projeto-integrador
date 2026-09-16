# Ajuste o import abaixo conforme o caminho real do seu projeto
from app.models.equipamento import Equipamento


class EquipamentoController:

    def __init__(self, equipamento_dao, cliente_dao):
        self.dao = equipamento_dao
        self.cliente_dao = cliente_dao

    def _validar_dados(self, tipo, marca, modelo, numero_serie, id_cliente):
        erros = []

        if not tipo or not tipo.strip():
            erros.append("O tipo do equipamento é obrigatório.")

        if not marca or not marca.strip():
            erros.append("A marca é obrigatória.")

        if not modelo or not modelo.strip():
            erros.append("O modelo é obrigatório.")

        if not numero_serie or not numero_serie.strip():
            erros.append("O número de série é obrigatório.")

        if id_cliente is None or self.cliente_dao.get_by_id(id_cliente) is None:
            erros.append("Cliente não encontrado.")

        return erros

    def _numero_serie_ja_cadastrado(self, numero_serie):
        numero_serie = (numero_serie or "").strip()
        for equipamento in self.dao.get_all():
            if equipamento.numero_serie == numero_serie:
                return equipamento
        return None

    def cadastrar(self, tipo, marca, modelo, numero_serie, id_cliente):
        erros = self._validar_dados(tipo, marca, modelo, numero_serie, id_cliente)
        if erros:
            return False, "\n".join(erros)

        if self._numero_serie_ja_cadastrado(numero_serie):
            return False, "Já existe um equipamento cadastrado com esse número de série."

        equipamento = Equipamento(
            None, tipo.strip(), marca.strip(), modelo.strip(), numero_serie.strip(), id_cliente
        )

        try:
            equipamento = self.dao.save(equipamento)
            return True, equipamento
        except Exception as erro:
            return False, f"Erro ao cadastrar equipamento: {erro}"

    def atualizar(self, id, tipo, marca, modelo, numero_serie, id_cliente):
        equipamento = self.dao.get_by_id(id)
        if equipamento is None:
            return False, "Equipamento não encontrado."

        erros = self._validar_dados(tipo, marca, modelo, numero_serie, id_cliente)
        if erros:
            return False, "\n".join(erros)

        existente = self._numero_serie_ja_cadastrado(numero_serie)
        if existente and existente.id != id:
            return False, "Já existe outro equipamento cadastrado com esse número de série."

        equipamento.atualizar_dados(tipo.strip(), marca.strip(), modelo.strip(), numero_serie.strip())
        equipamento.id_cliente = id_cliente  # atualizar_dados não cobre id_cliente

        try:
            sucesso = self.dao.update(equipamento)
            if sucesso:
                return True, "Equipamento atualizado com sucesso."
            return False, "Não foi possível atualizar o equipamento."
        except Exception as erro:
            return False, f"Erro ao atualizar equipamento: {erro}"

    def excluir(self, id):
        if self.dao.get_by_id(id) is None:
            return False, "Equipamento não encontrado."

        try:
            sucesso = self.dao.delete(id)
            if sucesso:
                return True, "Equipamento excluído com sucesso."
            return False, "Não foi possível excluir o equipamento."
        except Exception as erro:
            return False, f"Erro ao excluir equipamento: {erro}"

    def buscar_por_id(self, id):
        return self.dao.get_by_id(id)

    def listar_todos(self):
        return self.dao.get_all()