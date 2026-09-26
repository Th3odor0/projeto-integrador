import tkinter as tk
from tkinter import ttk, messagebox

from app.view.estilo_view import (
    COR_FUNDO_JANELA, CORES_MODULOS,
    configurar_janela, criar_cabecalho, criar_cartao, criar_label,
    criar_botao, estilizar_entry, aplicar_tema_widgets,
)


class CrudViewBase(tk.Frame):
    """
    Esqueleto genérico para telas simples de cadastro: formulário em cima
    (Salvar/Atualizar/Deletar/Novo) e uma Treeview de registros embaixo.
    Serve para Cliente, Funcionario, Peca, Servico — qualquer tela que só
    lista/cadastra campos de texto simples.

    Não serve, sem adaptação, para Equipamento (tem combobox de Cliente) nem
    para OrdemServico (várias entidades relacionadas, abas). Essas duas
    continuam como views próprias.

    Uma view concreta só declara:
        TITULO, SUBTITULO, MODULO   -> textos e cor do cabeçalho
                                       (MODULO é a chave em CORES_MODULOS)
        CAMPOS                      -> [(chave, rótulo), ...] na ordem do
                                       formulário e das colunas da Treeview
        COLUNAS_LARGURA             -> opcional, {chave: largura_em_px}

    O controller passado precisa expor, todos no formato (sucesso: bool, resultado):
        cadastrar(**campos), atualizar(id, **campos), excluir(id), buscar_todos()
    """

    TITULO = ""
    SUBTITULO = ""
    MODULO = ""
    CAMPOS = []
    COLUNAS_LARGURA = {}

    def __init__(self, master, controller):
        super().__init__(master, bg=COR_FUNDO_JANELA)
        self.master = master
        self.controller = controller
        self.entradas = {}

        configurar_janela(self.master, self.TITULO)
        self._criar_widgets()
        self._carregar_lista()
        self.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    # Montagem da tela
    # ------------------------------------------------------------------

    def _criar_widgets(self):
        criar_cabecalho(
            self, self.TITULO, self.SUBTITULO,
            cor_destaque=CORES_MODULOS[self.MODULO],
        )

        corpo = tk.Frame(self, bg=COR_FUNDO_JANELA)
        corpo.pack(fill="both", expand=True, padx=30, pady=(0, 24))

        self._montar_formulario(corpo)
        self._montar_lista(corpo)

    def _montar_formulario(self, corpo):
        cartao_form = criar_cartao(corpo)
        cartao_form.pack(fill="x", pady=(0, 20))

        form = tk.Frame(cartao_form, bg=cartao_form["bg"])
        form.pack(fill="x", padx=24, pady=20)

        criar_label(form, "ID:").grid(row=0, column=0, sticky="w", padx=5, pady=6)
        self.entry_id = tk.Entry(form, width=40, state="readonly")
        estilizar_entry(self.entry_id)
        self.entry_id.grid(row=0, column=1, padx=5, pady=6)

        for linha, (chave, rotulo) in enumerate(self.CAMPOS, start=1):
            criar_label(form, rotulo).grid(row=linha, column=0, sticky="w", padx=5, pady=6)
            entry = tk.Entry(form, width=40)
            estilizar_entry(entry)
            entry.grid(row=linha, column=1, padx=5, pady=6)
            self.entradas[chave] = entry

        frame_botoes = tk.Frame(form, bg=form["bg"])
        frame_botoes.grid(row=len(self.CAMPOS) + 1, column=0, columnspan=2, pady=(16, 0))

        criar_botao(frame_botoes, "Salvar", self._salvar).pack(side="left", padx=5)
        criar_botao(frame_botoes, "Atualizar", self._atualizar).pack(side="left", padx=5)
        criar_botao(frame_botoes, "Deletar", self._excluir, estilo="perigo").pack(side="left", padx=5)
        criar_botao(frame_botoes, "Novo", self._limpar_campos).pack(side="left", padx=5)

    def _montar_lista(self, corpo):
        cartao_lista = criar_cartao(corpo)
        cartao_lista.pack(fill="both", expand=True)

        estilo_tabela = aplicar_tema_widgets()
        colunas = ["id"] + [chave for chave, _ in self.CAMPOS]
        self.tree = ttk.Treeview(cartao_lista, columns=colunas, show="headings", style=estilo_tabela)

        self.tree.heading("id", text="ID")
        self.tree.column("id", width=40)
        for chave, rotulo in self.CAMPOS:
            self.tree.heading(chave, text=rotulo.rstrip(":"))
            self.tree.column(chave, width=self.COLUNAS_LARGURA.get(chave, 140))

        self.tree.pack(fill="both", expand=True, side="left", padx=(16, 0), pady=16)

        scrollbar = ttk.Scrollbar(cartao_lista, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 16), pady=16)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self._selecionar)

    # ------------------------------------------------------------------
    # Dados <-> formulário
    # ------------------------------------------------------------------

    def _selecionar(self, event):
        selecionado = self.tree.focus()
        if not selecionado:
            return
        valores = self.tree.item(selecionado, "values")
        if not valores:
            return

        self._set_id(valores[0])
        for entry, valor in zip(self.entradas.values(), valores[1:]):
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    def _set_id(self, valor):
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        if valor is not None:
            self.entry_id.insert(0, str(valor))
        self.entry_id.config(state="readonly")

    def _pegar_id(self):
        id_texto = self.entry_id.get()
        if not id_texto.strip():
            messagebox.showerror("Erro", "Nenhum registro selecionado (ID vazio).")
            return None
        try:
            return int(id_texto)
        except ValueError:
            messagebox.showerror("Erro", "O campo ID deve ser um número inteiro.")
            return None

    def _coletar_campos(self):
        return {chave: entry.get() for chave, entry in self.entradas.items()}

    def _limpar_campos(self):
        self._set_id(None)
        for entry in self.entradas.values():
            entry.delete(0, tk.END)

    # ------------------------------------------------------------------
    # Ações (Salvar / Atualizar / Excluir / Listar)
    # ------------------------------------------------------------------

    def _carregar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        sucesso, resultado = self.controller.buscar_todos()
        if not sucesso:
            messagebox.showerror("Erro", resultado)
            return

        for objeto in resultado:
            valores = [objeto.id] + [getattr(objeto, chave) for chave, _ in self.CAMPOS]
            self.tree.insert("", "end", values=valores)

    def _salvar(self):
        sucesso, resultado = self.controller.cadastrar(**self._coletar_campos())
        self._tratar_resultado(sucesso, resultado, "Cadastrado com sucesso.")

    def _atualizar(self):
        id_atual = self._pegar_id()
        if id_atual is None:
            return
        sucesso, resultado = self.controller.atualizar(id_atual, **self._coletar_campos())
        self._tratar_resultado(sucesso, resultado, "Atualizado com sucesso.")

    def _excluir(self):
        id_atual = self._pegar_id()
        if id_atual is None:
            return
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esse registro?"):
            return
        sucesso, resultado = self.controller.excluir(id_atual)
        self._tratar_resultado(sucesso, resultado, "Excluído com sucesso.")

    def _tratar_resultado(self, sucesso, resultado, mensagem_padrao):
        if sucesso:
            texto = resultado if isinstance(resultado, str) else mensagem_padrao
            messagebox.showinfo("Sucesso", texto)
            self._limpar_campos()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", resultado)