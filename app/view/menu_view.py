import tkinter as tk
from datetime import datetime

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


class MenuPrincipal(tk.Frame):
    """
    Tela inicial do sistema: sidebar (marca + botão "Sair") e um painel com
    a grade de cartões de módulos.

    'modulos' é uma lista de tuplas (icone, titulo, descricao, comando, cor),
    onde 'comando' é a função chamada ao clicar no cartão — normalmente um
    método _abrir_x do ErpApplication, passado de fora. Essa tela não sabe
    nada sobre DAOs, controllers ou outras views; só recebe o que precisa
    mostrar e quem chamar quando o usuário clicar.
    """

    def __init__(self, master, modulos, comando_sair):
        super().__init__(master, bg=COR_FUNDO_CONTEUDO)
        self.modulos = modulos
        self.comando_sair = comando_sair

        self._criar_sidebar()
        self._criar_conteudo_principal()

        self.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------------

    def _criar_sidebar(self):
        sidebar = tk.Frame(self, bg=COR_SIDEBAR, width=260)
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
        self._criar_item_nav(rodape, "🚪", "Sair", self.comando_sair, cor_hover=COR_SAIR_HOVER)

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

    # ------------------------------------------------------------------
    # Conteúdo principal
    # ------------------------------------------------------------------

    def _criar_conteudo_principal(self):
        conteudo = tk.Frame(self, bg=COR_FUNDO_CONTEUDO)
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

        for indice, (icone, titulo, descricao, comando, cor) in enumerate(self.modulos):
            linha, coluna = divmod(indice, colunas)
            tile = self._criar_tile(grade, icone, titulo, descricao, comando, cor)
            tile.grid(row=linha, column=coluna, padx=14, pady=14, sticky="nsew")

    def _criar_tile(self, container, icone, titulo, descricao, comando, cor_destaque):
        """Cartão clicável: faixa colorida no topo, ícone simples, título e descrição."""
        tile = tk.Frame(
            container, bg=COR_CARTAO,
            highlightbackground=COR_BORDA_CARTAO, highlightthickness=1, cursor="hand2",
        )

        tk.Frame(tile, bg=cor_destaque, height=4).pack(fill="x", side="top")

        conteudo = tk.Frame(tile, bg=COR_CARTAO)
        conteudo.pack(expand=True, fill="both", padx=24, pady=20)

        rotulo_icone = tk.Label(conteudo, text=icone, bg=COR_CARTAO, font=("Segoe UI Emoji", 32))
        rotulo_icone.pack(anchor="w")

        rotulo_titulo = tk.Label(
            conteudo, text=titulo, bg=COR_CARTAO, fg=COR_TITULO, font=FONTE_TILE_TITULO
        )
        rotulo_titulo.pack(anchor="w", pady=(14, 6))

        rotulo_descricao = tk.Label(
            conteudo, text=descricao, bg=COR_CARTAO, fg=COR_SUBTITULO, font=FONTE_TILE_DESCRICAO,
            wraplength=280, justify="left",
        )
        rotulo_descricao.pack(anchor="w")

        # Clique em qualquer parte do cartão abre a tela do módulo
        for widget in (tile, conteudo, rotulo_icone, rotulo_titulo, rotulo_descricao):
            widget.bind("<Button-1>", lambda event: comando())

        return tile