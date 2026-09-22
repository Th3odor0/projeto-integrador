import tkinter as tk
from datetime import datetime
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

# --- Paleta corporativa: sidebar em azul-marinho + destaque dourado ---
COR_SIDEBAR = "#101a2c"
COR_SIDEBAR_HOVER = "#1c2a44"
COR_SIDEBAR_TEXTO = "#a9b3c2"
COR_SIDEBAR_TEXTO_ATIVO = "#ffffff"
COR_ACCENT = "#c9a227"

COR_FUNDO_CONTEUDO = "#f4f6f9"
COR_CARTAO = "#ffffff"
COR_BORDA_CARTAO = "#e3e8ee"
COR_TITULO = "#101828"
COR_SUBTITULO = "#667085"

COR_SAIR_HOVER = "#c0392b"

FONTE_MARCA = ("Segoe UI", 16, "bold")
FONTE_TAGLINE = ("Segoe UI", 9)
FONTE_NAV_ITEM = ("Segoe UI", 11)
FONTE_TOPBAR_TITULO = ("Segoe UI", 11, "bold")
FONTE_TOPBAR_DATA = ("Segoe UI", 10)
FONTE_BEMVINDO = ("Segoe UI", 26, "bold")
FONTE_SUBTITULO_BEMVINDO = ("Segoe UI", 11)
FONTE_TILE_TITULO = ("Segoe UI", 16, "bold")
FONTE_TILE_DESCRICAO = ("Segoe UI", 11)

# Um destaque de cor por módulo, usado na faixa superior e no emblema do cartão
MODULOS = [
    ("🧾", "Ordens de Serviço", "Abrir, acompanhar e concluir atendimentos", "_abrir_ordem_servico", "#2f6fed"),
    ("👤", "Clientes", "Cadastro e histórico de clientes", "_abrir_cliente", "#1f9d63"),
    ("👷", "Funcionários", "Equipe técnica e administrativa", "_abrir_funcionario", "#7c5cff"),
    ("💻", "Equipamentos", "Aparelhos recebidos para reparo", "_abrir_equipamento", "#e08e2b"),
    ("🔧", "Serviços", "Catálogo de serviços prestados pela oficina", "_abrir_servico", "#0f9b8e"),
    ("🔩", "Peças", "Estoque de peças utilizadas nos reparos", "_abrir_peca", "#d1495b"),
]


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
        self._root.configure(bg=COR_FUNDO_CONTEUDO)

    # ------------------------------------------------------------------
    # Tela inicial: sidebar de navegação + painel principal com módulos
    # ------------------------------------------------------------------

    def _criar_tela_inicial(self):
        container = tk.Frame(self._root, bg=COR_FUNDO_CONTEUDO)
        container.pack(fill="both", expand=True)

        self._criar_sidebar(container)
        self._criar_conteudo_principal(container)

    def _criar_sidebar(self, container):
        sidebar = tk.Frame(container, bg=COR_SIDEBAR, width=260)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Bloco de marca: emblema circular + nome + tagline
        bloco_marca = tk.Frame(sidebar, bg=COR_SIDEBAR)
        bloco_marca.pack(fill="x", padx=26, pady=(34, 26))

        emblema = tk.Canvas(bloco_marca, width=46, height=46, bg=COR_SIDEBAR, highlightthickness=0)
        emblema.create_oval(2, 2, 44, 44, fill=COR_ACCENT, outline="")
        emblema.create_text(23, 23, text="AT", fill=COR_SIDEBAR, font=("Segoe UI", 14, "bold"))
        emblema.pack(anchor="w")

        tk.Label(
            bloco_marca,
            text="Assistência Técnica",
            bg=COR_SIDEBAR,
            fg="#ffffff",
            font=FONTE_MARCA,
            wraplength=200,
            justify="left",
        ).pack(anchor="w", pady=(14, 2))

        tk.Label(
            bloco_marca,
            text="Sistema ERP Corporativo",
            bg=COR_SIDEBAR,
            fg=COR_SIDEBAR_TEXTO,
            font=FONTE_TAGLINE,
        ).pack(anchor="w")

        # A navegação principal vive nos cartões do painel; a sidebar fica só
        # com a marca e o "Sair", deixando o espaço em branco de propósito —
        # é o padrão de apps corporativos mais enxutos (Stripe, Linear, Notion).

        # "Sair" fica ancorado embaixo da sidebar, mesmo com a janela maximizada
        rodape = tk.Frame(sidebar, bg=COR_SIDEBAR)
        rodape.pack(side="bottom", fill="x", pady=(0, 26))
        tk.Frame(rodape, bg=COR_SIDEBAR_HOVER, height=1).pack(fill="x", padx=26, pady=(0, 14))
        self._criar_item_nav(rodape, "🚪", "Sair", self._root.destroy, cor_hover=COR_SAIR_HOVER)

    def _criar_item_nav(self, container, icone, titulo, comando, cor_hover=COR_SIDEBAR_HOVER):
        """Um item de navegação da sidebar: destaca com uma faixa lateral ao passar o mouse."""
        item = tk.Frame(container, bg=COR_SIDEBAR, cursor="hand2")
        item.pack(fill="x", padx=14, pady=2)

        faixa = tk.Frame(item, bg=COR_SIDEBAR, width=3)
        faixa.pack(side="left", fill="y")

        conteudo = tk.Frame(item, bg=COR_SIDEBAR)
        conteudo.pack(side="left", fill="x", expand=True, padx=(10, 0), pady=10)

        rotulo = tk.Label(
            conteudo,
            text=f"{icone}   {titulo}",
            bg=COR_SIDEBAR,
            fg=COR_SIDEBAR_TEXTO,
            font=FONTE_NAV_ITEM,
            anchor="w",
        )
        rotulo.pack(fill="x")

        widgets = (item, faixa, conteudo, rotulo)

        def ao_entrar(event=None):
            item.configure(bg=cor_hover)
            conteudo.configure(bg=cor_hover)
            rotulo.configure(bg=cor_hover, fg=COR_SIDEBAR_TEXTO_ATIVO)
            faixa.configure(bg=COR_ACCENT)

        def ao_sair(event=None):
            item.configure(bg=COR_SIDEBAR)
            conteudo.configure(bg=COR_SIDEBAR)
            rotulo.configure(bg=COR_SIDEBAR, fg=COR_SIDEBAR_TEXTO)
            faixa.configure(bg=COR_SIDEBAR)

        for widget in widgets:
            widget.bind("<Enter>", ao_entrar)
            widget.bind("<Leave>", ao_sair)
            widget.bind("<Button-1>", lambda event: comando())

    def _criar_conteudo_principal(self, container):
        conteudo = tk.Frame(container, bg=COR_FUNDO_CONTEUDO)
        conteudo.pack(side="left", fill="both", expand=True)

        self._criar_barra_superior(conteudo)

        bloco_boasvindas = tk.Frame(conteudo, bg=COR_FUNDO_CONTEUDO)
        bloco_boasvindas.pack(fill="x", padx=48, pady=(28, 6))

        tk.Label(
            bloco_boasvindas,
            text="Bem-vindo(a) 👋",
            bg=COR_FUNDO_CONTEUDO,
            fg=COR_TITULO,
            font=FONTE_BEMVINDO,
        ).pack(anchor="w")

        tk.Label(
            bloco_boasvindas,
            text="Selecione um módulo abaixo para começar o atendimento.",
            bg=COR_FUNDO_CONTEUDO,
            fg=COR_SUBTITULO,
            font=FONTE_SUBTITULO_BEMVINDO,
        ).pack(anchor="w", pady=(6, 0))

        self._criar_grade_modulos(conteudo)

    def _criar_barra_superior(self, container):
        barra = tk.Frame(
            container, bg=COR_CARTAO, height=54,
            highlightbackground=COR_BORDA_CARTAO, highlightthickness=1,
        )
        barra.pack(fill="x")
        barra.pack_propagate(False)

        tk.Label(
            barra, text="Painel Inicial", bg=COR_CARTAO, fg=COR_TITULO, font=FONTE_TOPBAR_TITULO
        ).pack(side="left", padx=30)

        tk.Label(
            barra, text=self._data_por_extenso(), bg=COR_CARTAO, fg=COR_SUBTITULO, font=FONTE_TOPBAR_DATA
        ).pack(side="right", padx=30)

    @staticmethod
    def _data_por_extenso():
        dias = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
                "sexta-feira", "sábado", "domingo"]
        meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
                 "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
        agora = datetime.now()
        dia_semana = dias[agora.weekday()].capitalize()
        return f"{dia_semana}, {agora.day} de {meses[agora.month - 1]} de {agora.year}"

    def _criar_grade_modulos(self, container):
        """
        Grade de cartões (tiles), um por módulo. Usa columnconfigure/rowconfigure
        com weight para que os cartões cresçam junto com a janela (ela abre
        'zoomed'), sem sobrar espaço vazio.
        """
        grade = tk.Frame(container, bg=COR_FUNDO_CONTEUDO)
        grade.pack(fill="both", expand=True, padx=48, pady=(24, 40))

        colunas = 3
        for coluna in range(colunas):
            grade.columnconfigure(coluna, weight=1, uniform="col")
        for linha in range(2):
            grade.rowconfigure(linha, weight=1, uniform="row")

        for indice, (icone, titulo, descricao, nome_metodo, cor) in enumerate(MODULOS):
            comando = getattr(self, nome_metodo)
            linha, coluna = divmod(indice, colunas)
            tile = self._criar_tile(grade, icone, titulo, descricao, comando, cor)
            tile.grid(row=linha, column=coluna, padx=14, pady=14, sticky="nsew")

    def _criar_tile(self, container, icone, titulo, descricao, comando, cor_destaque):
        """Cartão clicável: faixa colorida no topo, emblema circular e destaque ao passar o mouse."""
        tile = tk.Frame(
            container, bg=COR_CARTAO,
            highlightbackground=COR_BORDA_CARTAO, highlightthickness=1, cursor="hand2",
        )

        tk.Frame(tile, bg=cor_destaque, height=4).pack(fill="x", side="top")

        conteudo = tk.Frame(tile, bg=COR_CARTAO)
        conteudo.pack(expand=True, fill="both", padx=24, pady=20)

        emblema = tk.Canvas(conteudo, width=68, height=68, bg=COR_CARTAO, highlightthickness=0)
        emblema.create_oval(2, 2, 66, 66, fill=self._clarear_cor(cor_destaque), outline="")
        self._desenhar_icone_centralizado(emblema, icone, centro=34, tamanho_fonte=30)
        emblema.pack(anchor="w")

        rotulo_titulo = tk.Label(
            conteudo, text=titulo, bg=COR_CARTAO, fg=COR_TITULO, font=FONTE_TILE_TITULO
        )
        rotulo_titulo.pack(anchor="w", pady=(18, 6))

        rotulo_descricao = tk.Label(
            conteudo, text=descricao, bg=COR_CARTAO, fg=COR_SUBTITULO, font=FONTE_TILE_DESCRICAO,
            wraplength=280, justify="left",
        )
        rotulo_descricao.pack(anchor="w")

        widgets = (tile, conteudo, emblema, rotulo_titulo, rotulo_descricao)

        def ao_entrar(event=None):
            tile.configure(highlightbackground=cor_destaque, highlightthickness=2)

        def ao_sair(event=None):
            tile.configure(highlightbackground=COR_BORDA_CARTAO, highlightthickness=1)

        for widget in widgets:
            widget.bind("<Enter>", ao_entrar)
            widget.bind("<Leave>", ao_sair)
            widget.bind("<Button-1>", lambda event: comando())

        return tile

    @staticmethod
    def _desenhar_icone_centralizado(canvas, texto, centro, tamanho_fonte):
        """
        Desenha 'texto' (geralmente um emoji) num Canvas e o recentraliza usando
        a caixa delimitadora real do que foi desenhado. Necessário porque emojis
        têm espaçamento interno irregular na fonte, então o anchor="center" do
        Tkinter sozinho não deixa o ícone visualmente no meio do círculo.
        """
        item = canvas.create_text(
            centro, centro, text=texto, font=("Segoe UI Emoji", tamanho_fonte), anchor="center"
        )
        caixa = canvas.bbox(item)
        if caixa:
            x0, y0, x1, y1 = caixa
            canvas.move(item, centro - (x0 + x1) / 2, centro - (y0 + y1) / 2)
        return item

    @staticmethod
    def _clarear_cor(cor_hex, fator=0.82):
        """Gera uma versão bem clara (pastel) de uma cor hex, para o fundo do emblema."""
        cor_hex = cor_hex.lstrip("#")
        r, g, b = int(cor_hex[0:2], 16), int(cor_hex[2:4], 16), int(cor_hex[4:6], 16)
        r = int(r + (255 - r) * fator)
        g = int(g + (255 - g) * fator)
        b = int(b + (255 - b) * fator)
        return f"#{r:02x}{g:02x}{b:02x}"

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