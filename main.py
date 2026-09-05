import tkinter as tk
from app.core.database import Database

# DAOs das entidades necessárias para Ordem de Serviço
from app.dao.cliente_dao import ClienteDAO
from app.dao.funcionario_dao import FuncionarioDAO
from app.dao.equipamento_dao import EquipamentoDAO
from app.dao.ordem_servico_dao import OrdemServicoDAO

# View
from app.view.ordem_servico_view import OrdemServicoView


class ErpApplication:

    def __init__(self):
        self._database = Database()
        self._root = tk.Tk()

        self._janela_ordem_servico = None

        self._configurar_janela()

        # 1. Instancia as DAOs dependentes
        self._dao_cliente = ClienteDAO(self._database)
        self._dao_funcionario = FuncionarioDAO(self._database)
        self._dao_equipamento = EquipamentoDAO(self._database)

        # 2. Injeta as dependências na DAO principal
        self._dao_ordem_servico = OrdemServicoDAO(
            self._database,
            self._dao_cliente,
            self._dao_funcionario,
            self._dao_equipamento
        )

        self._criar_menu()

    def _configurar_janela(self):
        self._root.title("Sistema ERP - Assistência Técnica")
        self._root.state("zoomed")

    def _criar_menu(self):
        menu_principal = tk.Menu(self._root)

        # Menu Atendimento
        menu_atendimento = tk.Menu(menu_principal, tearoff=0)
        menu_atendimento.add_command(
            label="Ordens de Serviço",
            command=self._abrir_ordem_servico
        )
        menu_principal.add_cascade(
            label="Atendimento",
            menu=menu_atendimento
        )

        # Encerrar aplicação
        menu_principal.add_command(
            label="Sair",
            command=self._root.destroy
        )

        self._root.config(menu=menu_principal)

    def _abrir_ordem_servico(self):
        # Evita duplicar a abertura da mesma janela no Tkinter
        if self._janela_ordem_servico is not None and self._janela_ordem_servico.winfo_exists():
            self._janela_ordem_servico.lift()
            self._janela_ordem_servico.focus_force()
            return

        janela = tk.Toplevel(self._root)
        self._janela_ordem_servico = janela
        OrdemServicoView(janela, self._dao_ordem_servico)

    def run(self):
        self._root.mainloop()


if __name__ == "__main__":
    app = ErpApplication()
    app.run()