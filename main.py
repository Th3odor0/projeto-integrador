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
from app.view.ordem_servico_view import Ordem_servico_View
from app.view.cliente_view import Cliente_view
from app.view.equipamento_view import Equipamento_View
from app.view.funcionario_view import Funcionario_View
from app.view.servico_view import Servico_View
from app.view.peca_view import Peca_View
# Ordem_servico_Servico_View não é mais aberta como janela própria — ela virou
# a aba "Serviços Prestados" embutida na Ordem_servico_View. O import dela e
# de Ordem_servico_Peca_View não são mais necessários aqui.

# --- Paleta e fontes da tela inicial ---
COR_FUNDO_JANELA = "#eef2f5"
COR_CARTAO = "#ffffff"
COR_BORDA_CARTAO = "#dfe6e9"
COR_TITULO = "#1a252f"
COR_SUBTITULO = "#7f8c8d"

COR_BOTAO = "#2c3e50"
COR_BOTAO_HOVER = "#3d566e"
COR_BOTAO_TEXTO = "#ecf0f1"

COR_SAIR = "#95a5a6"
COR_SAIR_HOVER = "#c0392b"

FONTE_TITULO = ("Segoe UI", 26, "bold")
FONTE_SUBTITULO = ("Segoe UI", 11)
FONTE_BOTAO = ("Segoe UI", 12, "bold")
FONTE_MENU_ITEM = ("Segoe UI", 10)
FONTE_SAIR = ("Segoe UI", 10)


class ErpApplication:

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

        # DAOs indenpendentes
        self._dao_cliente = Cliente_DAO(self._database)
        self._dao_funcionario = Funcionario_DAO(self._database)
        self._dao_equipamento = EquipamentoDAO(self._database, self._dao_cliente)
        self._dao_peca = PecaDAO(self._database)
        self._dao_servico = ServicoDAO(self._database)

        # Ordem_servico_Servico_Dao recebe uma conexão já aberta (não o Database
        # inteiro) — é um padrão proposital e diferente do resto das DAOs.
        conexao_os_servico = self._database.conectar()
        self._dao_servico_servico = Ordem_servico_Servico_Dao(conexao_os_servico)

        # Ordem_Servico_Peca_DAO segue o padrão normal, recebendo 'database'.
        self._dao_ordem_servico_peca = Ordem_Servico_Peca_DAO(self._database)

        # 2. Injeta as dependências na DAO principal
        self._dao_ordem_servico = Ordem_servico_DAO(
            self._database,
            self._dao_cliente,
            self._dao_funcionario,
            self._dao_equipamento
        )

        # 3. Controller usa a DAO principal + as DAOs auxiliares
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
            self._dao_servico_servico, self._dao_servico, self._dao_ordem_servico
        )
        self._controller_ordem_servico_peca = Ordem_Servico_Peca_Controller(
            self._dao_ordem_servico_peca, self._dao_peca, self._dao_ordem_servico
        )
        self._criar_tela_inicial()

    def _configurar_janela(self):
        self._root.title("Sistema ERP - Assistência Técnica")
        self._root.state("zoomed")
        self._root.configure(bg=COR_FUNDO_JANELA)

    # ------------------------------------------------------------------
    # Tela inicial: cartão centralizado com título, subtítulo e menu
    # ------------------------------------------------------------------

    def _criar_tela_inicial(self):
        fundo = tk.Frame(self._root, bg=COR_FUNDO_JANELA)
        fundo.pack(fill="both", expand=True)

        # "Sair" discreto, no canto superior direito — não compete com o
        # cartão central, que é o foco principal da tela
        botao_sair = tk.Label(
            fundo,
            text="Sair  ✕",
            bg=COR_FUNDO_JANELA,
            fg=COR_SAIR,
            font=FONTE_SAIR,
            cursor="hand2",
        )
        botao_sair.place(relx=1.0, x=-24, y=20, anchor="ne")
        botao_sair.bind("<Button-1>", lambda e: self._root.destroy())
        botao_sair.bind("<Enter>", lambda e: botao_sair.config(fg=COR_SAIR_HOVER))
        botao_sair.bind("<Leave>", lambda e: botao_sair.config(fg=COR_SAIR))

        # Cartão central: fica no meio da janela independente do tamanho dela,
        # porque relx/rely são recalculados quando a janela é redimensionada
        cartao = tk.Frame(
            fundo,
            bg=COR_CARTAO,
            padx=70,
            pady=50,
            highlightbackground=COR_BORDA_CARTAO,
            highlightthickness=1,
        )
        cartao.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(cartao, text="🛠️", bg=COR_CARTAO, font=("Segoe UI Emoji", 42)).pack(pady=(0, 12))

        tk.Label(
            cartao,
            text="Assistência Técnica",
            bg=COR_CARTAO,
            fg=COR_TITULO,
            font=FONTE_TITULO,
        ).pack()

        tk.Label(
            cartao,
            text="Sistema de Gestão de Ordens de Serviço",
            bg=COR_CARTAO,
            fg=COR_SUBTITULO,
            font=FONTE_SUBTITULO,
        ).pack(pady=(4, 32))

        self._criar_botao_atendimento(cartao)

    def _criar_botao_atendimento(self, container):
        """
        Botão central que abre o menu suspenso de Atendimento.
        Usa Label + tk_popup() manual (não Menubutton) pelo mesmo motivo de
        antes: o clique automático do Menubutton restilizado é pouco confiável.
        """
        menu_suspenso = tk.Menu(
            self._root,
            tearoff=0,
            bg=COR_BOTAO,
            fg=COR_BOTAO_TEXTO,
            activebackground=COR_BOTAO_HOVER,
            activeforeground="white",
            font=FONTE_MENU_ITEM,
            bd=0,
            relief="flat",
        )
        itens = [
            ("🧾  Ordens de Serviço", self._abrir_ordem_servico),
            ("👤  Clientes", self._abrir_cliente),
            ("🧑‍🔧  Funcionários", self._abrir_funcionario),
            ("🖥️  Equipamentos", self._abrir_equipamento),
            ("🛠️  Serviços", self._abrir_servico),
            ("🔩  Peças", self._abrir_peca),
        ]
        for label, comando in itens:
            menu_suspenso.add_command(label=label, command=comando)

        botao = tk.Label(
            container,
            text="  ☰   Atendimento   ",
            bg=COR_BOTAO,
            fg=COR_BOTAO_TEXTO,
            font=FONTE_BOTAO,
            cursor="hand2",
            padx=10,
            pady=12,
        )
        botao.pack()

        def abrir_menu(event=None):
            x = botao.winfo_rootx()
            y = botao.winfo_rooty() + botao.winfo_height()
            menu_suspenso.tk_popup(x, y)

        botao.bind("<Button-1>", abrir_menu)
        botao.bind("<Enter>", lambda e: botao.config(bg=COR_BOTAO_HOVER))
        botao.bind("<Leave>", lambda e: botao.config(bg=COR_BOTAO))

        return botao

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
        # Evita duplicar a abertura da mesma janela no Tkinter
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