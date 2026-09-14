import tkinter as tk
from tkinter import ttk, messagebox


class Ordem_servico_View(tk.Frame):
   
    STATUS_OPCOES = ["aberta", "em andamento", "concluida", "cancelada"]

    # (chave usada internamente == nome do kwarg passado ao controller, label exibido)
    CAMPOS_TEXTO = [
        ("data_entrada_texto", "Data de entrada (dd/mm/aaaa):"),
        ("data_conclusao_texto", "Data de conclusão (opcional):"),
        ("problema", "Problema:"),
        ("diagnostico", "Diagnóstico:"),
        ("valor_total", "Valor total (R$):"),
        ("forma_pagamento", "Forma de pagamento:"),
        ("dias_garantia", "Dias de garantia:"),
    ]

    # Campos que o controller aceita alterar numa ordem já existente
    # (tudo em CAMPOS_TEXTO exceto data_entrada_texto, que é imutável)
    CAMPOS_ATUALIZAVEIS = [chave for chave, _ in CAMPOS_TEXTO if chave != "data_entrada_texto"]

    # Campos travados durante a edição, porque o controller não permite mudá-los
    CAMPOS_IMUTAVEIS_NA_EDICAO = ["cliente", "funcionario", "equipamento"]

    def __init__(self, master, ordem_servico_controller, cliente_dao, funcionario_dao, equipamento_dao):
        super().__init__(master)
        self.master = master
        self.controller = ordem_servico_controller
        self.cliente_dao = cliente_dao
        self.funcionario_dao = funcionario_dao
        self.equipamento_dao = equipamento_dao

        self.id_selecionado = None  # None = modo "novo cadastro"
        self.combos = {}            # chave -> Combobox
        self.entradas = {}          # chave -> Entry

        self.master.title("Cadastro de Ordem de Serviço")

        self._linha_atual = 0
        self._criar_combos()
        self._criar_campos_texto()
        self._criar_treeview()
        self._criar_botoes()
        self.tbl_ordens.bind("<<TreeviewSelect>>", self._selecionar_ordem)

        self._carregar_combos()
        self._atualizar_treeview()

        # Sem isso, o Frame nunca aparece dentro do Toplevel (janela fica em branco)
        self.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # Construção da interface
    # ------------------------------------------------------------------

    def _adicionar_linha(self, texto_label, widget):
        tk.Label(self, text=texto_label).grid(row=self._linha_atual, column=0, sticky="w", padx=5, pady=5)
        widget.grid(row=self._linha_atual, column=1, padx=5, pady=5)
        self._linha_atual += 1
        return widget

    def _criar_combos(self):
        self.combos["cliente"] = self._adicionar_linha(
            "Cliente:", ttk.Combobox(self, state="readonly", width=40)
        )
        self.combos["funcionario"] = self._adicionar_linha(
            "Funcionário:", ttk.Combobox(self, state="readonly", width=40)
        )
        self.combos["equipamento"] = self._adicionar_linha(
            "Equipamento:", ttk.Combobox(self, state="readonly", width=40)
        )

    def _criar_campos_texto(self):
        for chave, label in self.CAMPOS_TEXTO:
            self.entradas[chave] = self._adicionar_linha(label, tk.Entry(self, width=42))
            if chave == "data_conclusao_texto":
                # Status entra logo depois da data de conclusão, como no layout original
                self.combos["status"] = self._adicionar_linha(
                    "Status:", ttk.Combobox(self, state="readonly", width=40, values=self.STATUS_OPCOES)
                )
                self.combos["status"].current(0)

    def _criar_treeview(self):
        # coluna -> (título, largura, alinhamento)
        colunas_config = {
            "id": ("ID", 40, "center"),
            "cliente": ("Cliente", 140, "w"),
            "equipamento": ("Equipamento", 140, "w"),
            "status": ("Status", 100, "center"),
            "data_entrada": ("Entrada", 90, "center"),
        }

        self.tbl_ordens = ttk.Treeview(self, columns=tuple(colunas_config), show="headings", height=8)
        self.tbl_ordens.grid(row=self._linha_atual, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")
        self._linha_atual += 1

        for coluna, (titulo, largura, alinhamento) in colunas_config.items():
            self.tbl_ordens.heading(coluna, text=titulo)
            self.tbl_ordens.column(coluna, width=largura, anchor=alinhamento)

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

    def _carregar_combos(self):
        """Popula os comboboxes com dados vindos do banco via DAO."""
        self.combos["cliente"]["values"] = [f"{c.id} - {c.nome}" for c in self.cliente_dao.get_all()]
        self.combos["funcionario"]["values"] = [f"{f.id} - {f.nome}" for f in self.funcionario_dao.get_all()]
        self.combos["equipamento"]["values"] = [
            f"{e.id} - {e.tipo} {e.marca} {e.modelo}" for e in self.equipamento_dao.get_all()
        ]

    def _atualizar_treeview(self):
        """Busca as ordens no controller e repopula a Treeview."""
        self.tbl_ordens.delete(*self.tbl_ordens.get_children())

        for ordem in self.controller.listar_todas():
            self.tbl_ordens.insert("", tk.END, values=(
                ordem.id,
                ordem.cliente.nome,
                f"{ordem.equipamento.tipo} {ordem.equipamento.marca} {ordem.equipamento.modelo}",
                ordem.status,
                ordem.data_entrada,
            ))

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

    def _selecionar_ordem(self, event=None):
        selecao = self.tbl_ordens.selection()
        if not selecao:
            return

        id_ordem = self.tbl_ordens.item(selecao[0])["values"][0]
        try:
            ordem = self.controller.buscar_por_id(id_ordem)
        except ValueError as erro:
            self._exibir_mensagem("Erro", str(erro), sucesso=False)
            return

        self._preencher_campos(ordem)

    def _preencher_campos(self, ordem):
        self.id_selecionado = ordem.id

        self._selecionar_valor_combo(self.combos["cliente"], ordem.cliente.id)
        self._selecionar_valor_combo(self.combos["funcionario"], ordem.funcionario.id)
        self._selecionar_valor_combo(self.combos["equipamento"], ordem.equipamento.id)
        self.combos["status"].set(ordem.status)

        valores = {
            "data_entrada_texto": ordem.data_entrada,
            "data_conclusao_texto": ordem.data_conclusao,
            "problema": ordem.problema,
            "diagnostico": ordem.diagnostico,
            "valor_total": ordem.valor_total,
            "forma_pagamento": ordem.forma_pagamento,
            "dias_garantia": ordem.dias_garantia,
        }
        for chave, valor in valores.items():
            self.entradas[chave].delete(0, tk.END)
            self.entradas[chave].insert(0, "" if valor is None else str(valor))

        # cliente/funcionário/equipamento/data de entrada não são editáveis
        # numa ordem já existente (o controller.atualizar não aceita esses campos)
        self._travar_campos_imutaveis(True)

    def _travar_campos_imutaveis(self, travar):
        estado_combo = "disabled" if travar else "readonly"
        for chave in self.CAMPOS_IMUTAVEIS_NA_EDICAO:
            self.combos[chave].config(state=estado_combo)

        estado_entrada = "disabled" if travar else "normal"
        self.entradas["data_entrada_texto"].config(state=estado_entrada)

    def _limpar_campos(self):
        self.id_selecionado = None
        self._travar_campos_imutaveis(False)

        for combo in self.combos.values():
            combo.set("")
        self.combos["status"].current(0)

        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

    def _coletar_dados_cadastro(self):
        """Dados para controller.cadastrar — inclui cliente/funcionário/equipamento/data de entrada."""
        id_cliente = self._extrair_id_do_combo(self.combos["cliente"].get())
        id_funcionario = self._extrair_id_do_combo(self.combos["funcionario"].get())
        id_equipamento = self._extrair_id_do_combo(self.combos["equipamento"].get())

        if id_cliente is None or id_funcionario is None or id_equipamento is None:
            raise ValueError("Selecione cliente, funcionário e equipamento.")

        dados = {chave: self.entradas[chave].get() for chave, _ in self.CAMPOS_TEXTO}
        dados.update(
            id_cliente=id_cliente,
            id_funcionario=id_funcionario,
            id_equipamento=id_equipamento,
            status=self.combos["status"].get(),
        )
        return dados

    def _coletar_dados_atualizacao(self):
        """Dados para controller.atualizar — sem cliente/funcionário/equipamento/data de entrada,
        porque o controller não aceita alterar esses campos numa ordem já existente."""
        dados = {chave: self.entradas[chave].get() for chave in self.CAMPOS_ATUALIZAVEIS}
        dados["status"] = self.combos["status"].get()
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
        """Limpa o formulário para cadastrar uma nova ordem."""
        self.tbl_ordens.selection_remove(self.tbl_ordens.selection())
        self._limpar_campos()

    def _salvar(self):
        self._executar_operacao(
            lambda: self.controller.cadastrar(**self._coletar_dados_cadastro()),
            "Ordem de serviço cadastrada com sucesso!",
        )

    def _alterar(self):
        if self.id_selecionado is None:
            self._exibir_mensagem("Aviso", "Selecione uma ordem na lista para alterar.", sucesso=False)
            return

        self._executar_operacao(
            lambda: self.controller.atualizar(self.id_selecionado, **self._coletar_dados_atualizacao()),
            "Ordem de serviço alterada com sucesso!",
        )

    def _excluir(self):
        if self.id_selecionado is None:
            self._exibir_mensagem("Aviso", "Selecione uma ordem na lista para excluir.", sucesso=False)
            return

        if not messagebox.askyesno("Confirmação", "Deseja realmente excluir esta ordem de serviço?"):
            return

        self._executar_operacao(
            lambda: self.controller.excluir(self.id_selecionado),
            "Ordem de serviço excluída com sucesso!",
        )