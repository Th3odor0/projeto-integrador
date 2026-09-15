import tkinter as tk
from tkinter import ttk, messagebox


class Peca_View(tk.Frame):

    CAMPOS_TEXTO = [
        ("nome", "Nome:"),
        ("codigo", "Código:"),
        ("quantidade_estoque", "Quantidade em estoque:"),
        ("preco_venda", "Preço de venda (R$):"),
    ]

    def __init__(self, master, peca_controller):
        super().__init__(master)
        self.master = master
        self.controller = peca_controller

        self.id_selecionado = None  # None = modo "novo cadastro"
        self.entradas = {}          # chave -> Entry

        self.master.title("Cadastro de Peça")

        self._linha_atual = 0
        self._criar_campos_texto()
        self._criar_treeview()
        self._criar_botoes()
        self.tbl_pecas.bind("<<TreeviewSelect>>", self._selecionar_peca)

        self._atualizar_treeview()

        self.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # Construção da interface
    # ------------------------------------------------------------------

    def _adicionar_linha(self, texto_label, widget):
        tk.Label(self, text=texto_label).grid(row=self._linha_atual, column=0, sticky="w", padx=5, pady=5)
        widget.grid(row=self._linha_atual, column=1, padx=5, pady=5)
        self._linha_atual += 1
        return widget

    def _criar_campos_texto(self):
        for chave, label in self.CAMPOS_TEXTO:
            self.entradas[chave] = self._adicionar_linha(label, tk.Entry(self, width=40))

    def _criar_treeview(self):
        # coluna -> (título, largura, alinhamento)
        colunas_config = {
            "id": ("ID", 40, "center"),
            "nome": ("Nome", 160, "w"),
            "codigo": ("Código", 100, "center"),
            "quantidade_estoque": ("Qtd. estoque", 100, "center"),
            "preco_venda": ("Preço venda", 100, "center"),
        }

        self.tbl_pecas = ttk.Treeview(self, columns=tuple(colunas_config), show="headings", height=8)
        self.tbl_pecas.grid(row=self._linha_atual, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")
        self._linha_atual += 1

        for coluna, (titulo, largura, alinhamento) in colunas_config.items():
            self.tbl_pecas.heading(coluna, text=titulo)
            self.tbl_pecas.column(coluna, width=largura, anchor=alinhamento)

    def _criar_botoes(self):
        frame = tk.Frame(self)
        frame.grid(row=self._linha_atual, column=0, columnspan=2, pady=10)

        botoes = [
            ("Novo", self._novo),
            ("Salvar", self._salvar),
            ("Alterar", self._alterar),
            ("Excluir", self._excluir),
        ]
        for coluna, (texto, comando) in enumerate(botoes):
            tk.Button(frame, text=texto, width=15, command=comando).grid(row=0, column=coluna, padx=5)

    # ------------------------------------------------------------------
    # Carregamento de dados
    # ------------------------------------------------------------------

    def _atualizar_treeview(self):
        """Busca as peças no controller e repopula a Treeview."""
        self.tbl_pecas.delete(*self.tbl_pecas.get_children())

        for peca in self.controller.listar_todas():
            self.tbl_pecas.insert("", tk.END, values=(
                peca.id,
                peca.nome,
                peca.codigo,
                peca.quantidade_estoque,
                peca.preco_venda,
            ))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _exibir_mensagem(titulo, mensagem, sucesso=True):
        (messagebox.showinfo if sucesso else messagebox.showerror)(titulo, mensagem)

    # ------------------------------------------------------------------
    # Ações da Treeview
    # ------------------------------------------------------------------

    def _selecionar_peca(self, event=None):
        selecao = self.tbl_pecas.selection()
        if not selecao:
            return

        id_peca = self.tbl_pecas.item(selecao[0])["values"][0]
        try:
            peca = self.controller.buscar_por_id(id_peca)
        except ValueError as erro:
            self._exibir_mensagem("Erro", str(erro), sucesso=False)
            return

        self._preencher_campos(peca)

    def _preencher_campos(self, peca):
        self.id_selecionado = peca.id

        valores = {
            "nome": peca.nome,
            "codigo": peca.codigo,
            "quantidade_estoque": peca.quantidade_estoque,
            "preco_venda": peca.preco_venda,
        }
        for chave, valor in valores.items():
            self.entradas[chave].delete(0, tk.END)
            self.entradas[chave].insert(0, "" if valor is None else str(valor))

    def _limpar_campos(self):
        self.id_selecionado = None
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

    def _coletar_dados_formulario(self):
        nome = self.entradas["nome"].get().strip()
        if not nome:
            raise ValueError("O campo 'nome' é obrigatório.")

        try:
            quantidade_estoque = int(self.entradas["quantidade_estoque"].get())
        except ValueError:
            raise ValueError("Quantidade em estoque precisa ser um número inteiro.")

        try:
            preco_venda = float(self.entradas["preco_venda"].get())
        except ValueError:
            raise ValueError("Preço de venda precisa ser um número.")

        return {
            "nome": nome,
            "codigo": self.entradas["codigo"].get(),
            "quantidade_estoque": quantidade_estoque,
            "preco_venda": preco_venda,
        }

    # ------------------------------------------------------------------
    # Ações dos botões (CRUD)
    # ------------------------------------------------------------------

    def _executar_operacao(self, operacao, mensagem_sucesso):
        """Roda uma operação do controller tratando os erros de forma padronizada."""
        try:
            operacao()
            self._exibir_mensagem("Sucesso", mensagem_sucesso)
            self._limpar_campos()
            self._atualizar_treeview()
        except ValueError as erro:
            self._exibir_mensagem("Erro de validação", str(erro), sucesso=False)
        except Exception as erro:
            self._exibir_mensagem("Erro inesperado", f"Ocorreu um erro: {erro}", sucesso=False)

    def _novo(self):
        """Limpa o formulário para cadastrar uma nova peça."""
        self.tbl_pecas.selection_remove(self.tbl_pecas.selection())
        self._limpar_campos()

    def _salvar(self):
        self._executar_operacao(
            lambda: self.controller.cadastrar(**self._coletar_dados_formulario()),
            "Peça cadastrada com sucesso!",
        )

    def _alterar(self):
        if self.id_selecionado is None:
            self._exibir_mensagem("Aviso", "Selecione uma peça na lista para alterar.", sucesso=False)
            return

        self._executar_operacao(
            lambda: self.controller.atualizar(self.id_selecionado, **self._coletar_dados_formulario()),
            "Peça alterada com sucesso!",
        )

    def _excluir(self):
        if self.id_selecionado is None:
            self._exibir_mensagem("Aviso", "Selecione uma peça na lista para excluir.", sucesso=False)
            return

        if not messagebox.askyesno("Confirmação", "Deseja realmente excluir esta peça?"):
            return

        self._executar_operacao(
            lambda: self.controller.excluir(self.id_selecionado),
            "Peça excluída com sucesso!",
        )