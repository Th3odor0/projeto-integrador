import tkinter as tk
from app.core.database import Database

# DAOs
from app.dao.cliente_dao import Cliente_DAO
from app.dao.funcionario_dao import Funcionario_DAO
from app.dao.equipamento_dao import EquipamentoDAO
from app.dao.ordem_servico_dao import Ordem_servico_DAO
from app.dao.ordem_servico_pecas_dao import Ordem_Servico_Peca_DAO
from app.dao.peca_dao import PecaDAO
from app.dao.servico_dao import ServicoDAO
from app.dao.ordem_servico_servico_dao import Ordem_servico_Servico_Dao

# Controllers
from app.controller.ordem_servico_controller import Ordem_servico_Controller
from app.controller.cliente_controller import ClienteController
from app.controller.funcionario_controller import FuncionarioController
from app.controller.peca_controller import PecaController
from app.controller.servico_controller import ServicoController
from app.controller.equipamento_controller import EquipamentoController
from app.controller.ordem_servico_servico_controller import Ordem_servico_Servico_Controller

# Views principais (Views de tabelas associativas removidas)
from app.view.ordem_servico_view import Ordem_servico_View
from app.view.cliente_view import Cliente_view
from app.view.equipamento_view import Equipamento_View
from app.view.funcionario_view import Funcionario_View
from app.view.servico_view import Servico_View
from app.view.peca_view import Peca_View


class ErpApplication:

    def __init__(self):
        self._database = Database()
        self._root = tk.Tk()

        # Controle de janelas ativas
        self._janela_ordem_servico = None
        self._janela_cliente = None
        self._janela_funcionario = None
        self._janela_equipamento = None
        self._janela_servico = None
        self._janela_peca = None

        self._configurar_janela()

        # Instanciação das DAOs
        self._dao_cliente = Cliente_DAO(self._database)
        self._dao_funcionario = Funcionario_DAO(self._database)
        self._dao_equipamento = EquipamentoDAO(self._database, self._dao_cliente)
        self._dao_peca = PecaDAO(self._database)
        self._dao_servico = ServicoDAO(self._database)
        self._dao_servico_servico = Ordem_servico_Servico_Dao(self._database)
        self._dao_peca_peca = Ordem_Servico_Peca_DAO(self._database)

        self._dao_ordem_servico = Ordem_servico_DAO(
            self._database,
            self._dao_cliente,
            self._dao_funcionario,
            self._dao_equipamento
        )

        # Instanciação dos Controllers
        self._controller_ordem_servico = Ordem_servico_Controller(
            self._dao_ordem_servico,
            self._dao_cliente,
            self._dao_funcionario,
            self._dao_equipamento
        )
        self._controller_cliente = ClienteController(self._dao_cliente)
        self._controller_funcionario = FuncionarioController(self._dao_funcionario)
        self._controller_peca = PecaController(self._dao_peca)
        self._controller_servico = ServicoController(self._dao_servico)
        self._controller_equipamento = EquipamentoController(self._dao_equipamento, self._dao_cliente)
        self._controller_servico_servico = Ordem_servico_Servico_Controller(
            self._dao_servico_servico,
            self._dao_servico,
            self._dao_ordem_servico
        )

        self._criar_menu()

    def _configurar_janela(self):
        self._root.title("Sistema ERP - Assistência Técnica")
        self._root.state("zoomed")

    def _criar_menu(self):
        menu_principal = tk.Menu(self._root)

        menu_atendimento = tk.Menu(menu_principal, tearoff=0)
        menu_atendimento.add_command(
            label="Ordens de Serviço",
            command=self._abrir_ordem_servico
        )
        menu_atendimento.add_command(
            label="Clientes",
            command=self._abrir_cliente
        )
        menu_atendimento.add_command(
            label="Funcionarios",
            command=self._abrir_funcionario
        )
        menu_atendimento.add_command(
            label="Equipamentos",
            command=self._abrir_equipamento
        )
        menu_atendimento.add_command(
            label="Serviços",
            command=self._abrir_servico
        )
        menu_atendimento.add_command(
            label="Peças",
            command=self._abrir_peca
        )
        
        menu_principal.add_cascade(
            label="Atendimento",
            menu=menu_atendimento
        )

        menu_principal.add_command(
            label="Sair",
            command=self._root.destroy
        )

        self._root.config(menu=menu_principal)

    def _abrir_ordem_servico(self):
        if self._janela_ordem_servico is not None and self._janela_ordem_servico.winfo_exists():
            self._janela_ordem_servico.lift()
            self._janela_ordem_servico.focus_force()
            return

        janela = tk.Toplevel(self._root)
        self._janela_ordem_servico = janela

        # Injeta todos os controllers e DAOs que as abas internas da OS necessitam
        Ordem_servico_View(
            janela,
            self._controller_ordem_servico,
            self._controller_servico_servico,
            self._dao_cliente,
            self._dao_funcionario,
            self._dao_equipamento,
            self._dao_servico,
            self._dao_peca
        )

    def _abrir_cliente(self):
        if self._janela_cliente is not None and self._janela_cliente.winfo_exists():
            self._janela_cliente.lift()
            self._janela_cliente.focus_force()
            return

        janela = tk.Toplevel(self._root)
        self._janela_cliente = janela
        Cliente_view(janela, self._controller_cliente)

    def _abrir_funcionario(self):
        if self._janela_funcionario is not None and self._janela_funcionario.winfo_exists():
            self._janela_funcionario.lift()
            self._janela_funcionario.focus_force()
            return

        janela = tk.Toplevel(self._root)
        self._janela_funcionario = janela
        Funcionario_View(janela, self._controller_funcionario)

    def _abrir_equipamento(self):
        if self._janela_equipamento is not None and self._janela_equipamento.winfo_exists():
            self._janela_equipamento.lift()
            self._janela_equipamento.focus_force()
            return

        janela = tk.Toplevel(self._root)
        self._janela_equipamento = janela
        Equipamento_View(janela, self._controller_equipamento, self._dao_cliente)

    def _abrir_servico(self):
        if self._janela_servico is not None and self._janela_servico.winfo_exists():
            self._janela_servico.lift()
            self._janela_servico.focus_force()
            return

        janela = tk.Toplevel(self._root)
        self._janela_servico = janela
        Servico_View(janela, self._controller_servico)

    def _abrir_peca(self):
        if self._janela_peca is not None and self._janela_peca.winfo_exists():
            self._janela_peca.lift()
            self._janela_peca.focus_force()
            return

        janela = tk.Toplevel(self._root)
        self._janela_peca = janela
        Peca_View(janela, self._controller_peca)

    def run(self):
        self._root.mainloop()


if __name__ == "__main__":
    app = ErpApplication()
    app.run()