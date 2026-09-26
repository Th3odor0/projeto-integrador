import tkinter as tk
from app.core.database import Database

# DAOs das entidades necessárias para Ordem de Serviço
from app.dao.cliente_dao import Cliente_DAO
from app.dao.funcionario_dao import Funcionario_DAO
from app.dao.equipamento_dao import EquipamentoDAO
from app.dao.ordem_servico_dao import Ordem_servico_DAO
from app.dao.ordem_servico_pecas_dao import Ordem_Servico_Peca_DAO
from app.dao.peca_dao import PecaDAO
from app.dao.servico_dao import ServicoDAO
from app.dao.ordem_servico_servico_dao import Ordem_servico_Servico_Dao
# Controller
from app.controller.ordem_servico_controller import Ordem_servico_Controller
from app.controller.cliente_controller import ClienteController
from app.controller.funcionario_controller import FuncionarioController
from app.controller.peca_controller import PecaController
from app.controller.servico_controller import ServicoController
from app.controller.equipamento_controller import EquipamentoController
from app.controller.ordem_servico_servico_controller import Ordem_servico_Servico_Controller
# Ajuste este caminho para onde você salvou o Ordem_Servico_Peca_Controller
from app.controller.ordem_servico_pecas_controller import Ordem_Servico_Peca_Controller
# View
from app.view.menu_view import MenuPrincipal
from app.view.ordem_servico_view import Ordem_servico_View
from app.view.cliente_view import Cliente_View
from app.view.equipamento_view import Equipamento_View
from app.view.funcionario_view import Funcionario_View
from app.view.servico_view import Servico_View
from app.view.peca_view import Peca_View
# Ordem_servico_Servico_View e Ordem_Servico_Peca_View são abertas de dentro
# da própria Ordem_servico_View (botões "Serviços desta Ordem" / "Peças desta
# Ordem"), então não precisam ser importadas nem abertas aqui.

COR_FUNDO_JANELA = "#f4f6f9"


class ErpApplication:
    """
    Raiz da aplicação: conecta no banco, monta os DAOs e Controllers de cada
    módulo, mostra o menu principal (MenuPrincipal, em app/view/menu_view.py)
    e abre a janela de cada módulo quando o usuário clica no cartão dele.
    """

    def __init__(self):
        self._database = Database()
        self._root = tk.Tk()

        self._janela_ordem_servico = None
        self._janela_cliente = None
        self._janela_funcionario = None
        self._janela_equipamento = None
        self._janela_servico = None
        self._janela_peca = None

        self._configurar_janela()
        self._montar_daos_e_controllers()
        self._criar_menu_principal()

    def _configurar_janela(self):
        self._root.title("Sistema ERP - Assistência Técnica")
        self._root.state("zoomed")
        self._root.configure(bg=COR_FUNDO_JANELA)

    def _montar_daos_e_controllers(self):
        # DAOs independentes
        self._dao_cliente = Cliente_DAO(self._database)
        self._dao_funcionario = Funcionario_DAO(self._database)
        self._dao_equipamento = EquipamentoDAO(self._database, self._dao_cliente)
        self._dao_peca = PecaDAO(self._database)
        self._dao_servico = ServicoDAO(self._database)
        self._dao_servico_servico = Ordem_servico_Servico_Dao(self._database)
        self._dao_ordem_servico_peca = Ordem_Servico_Peca_DAO(self._database)

        # DAO principal, que depende dos DAOs acima
        self._dao_ordem_servico = Ordem_servico_DAO(
            self._database, self._dao_cliente, self._dao_funcionario, self._dao_equipamento
        )

        # Controllers
        self._controller_ordem_servico = Ordem_servico_Controller(
            self._dao_ordem_servico, self._dao_cliente, self._dao_funcionario, self._dao_equipamento
        )
        self._controller_cliente = ClienteController(self._dao_cliente)
        self._controller_funcionario = FuncionarioController(self._dao_funcionario)
        self._controller_peca = PecaController(self._dao_peca)
        self._controller_servico = ServicoController(self._dao_servico)
        self._controller_equipamento = EquipamentoController(self._dao_equipamento, self._dao_cliente)
        self._controller_servico_servico = Ordem_servico_Servico_Controller(
            self._dao_servico_servico, self._dao_servico, self._dao_ordem_servico
        )
        self._controller_ordem_servico_peca = Ordem_Servico_Peca_Controller(
            self._dao_ordem_servico_peca, self._dao_peca, self._dao_ordem_servico
        )

    # ------------------------------------------------------------------
    # Menu principal
    # ------------------------------------------------------------------

    def _criar_menu_principal(self):
        modulos = [
            ("🧾", "Ordens de Serviço", "Abrir, acompanhar e concluir atendimentos",
             self._abrir_ordem_servico, "#2f6fed"),
            ("👤", "Clientes", "Cadastro e histórico de clientes",
             self._abrir_cliente, "#1f9d63"),
            ("👷", "Funcionários", "Equipe técnica e administrativa",
             self._abrir_funcionario, "#7c5cff"),
            ("💻", "Equipamentos", "Aparelhos recebidos para reparo",
             self._abrir_equipamento, "#e08e2b"),
            ("🔧", "Serviços", "Catálogo de serviços prestados pela oficina",
             self._abrir_servico, "#0f9b8e"),
            ("🔩", "Peças", "Estoque de peças utilizadas nos reparos",
             self._abrir_peca, "#d1495b"),
        ]
        MenuPrincipal(self._root, modulos, self._root.destroy)

    # ------------------------------------------------------------------
    # Abertura das telas (janelas Toplevel)
    # ------------------------------------------------------------------

    def _abrir_ordem_servico(self):
        # Evita duplicar a abertura da mesma janela no Tkinter
        if self._janela_ordem_servico is not None and self._janela_ordem_servico.winfo_exists():
            self._janela_ordem_servico.lift()
            self._janela_ordem_servico.focus_force()
            return

        janela = tk.Toplevel(self._root)
        self._janela_ordem_servico = janela
        Ordem_servico_View(
            janela,
            self._controller_ordem_servico,
            self._dao_cliente,
            self._dao_funcionario,
            self._dao_equipamento,
            self._controller_servico_servico,
            self._dao_servico,
            self._controller_ordem_servico_peca,
            self._dao_peca,
        )

    def _abrir_cliente(self):
        if self._janela_cliente is not None and self._janela_cliente.winfo_exists():
            self._janela_cliente.lift()
            self._janela_cliente.focus_force()
            return

        janela = tk.Toplevel(self._root)
        self._janela_cliente = janela
        Cliente_View(janela, self._controller_cliente)

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