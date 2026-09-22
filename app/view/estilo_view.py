"""
Módulo de estilo compartilhado por toda a interface do sistema.

Centraliza cores, fontes e componentes visuais (cabeçalho, botão, cartão,
tema de Treeview/Combobox/Notebook) para que a tela inicial e as views de
cada módulo (Clientes, Ordens de Serviço, etc.) tenham a mesma identidade.

Uso básico numa view:

    from app.view.estilo import (
        configurar_janela, criar_cabecalho, criar_cartao, criar_label,
        criar_botao, estilizar_entry, aplicar_tema_widgets, CORES_MODULOS,
    )

    configurar_janela(master, "Clientes")
    criar_cabecalho(self, "Clientes", "Cadastro e histórico de clientes",
                     cor_destaque=CORES_MODULOS["cliente"])
    estilo_tabela = aplicar_tema_widgets()
    tabela = ttk.Treeview(container, style=estilo_tabela, columns=(...))
"""

import tkinter as tk
from tkinter import ttk

# --- Paleta corporativa (a mesma do menu principal) ---
COR_FUNDO_JANELA = "#f4f6f9"
COR_CARTAO = "#ffffff"
COR_BORDA_CARTAO = "#e3e8ee"
COR_TITULO = "#101828"
COR_SUBTITULO = "#667085"

COR_SIDEBAR = "#101a2c"
COR_ACCENT = "#c9a227"

COR_BOTAO = "#101a2c"
COR_BOTAO_HOVER = "#1c2a44"
COR_BOTAO_TEXTO = "#ffffff"

COR_PERIGO = "#c0392b"
COR_PERIGO_HOVER = "#a93226"

# Mesma cor de destaque por módulo usada nos cartões do menu principal
CORES_MODULOS = {
    "ordem_servico": "#2f6fed",
    "cliente": "#1f9d63",
    "funcionario": "#7c5cff",
    "equipamento": "#e08e2b",
    "servico": "#0f9b8e",
    "peca": "#d1495b",
}

FONTE_TITULO_JANELA = ("Segoe UI", 18, "bold")
FONTE_SUBTITULO_JANELA = ("Segoe UI", 10)
FONTE_LABEL = ("Segoe UI", 10)
FONTE_LABEL_NEGRITO = ("Segoe UI", 10, "bold")
FONTE_BOTAO = ("Segoe UI", 10, "bold")
FONTE_TABELA = ("Segoe UI", 10)
FONTE_TABELA_CABECALHO = ("Segoe UI", 10, "bold")


def configurar_janela(janela, titulo):
    """Aplica o fundo e o título padrão a uma janela (Toplevel ou Tk)."""
    janela.configure(bg=COR_FUNDO_JANELA)
    janela.title(titulo)


def criar_cabecalho(container, titulo, subtitulo=None, cor_destaque=COR_ACCENT):
    """
    Cabeçalho padrão de uma view: uma faixa colorida fina no topo (mesma
    lógica dos cartões do menu), seguida do título do módulo e, opcionalmente,
    um subtítulo explicando a tela.
    """
    tk.Frame(container, bg=cor_destaque, height=4).pack(fill="x", side="top")

    bloco = tk.Frame(container, bg=COR_FUNDO_JANELA)
    bloco.pack(fill="x", padx=30, pady=(20, 14))

    tk.Label(
        bloco, text=titulo, bg=COR_FUNDO_JANELA, fg=COR_TITULO, font=FONTE_TITULO_JANELA
    ).pack(anchor="w")

    if subtitulo:
        tk.Label(
            bloco, text=subtitulo, bg=COR_FUNDO_JANELA, fg=COR_SUBTITULO, font=FONTE_SUBTITULO_JANELA
        ).pack(anchor="w", pady=(4, 0))

    return bloco


def criar_cartao(container, **kwargs):
    """Frame branco com borda fina, usado para envolver formulários e listas."""
    return tk.Frame(
        container, bg=COR_CARTAO, highlightbackground=COR_BORDA_CARTAO,
        highlightthickness=1, **kwargs
    )


def criar_label(container, texto, negrito=False):
    """Label padrão do sistema, já com a cor certa para um fundo de cartão (branco)."""
    return tk.Label(
        container, text=texto, bg=COR_CARTAO,
        fg=COR_TITULO if negrito else COR_SUBTITULO,
        font=FONTE_LABEL_NEGRITO if negrito else FONTE_LABEL,
    )


def estilizar_entry(entry):
    """Tira o relevo 3D padrão do Tkinter e aplica uma borda fina e moderna."""
    entry.configure(
        relief="flat",
        highlightthickness=1,
        highlightbackground=COR_BORDA_CARTAO,
        highlightcolor=COR_ACCENT,
        bg="#ffffff",
        fg=COR_TITULO,
        font=FONTE_LABEL,
        disabledbackground=COR_FUNDO_JANELA,
        readonlybackground=COR_FUNDO_JANELA,
    )
    return entry


def criar_botao(container, texto, comando, estilo="primario"):
    """
    Botão flat consistente com o resto do sistema (Label clicável, sem o
    visual "quadrado" padrão do tk.Button).
    estilo: 'primario' (azul-marinho) ou 'perigo' (vermelho, para excluir).
    """
    cores = {
        "primario": (COR_BOTAO, COR_BOTAO_HOVER, COR_BOTAO_TEXTO),
        "perigo": (COR_PERIGO, COR_PERIGO_HOVER, "#ffffff"),
    }
    cor_normal, cor_hover, cor_texto = cores.get(estilo, cores["primario"])

    botao = tk.Label(
        container, text=texto, bg=cor_normal, fg=cor_texto, font=FONTE_BOTAO,
        padx=18, pady=8, cursor="hand2",
    )
    botao.bind("<Button-1>", lambda event: comando())
    botao.bind("<Enter>", lambda event: botao.configure(bg=cor_hover))
    botao.bind("<Leave>", lambda event: botao.configure(bg=cor_normal))
    return botao


def estilizar_botao_tk(botao, estilo="primario"):
    """
    Aplica a aparência flat do sistema a um tk.Button JÁ CRIADO, mantendo o
    comportamento nativo de state="disabled"/"normal". Use isto (em vez de
    criar_botao) para qualquer botão cujo estado é alternado em tempo de
    execução via botao.config(state=...) — como nas abas de Serviços
    Prestados e Peças Utilizadas da Ordem de Serviço — porque o botão flat
    (um Label clicável) não bloqueia o clique sozinho quando "desabilitado".
    """
    cores = {
        "primario": (COR_BOTAO, COR_BOTAO_HOVER, COR_BOTAO_TEXTO),
        "perigo": (COR_PERIGO, COR_PERIGO_HOVER, "#ffffff"),
    }
    cor_normal, cor_hover, cor_texto = cores.get(estilo, cores["primario"])
    botao.configure(
        bg=cor_normal, fg=cor_texto, activebackground=cor_hover, activeforeground=cor_texto,
        disabledforeground=COR_SUBTITULO, relief="flat", bd=0, font=FONTE_BOTAO,
        padx=14, pady=6, cursor="hand2",
    )
    return botao


def aplicar_tema_widgets(nome_estilo_treeview="Corporativo.Treeview"):
    """
    Configura de uma vez o tema 'clam' do ttk para Treeview, Combobox,
    Scrollbar e Notebook, deixando os widgets padrão do ttk combinando com
    o menu principal. Chame uma vez por janela (Toplevel) — é seguro chamar
    de novo em outra janela, só reaplica a mesma configuração.

    Retorna o nome do estilo de Treeview, para passar como style=... nele.
    """
    style = ttk.Style()
    style.theme_use("clam")

    # Treeview (listagens de registros)
    style.configure(
        nome_estilo_treeview,
        background=COR_CARTAO,
        fieldbackground=COR_CARTAO,
        foreground=COR_TITULO,
        rowheight=30,
        font=FONTE_TABELA,
        borderwidth=0,
    )
    style.configure(
        f"{nome_estilo_treeview}.Heading",
        background=COR_SIDEBAR,
        foreground="#ffffff",
        font=FONTE_TABELA_CABECALHO,
        borderwidth=0,
    )
    style.map(
        nome_estilo_treeview,
        background=[("selected", COR_ACCENT)],
        foreground=[("selected", COR_TITULO)],
    )

    # Combobox
    style.configure(
        "TCombobox",
        fieldbackground="#ffffff",
        background="#ffffff",
        foreground=COR_TITULO,
        arrowcolor=COR_SIDEBAR,
        bordercolor=COR_BORDA_CARTAO,
        lightcolor="#ffffff",
        darkcolor="#ffffff",
        padding=4,
    )
    style.map("TCombobox", fieldbackground=[("readonly", "#ffffff")])

    # Scrollbar
    style.configure(
        "TScrollbar",
        background=COR_FUNDO_JANELA,
        troughcolor=COR_FUNDO_JANELA,
        bordercolor=COR_FUNDO_JANELA,
        arrowcolor=COR_SUBTITULO,
    )

    # ttk.Frame genérico (usado como conteúdo das abas do Notebook)
    style.configure("TFrame", background=COR_FUNDO_JANELA)

    # Notebook (abas, usado na tela de Ordem de Serviço)
    style.configure("TNotebook", background=COR_FUNDO_JANELA, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=COR_FUNDO_JANELA,
        foreground=COR_SUBTITULO,
        font=FONTE_LABEL_NEGRITO,
        padding=(18, 10),
        borderwidth=0,
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", COR_CARTAO)],
        foreground=[("selected", COR_TITULO)],
    )

    return nome_estilo_treeview