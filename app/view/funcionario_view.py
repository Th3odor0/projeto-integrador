import tkinter as tk
from tkinter import ttk, messagebox


class Funcionario_View(tk.Frame):
    

    CAMPOS_TEXTO = [
        ("nome", "Nome:"),
        ("cpf", "CPF:"),
        ("cargo", "Cargo:"),
    ]

    def __init__(self, master, funcionario_controller):
        super().__init__(master)
        self.master = master
        self.controller = funcionario_controller

        self.id_selecionado = None  # None = modo "novo cadastro"
        self.entradas = {}          # chave -> Entry

        self.master.title("Cadastro de Funcionário")

        self._linha_atual = 0
        self._criar_campos_texto()
        self._criar_treeview()
        self._criar_botoes()
        self.tbl_funcionarios.bind("<<TreeviewSelect>>", self._selecionar_funcionario)

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
            "cpf": ("CPF", 120, "center"),
            "cargo": ("Cargo", 140, "w"),
        }

        self.tbl_funcionarios = ttk.Treeview(self, columns=tuple(colunas_config), show="headings", height=8)
        self.tbl_funcionarios.grid(row=self._linha_atual, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")
        self._linha_atual += 1

        for coluna, (titulo, largura, alinhamento) in colunas_config.items():
            self.tbl_funcionarios.heading(coluna, text=titulo)
            self.tbl_funcionarios.column(coluna, width=largura, anchor=alinhamento)

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
        """Busca os funcionários no controller e repopula a Treeview."""
        self.tbl_funcionarios.delete(*self.tbl_funcionarios.get_children())

        for funcionario in self.controller.listar_todos():
            self.tbl_funcionarios.insert("", tk.END, values=(
                funcionario.id,
                funcionario.nome,
                funcionario.cpf,
                funcionario.cargo,
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

    def _selecionar_funcionario(self, event=None):
        selecao = self.tbl_funcionarios.selection()
        if not selecao:
            return

        id_funcionario = self.tbl_funcionarios.item(selecao[0])["values"][0]
        funcionario = self.controller.buscar_por_id(id_funcionario)
        if funcionario is None:
            self._exibir_mensagem("Erro", "Funcionário não encontrado.", sucesso=False)
            return

        self._preencher_campos(funcionario)

    def _preencher_campos(self, funcionario):
        self.id_selecionado = funcionario.id

        valores = {
            "nome": funcionario.nome,
            "cpf": funcionario.cpf,
            "cargo": funcionario.cargo,
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

        return {chave: self.entradas[chave].get() for chave, _ in self.CAMPOS_TEXTO}

    # ------------------------------------------------------------------
    # Ações dos botões (CRUD)
    # ------------------------------------------------------------------

    def _executar_operacao(self, chamada_controller, mensagem_sucesso):
        """
        Executa uma chamada ao controller que retorna (sucesso, mensagem_ou_objeto).
        Erros de validação levantados na coleta dos dados da própria view
        (ex.: campo obrigatório vazio) também são tratados aqui.
        """
        try:
            sucesso, resultado = chamada_controller()
        except ValueError as erro:
            self._exibir_mensagem("Erro de validação", str(erro), sucesso=False)
            return
        except Exception as erro:
            self._exibir_mensagem("Erro inesperado", f"Ocorreu um erro: {erro}", sucesso=False)
            return

        if sucesso:
            self._exibir_mensagem("Sucesso", mensagem_sucesso)
            self._limpar_campos()
            self._atualizar_treeview()
        else:
            self._exibir_mensagem("Erro", resultado, sucesso=False)

    def _novo(self):
        """Limpa o formulário para cadastrar um novo funcionário."""
        self.tbl_funcionarios.selection_remove(self.tbl_funcionarios.selection())
        self._limpar_campos()

    def _salvar(self):
        self._executar_operacao(
            lambda: self.controller.cadastrar(**self._coletar_dados_formulario()),
            "Funcionário cadastrado com sucesso!",
        )

    def _alterar(self):
        if self.id_selecionado is None:
            self._exibir_mensagem("Aviso", "Selecione um funcionário na lista para alterar.", sucesso=False)
            return

        self._executar_operacao(
            lambda: self.controller.atualizar(self.id_selecionado, **self._coletar_dados_formulario()),
            "Funcionário alterado com sucesso!",
        )

    def _excluir(self):
        if self.id_selecionado is None:
            self._exibir_mensagem("Aviso", "Selecione um funcionário na lista para excluir.", sucesso=False)
            return

        if not messagebox.askyesno("Confirmação", "Deseja realmente excluir este funcionário?"):
            return

        self._executar_operacao(
            lambda: self.controller.excluir(self.id_selecionado),
            "Funcionário excluído com sucesso!",
        )