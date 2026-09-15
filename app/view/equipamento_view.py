import tkinter as tk
from tkinter import ttk, messagebox


class Equipamento_View(tk.Frame):

    CAMPOS_TEXTO = [
        ("tipo", "Tipo:"),
        ("marca", "Marca:"),
        ("modelo", "Modelo:"),
        ("numero_serie", "Número de série:"),
    ]

    def __init__(self, master, equipamento_controller, cliente_dao):
        super().__init__(master)
        self.master = master
        self.controller = equipamento_controller
        self.cliente_dao = cliente_dao

        self.id_selecionado = None  # None = modo "novo cadastro"
        self.entradas = {}          # chave -> Entry

        self.master.title("Cadastro de Equipamento")

        self._linha_atual = 0
        self._criar_combo_cliente()
        self._criar_campos_texto()
        self._criar_treeview()
        self._criar_botoes()
        self.tbl_equipamentos.bind("<<TreeviewSelect>>", self._selecionar_equipamento)

        self._carregar_combo_cliente()
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

    def _criar_combo_cliente(self):
        self.combo_cliente = self._adicionar_linha(
            "Cliente:", ttk.Combobox(self, state="readonly", width=38)
        )

    def _criar_campos_texto(self):
        for chave, label in self.CAMPOS_TEXTO:
            self.entradas[chave] = self._adicionar_linha(label, tk.Entry(self, width=40))

    def _criar_treeview(self):
        # coluna -> (título, largura, alinhamento)
        colunas_config = {
            "id": ("ID", 40, "center"),
            "tipo": ("Tipo", 100, "w"),
            "marca": ("Marca", 100, "w"),
            "modelo": ("Modelo", 100, "w"),
            "numero_serie": ("Nº série", 100, "center"),
            "cliente": ("Cliente", 140, "w"),
        }

        self.tbl_equipamentos = ttk.Treeview(self, columns=tuple(colunas_config), show="headings", height=8)
        self.tbl_equipamentos.grid(row=self._linha_atual, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")
        self._linha_atual += 1

        for coluna, (titulo, largura, alinhamento) in colunas_config.items():
            self.tbl_equipamentos.heading(coluna, text=titulo)
            self.tbl_equipamentos.column(coluna, width=largura, anchor=alinhamento)

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

    def _carregar_combo_cliente(self):
        """Popula o combobox de clientes com dados vindos do banco via DAO."""
        self.combo_cliente["values"] = [f"{c.id} - {c.nome}" for c in self.cliente_dao.get_all()]

    def _atualizar_treeview(self):
        """Busca os equipamentos no controller e repopula a Treeview."""
        self.tbl_equipamentos.delete(*self.tbl_equipamentos.get_children())

        for equipamento in self.controller.listar_todas():
            self.tbl_equipamentos.insert("", tk.END, values=(
                equipamento.id,
                equipamento.tipo,
                equipamento.marca,
                equipamento.modelo,
                equipamento.numero_serie,
                self._nome_cliente(equipamento),
            ))

    @staticmethod
    def _nome_cliente(equipamento):
        """equipamento.id_cliente pode vir como objeto Cliente ou como int puro."""
        cliente = equipamento.id_cliente
        return getattr(cliente, "nome", cliente)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extrair_id_do_combo(texto_combo):
        """Extrai o id numérico do texto '3 - Nome do Cliente' -> 3"""
        return int(texto_combo.split(" - ")[0]) if texto_combo else None

    @staticmethod
    def _selecionar_valor_combo(combobox, id_procurado):
        """Seleciona no combobox o item cujo texto começa com 'id_procurado - '."""
        valor = next((v for v in combobox["values"] if v.split(" - ")[0] == str(id_procurado)), "")
        combobox.set(valor)

    @staticmethod
    def _exibir_mensagem(titulo, mensagem, sucesso=True):
        (messagebox.showinfo if sucesso else messagebox.showerror)(titulo, mensagem)

    # ------------------------------------------------------------------
    # Ações da Treeview
    # ------------------------------------------------------------------

    def _selecionar_equipamento(self, event=None):
        selecao = self.tbl_equipamentos.selection()
        if not selecao:
            return

        id_equipamento = self.tbl_equipamentos.item(selecao[0])["values"][0]
        try:
            equipamento = self.controller.buscar_por_id(id_equipamento)
        except ValueError as erro:
            self._exibir_mensagem("Erro", str(erro), sucesso=False)
            return

        self._preencher_campos(equipamento)

    def _preencher_campos(self, equipamento):
        self.id_selecionado = equipamento.id

        id_cliente = getattr(equipamento.id_cliente, "id", equipamento.id_cliente)
        self._selecionar_valor_combo(self.combo_cliente, id_cliente)

        valores = {
            "tipo": equipamento.tipo,
            "marca": equipamento.marca,
            "modelo": equipamento.modelo,
            "numero_serie": equipamento.numero_serie,
        }
        for chave, valor in valores.items():
            self.entradas[chave].delete(0, tk.END)
            self.entradas[chave].insert(0, "" if valor is None else str(valor))

    def _limpar_campos(self):
        self.id_selecionado = None
        self.combo_cliente.set("")
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

    def _coletar_dados_formulario(self):
        id_cliente = self._extrair_id_do_combo(self.combo_cliente.get())
        if id_cliente is None:
            raise ValueError("Selecione um cliente.")

        dados = {chave: self.entradas[chave].get() for chave, _ in self.CAMPOS_TEXTO}
        dados["id_cliente"] = id_cliente
        return dados

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
        """Limpa o formulário para cadastrar um novo equipamento."""
        self.tbl_equipamentos.selection_remove(self.tbl_equipamentos.selection())
        self._limpar_campos()

    def _salvar(self):
        self._executar_operacao(
            lambda: self.controller.cadastrar(**self._coletar_dados_formulario()),
            "Equipamento cadastrado com sucesso!",
        )

    def _alterar(self):
        if self.id_selecionado is None:
            self._exibir_mensagem("Aviso", "Selecione um equipamento na lista para alterar.", sucesso=False)
            return

        self._executar_operacao(
            lambda: self.controller.atualizar(self.id_selecionado, **self._coletar_dados_formulario()),
            "Equipamento alterado com sucesso!",
        )

    def _excluir(self):
        if self.id_selecionado is None:
            self._exibir_mensagem("Aviso", "Selecione um equipamento na lista para excluir.", sucesso=False)
            return

        if not messagebox.askyesno("Confirmação", "Deseja realmente excluir este equipamento?"):
            return

        self._executar_operacao(
            lambda: self.controller.excluir(self.id_selecionado),
            "Equipamento excluído com sucesso!",
        )