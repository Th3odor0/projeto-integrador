import tkinter as tk
from tkinter import ttk, messagebox

from app.core.dataUltils import DataUtils


class Ordem_servico_View(tk.Frame):
    """
    Tela de Ordem de Serviço com abas: Dados da Ordem, Serviços Prestados
    e Peças Utilizadas — tudo embutido na mesma janela, em vez de telas
    separadas abertas pelo menu principal.

    Alinhado com Ordem_servico_Controller (aba "Dados da Ordem"):
        - listar_todas() -> list de Ordem_servico, cada uma com .cliente/.funcionario/
              .equipamento (objetos, não ids) e os demais campos escalares.
        - buscar_por_id(id) -> Ordem_servico, ou lança ValueError se não existir.
        - cadastrar(id_cliente, id_funcionario, id_equipamento, data_entrada_texto,
              data_conclusao_texto, status, problema, diagnostico, valor_total,
              forma_pagamento, dias_garantia)
        - atualizar(id, status, data_conclusao_texto, problema, diagnostico,
              valor_total, forma_pagamento, dias_garantia)
        - excluir(id)

    Alinhado com Ordem_servico_Servico_Controller (aba "Serviços Prestados"):
        - buscar_por_ordem(ordem_servico_id) -> (sucesso, itens_ou_mensagem)
        - cadastrar(ordem_servico_id, servico_id, valor_cobrado) -> (sucesso, item_ou_mensagem)
        - atualizar(id, valor_cobrado) -> (sucesso, mensagem)
        - deletar(id) -> (sucesso, mensagem)

    Alinhado com Ordem_Servico_Peca_Controller (aba "Peças Utilizadas"):
        - listar_pecas_da_ordem(ordem_servico_id) -> (sucesso, lista_de_Peca_ou_mensagem)
              cada Peca vem com .quantidade_os e .valor_unitario_os já resolvidos
        - salvar_pecas_da_ordem(ordem_servico_id, itens) -> (sucesso, mensagem)
              'itens' é [{"peca_id", "quantidade", "valor_unitario"}, ...] — SUBSTITUI
              tudo de uma vez, por isso a aba trabalha com uma lista em memória e só
              persiste ao clicar em "Salvar peças da ordem".

    IMPORTANTE (datas): tudo que entra ou sai dos campos de texto passa por
    DataUtils. O banco devolve objetos date, e str(date) produz "aaaa-mm-dd",
    formato que o controller rejeita. Nunca use str() direto numa data aqui.
    """

    STATUS_OPCOES = ["aberta", "em andamento", "concluida", "cancelada"]

    CAMPOS_TEXTO = [
        ("data_entrada_texto", "Data de entrada (dd/mm/aaaa):"),
        ("data_conclusao_texto", "Data de conclusão (opcional):"),
        ("problema", "Problema:"),
        ("diagnostico", "Diagnóstico:"),
        ("valor_total", "Valor total (R$):"),
        ("forma_pagamento", "Forma de pagamento:"),
        ("dias_garantia", "Dias de garantia:"),
    ]

    CAMPOS_ATUALIZAVEIS = [chave for chave, _ in CAMPOS_TEXTO if chave != "data_entrada_texto"]
    CAMPOS_IMUTAVEIS_NA_EDICAO = ["cliente", "funcionario", "equipamento"]

    def __init__(self, master, ordem_servico_controller, cliente_dao, funcionario_dao, equipamento_dao,
                 ordem_servico_servico_controller, servico_dao,
                 ordem_servico_peca_controller=None, peca_dao=None):
        super().__init__(master)
        self.master = master
        self.controller = ordem_servico_controller
        self.cliente_dao = cliente_dao
        self.funcionario_dao = funcionario_dao
        self.equipamento_dao = equipamento_dao

        # aba de serviços prestados (embutida)
        self.ordem_servico_servico_controller = ordem_servico_servico_controller
        self.servico_dao = servico_dao

        # aba de peças utilizadas (embutida)
        self.ordem_servico_peca_controller = ordem_servico_peca_controller
        self.peca_dao = peca_dao

        self.id_selecionado = None      # None = modo "novo cadastro" (ordem)
        self.id_item_servico_selecionado = None
        self.combos = {}
        self.entradas = {}

        self.master.title("Ordem de Serviço")

        self.notebook = ttk.Notebook(self)
        self.aba_dados = ttk.Frame(self.notebook)
        self.aba_servicos = ttk.Frame(self.notebook)
        self.aba_pecas = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_dados, text="Dados da Ordem")
        self.notebook.add(self.aba_servicos, text="Serviços Prestados")
        self.notebook.add(self.aba_pecas, text="Peças Utilizadas")
        self.notebook.pack(fill="both", expand=True)

        self._linha_atual = 0
        self._criar_combos()
        self._criar_campos_texto()
        self._criar_treeview()
        self._criar_botoes()
        self.tbl_ordens.bind("<<TreeviewSelect>>", self._selecionar_ordem)

        self._criar_aba_servicos()
        self._criar_aba_pecas()

        self._carregar_combos()
        self._atualizar_treeview()
        self._carregar_combo_servico_aba()
        self._atualizar_aba_servicos()
        self._carregar_combo_peca_aba()
        self._atualizar_aba_pecas()

        # Sem isso, o Frame nunca aparece dentro do Toplevel (janela fica em branco)
        self.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # Aba "Dados da Ordem" — construção
    # ------------------------------------------------------------------

    def _adicionar_linha(self, texto_label, widget):
        tk.Label(self.aba_dados, text=texto_label).grid(row=self._linha_atual, column=0, sticky="w", padx=5, pady=5)
        widget.grid(row=self._linha_atual, column=1, padx=5, pady=5)
        self._linha_atual += 1
        return widget

    def _criar_combos(self):
        self.combos["cliente"] = self._adicionar_linha(
            "Cliente:", ttk.Combobox(self.aba_dados, state="readonly", width=40)
        )
        self.combos["funcionario"] = self._adicionar_linha(
            "Funcionário:", ttk.Combobox(self.aba_dados, state="readonly", width=40)
        )
        self.combos["equipamento"] = self._adicionar_linha(
            "Equipamento:", ttk.Combobox(self.aba_dados, state="readonly", width=40)
        )

    def _criar_campos_texto(self):
        for chave, label in self.CAMPOS_TEXTO:
            self.entradas[chave] = self._adicionar_linha(label, tk.Entry(self.aba_dados, width=42))
            if chave == "data_conclusao_texto":
                self.combos["status"] = self._adicionar_linha(
                    "Status:", ttk.Combobox(self.aba_dados, state="readonly", width=40, values=self.STATUS_OPCOES)
                )
                self.combos["status"].current(0)

    def _criar_treeview(self):
        colunas_config = {
            "id": ("ID", 40, "center"),
            "cliente": ("Cliente", 140, "w"),
            "equipamento": ("Equipamento", 140, "w"),
            "status": ("Status", 100, "center"),
            "data_entrada": ("Entrada", 90, "center"),
        }

        self.tbl_ordens = ttk.Treeview(self.aba_dados, columns=tuple(colunas_config), show="headings", height=8)
        self.tbl_ordens.grid(row=self._linha_atual, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")
        self._linha_atual += 1

        for coluna, (titulo, largura, alinhamento) in colunas_config.items():
            self.tbl_ordens.heading(coluna, text=titulo)
            self.tbl_ordens.column(coluna, width=largura, anchor=alinhamento)

    def _criar_botoes(self):
        frame = tk.Frame(self.aba_dados)
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
    # Aba "Dados da Ordem" — carregamento de dados
    # ------------------------------------------------------------------

    def _carregar_combos(self):
        self.combos["cliente"]["values"] = [f"{c.id} - {c.nome}" for c in self.cliente_dao.get_all()]
        self.combos["funcionario"]["values"] = [f"{f.id} - {f.nome}" for f in self.funcionario_dao.get_all()]
        self.combos["equipamento"]["values"] = [
            f"{e.id} - {e.tipo} {e.marca} {e.modelo}" for e in self.equipamento_dao.get_all()
        ]

    def _atualizar_treeview(self):
        self.tbl_ordens.delete(*self.tbl_ordens.get_children())

        for ordem in self.controller.listar_todas():
            self.tbl_ordens.insert("", tk.END, values=(
                ordem.id,
                ordem.cliente.nome,
                f"{ordem.equipamento.tipo} {ordem.equipamento.marca} {ordem.equipamento.modelo}",
                ordem.status,
                DataUtils.data_para_string(ordem.data_entrada),   # dd/mm/aaaa, nunca o ISO do banco
            ))

    # ------------------------------------------------------------------
    # Helpers gerais
    # ------------------------------------------------------------------

    @staticmethod
    def _extrair_id_do_combo(texto_combo):
        return int(texto_combo.split(" - ")[0]) if texto_combo else None

    @staticmethod
    def _selecionar_valor_combo(combobox, id_procurado):
        valor = next((v for v in combobox["values"] if v.split(" - ")[0] == str(id_procurado)), "")
        combobox.set(valor)

    @staticmethod
    def _exibir_mensagem(titulo, mensagem, sucesso=True):
        (messagebox.showinfo if sucesso else messagebox.showerror)(titulo, mensagem)

    @staticmethod
    def _formatar_valor(valor):
        """Formata o valor total para exibição; se não for numérico, devolve o texto cru."""
        try:
            return f"{float(valor):.2f}"
        except (TypeError, ValueError):
            return "" if valor is None else str(valor)

    # ------------------------------------------------------------------
    # Aba "Dados da Ordem" — seleção na Treeview
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

        # Destrava ANTES de escrever: um Entry com state="disabled" recusa
        # delete/insert e derruba a tela ao selecionar a segunda ordem.
        self._travar_campos_imutaveis(False)

        self._selecionar_valor_combo(self.combos["cliente"], ordem.cliente.id)
        self._selecionar_valor_combo(self.combos["funcionario"], ordem.funcionario.id)
        self._selecionar_valor_combo(self.combos["equipamento"], ordem.equipamento.id)
        self.combos["status"].set(ordem.status)

        valores = {
            # As datas vêm do banco como objetos date — converter para dd/mm/aaaa
            "data_entrada_texto": DataUtils.data_para_string(ordem.data_entrada),
            "data_conclusao_texto": DataUtils.data_para_string(ordem.data_conclusao),
            "problema": ordem.problema,
            "diagnostico": ordem.diagnostico,
            "valor_total": self._formatar_valor(ordem.valor_total),
            "forma_pagamento": ordem.forma_pagamento,
            "dias_garantia": ordem.dias_garantia,
        }
        for chave, valor in valores.items():
            self.entradas[chave].delete(0, tk.END)
            self.entradas[chave].insert(0, "" if valor is None else str(valor))

        self._travar_campos_imutaveis(True)
        self._atualizar_aba_servicos()
        self._atualizar_aba_pecas()

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

        self._atualizar_aba_servicos()
        self._atualizar_aba_pecas()

    def _coletar_dados_cadastro(self):
        id_cliente = self._extrair_id_do_combo(self.combos["cliente"].get())
        id_funcionario = self._extrair_id_do_combo(self.combos["funcionario"].get())
        id_equipamento = self._extrair_id_do_combo(self.combos["equipamento"].get())

        if id_cliente is None or id_funcionario is None or id_equipamento is None:
            raise ValueError("Selecione cliente, funcionário e equipamento.")

        dados = {chave: self.entradas[chave].get().strip() for chave, _ in self.CAMPOS_TEXTO}
        dados.update(
            id_cliente=id_cliente,
            id_funcionario=id_funcionario,
            id_equipamento=id_equipamento,
            status=self.combos["status"].get(),
        )
        return dados

    def _coletar_dados_atualizacao(self):
        dados = {chave: self.entradas[chave].get().strip() for chave in self.CAMPOS_ATUALIZAVEIS}
        dados["status"] = self.combos["status"].get()
        return dados

    # ------------------------------------------------------------------
    # Aba "Dados da Ordem" — ações dos botões (CRUD)
    # ------------------------------------------------------------------

    def _executar_operacao(self, operacao, mensagem_sucesso):
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
        self.tbl_ordens.selection_remove(self.tbl_ordens.selection())
        self._limpar_campos()

    def _salvar(self):
        # Evita gravar uma ordem duplicada quando há uma já selecionada na lista
        if self.id_selecionado is not None:
            self._exibir_mensagem(
                "Aviso",
                'Há uma ordem selecionada. Use "Alterar" para editá-la ou "Novo" para começar um cadastro.',
                sucesso=False,
            )
            return

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

    # ------------------------------------------------------------------
    # Aba "Serviços Prestados" — construção
    # ------------------------------------------------------------------

    def _criar_aba_servicos(self):
        self.lbl_ordem_servicos = tk.Label(self.aba_servicos, text="", anchor="w", justify="left")
        self.lbl_ordem_servicos.pack(fill="x", padx=10, pady=(10, 5))

        form = tk.Frame(self.aba_servicos)
        form.pack(fill="x", padx=10, pady=5)

        tk.Label(form, text="Serviço:").grid(row=0, column=0, sticky="w")
        self.combo_servico_aba = ttk.Combobox(form, state="readonly", width=35)
        self.combo_servico_aba.grid(row=0, column=1, padx=5)
        self.combo_servico_aba.bind("<<ComboboxSelected>>", self._preencher_valor_padrao_servico)

        tk.Label(form, text="Valor cobrado (R$):").grid(row=1, column=0, sticky="w")
        self.entry_valor_cobrado_aba = tk.Entry(form, width=12)
        self.entry_valor_cobrado_aba.grid(row=1, column=1, sticky="w", padx=5)

        frame_botoes = tk.Frame(self.aba_servicos)
        frame_botoes.pack(pady=5)
        self.btn_add_servico = tk.Button(frame_botoes, text="Adicionar", width=14, command=self._adicionar_servico)
        self.btn_add_servico.pack(side="left", padx=5)
        self.btn_atualizar_servico = tk.Button(
            frame_botoes, text="Atualizar valor", width=14, command=self._atualizar_servico
        )
        self.btn_atualizar_servico.pack(side="left", padx=5)
        self.btn_remover_servico = tk.Button(frame_botoes, text="Remover", width=14, command=self._remover_servico)
        self.btn_remover_servico.pack(side="left", padx=5)

        colunas = ("id", "servico", "valor_cobrado")
        self.tbl_servicos = ttk.Treeview(self.aba_servicos, columns=colunas, show="headings", height=8)
        self.tbl_servicos.heading("id", text="ID")
        self.tbl_servicos.heading("servico", text="Serviço")
        self.tbl_servicos.heading("valor_cobrado", text="Valor Cobrado")
        self.tbl_servicos.column("id", width=40, anchor="center")
        self.tbl_servicos.column("servico", width=220)
        self.tbl_servicos.column("valor_cobrado", width=100, anchor="center")
        self.tbl_servicos.pack(fill="both", expand=True, padx=10, pady=10)
        self.tbl_servicos.bind("<<TreeviewSelect>>", self._selecionar_servico_da_aba)

        self._id_servico_por_item = {}

    def _criar_aba_pecas(self):
        if self.ordem_servico_peca_controller is None or self.peca_dao is None:
            tk.Label(
                self.aba_pecas,
                text="Gerenciamento de peças não conectado (controller/DAO não informados).",
                justify="left",
            ).pack(padx=15, pady=15, anchor="w")
            return

        self.lbl_ordem_pecas = tk.Label(self.aba_pecas, text="", anchor="w", justify="left")
        self.lbl_ordem_pecas.pack(fill="x", padx=10, pady=(10, 5))

        form = tk.Frame(self.aba_pecas)
        form.pack(fill="x", padx=10, pady=5)

        tk.Label(form, text="Peça:").grid(row=0, column=0, sticky="w")
        self.combo_peca_aba = ttk.Combobox(form, state="readonly", width=35)
        self.combo_peca_aba.grid(row=0, column=1, padx=5)
        self.combo_peca_aba.bind("<<ComboboxSelected>>", self._preencher_valor_padrao_peca)

        tk.Label(form, text="Quantidade:").grid(row=1, column=0, sticky="w")
        self.entry_quantidade_peca_aba = tk.Entry(form, width=10)
        self.entry_quantidade_peca_aba.grid(row=1, column=1, sticky="w", padx=5)

        tk.Label(form, text="Valor unitário (R$):").grid(row=2, column=0, sticky="w")
        self.entry_valor_unitario_peca_aba = tk.Entry(form, width=12)
        self.entry_valor_unitario_peca_aba.grid(row=2, column=1, sticky="w", padx=5)

        frame_botoes = tk.Frame(self.aba_pecas)
        frame_botoes.pack(pady=5)
        self.btn_add_peca = tk.Button(
            frame_botoes, text="Adicionar à lista", width=16, command=self._adicionar_peca_na_lista
        )
        self.btn_add_peca.pack(side="left", padx=5)
        self.btn_remover_peca = tk.Button(
            frame_botoes, text="Remover da lista", width=16, command=self._remover_peca_da_lista
        )
        self.btn_remover_peca.pack(side="left", padx=5)

        colunas = ("peca", "quantidade", "valor_unitario", "subtotal")
        self.tbl_pecas = ttk.Treeview(self.aba_pecas, columns=colunas, show="headings", height=7)
        self.tbl_pecas.heading("peca", text="Peça")
        self.tbl_pecas.heading("quantidade", text="Qtd.")
        self.tbl_pecas.heading("valor_unitario", text="Valor unit.")
        self.tbl_pecas.heading("subtotal", text="Subtotal")
        self.tbl_pecas.column("peca", width=200)
        self.tbl_pecas.column("quantidade", width=60, anchor="center")
        self.tbl_pecas.column("valor_unitario", width=90, anchor="center")
        self.tbl_pecas.column("subtotal", width=90, anchor="center")
        self.tbl_pecas.pack(fill="both", expand=True, padx=10, pady=10)
        self.tbl_pecas.bind("<<TreeviewSelect>>", self._selecionar_peca_da_aba)

        frame_total = tk.Frame(self.aba_pecas)
        frame_total.pack(fill="x", padx=10, pady=(0, 5))
        self.lbl_total_pecas = tk.Label(frame_total, text="Total peças: R$ 0.00", anchor="e")
        self.lbl_total_pecas.pack(side="right")

        self.btn_salvar_pecas = tk.Button(
            self.aba_pecas, text="Salvar peças da ordem", command=self._salvar_pecas
        )
        self.btn_salvar_pecas.pack(pady=10)

        # lista de trabalho em memória: peca_id -> {"nome", "quantidade", "valor_unitario"}
        # só vira persistência de fato quando "Salvar peças da ordem" é clicado
        self._lista_pecas_local = {}

    # ------------------------------------------------------------------
    # Aba "Serviços Prestados" — carregamento de dados
    # ------------------------------------------------------------------

    def _carregar_combo_servico_aba(self):
        self.servicos_disponiveis = self.servico_dao.get_all()
        self.combo_servico_aba["values"] = [f"{s.id} - {s.nome}" for s in self.servicos_disponiveis]

    def _atualizar_aba_servicos(self):
        """Recarrega a aba de Serviços Prestados para a ordem atualmente selecionada na aba Dados."""
        habilitado = self.id_selecionado is not None

        self.combo_servico_aba.config(state="readonly" if habilitado else "disabled")
        self.entry_valor_cobrado_aba.config(state="normal" if habilitado else "disabled")
        estado_botoes = "normal" if habilitado else "disabled"
        self.btn_add_servico.config(state=estado_botoes)
        self.btn_atualizar_servico.config(state=estado_botoes)
        self.btn_remover_servico.config(state=estado_botoes)

        self.tbl_servicos.delete(*self.tbl_servicos.get_children())
        self._id_servico_por_item.clear()
        self._limpar_form_servico()

        if not habilitado:
            self.lbl_ordem_servicos.config(
                text='Selecione ou salve uma ordem na aba "Dados da Ordem" para gerenciar os serviços.'
            )
            return

        self.lbl_ordem_servicos.config(text=f"Serviços da ordem #{self.id_selecionado}")

        sucesso, resultado = self.ordem_servico_servico_controller.buscar_por_ordem(self.id_selecionado)
        if not sucesso:
            self._exibir_mensagem("Erro", resultado, sucesso=False)
            return

        for item in resultado:
            iid = str(item.id)
            self.tbl_servicos.insert(
                "", tk.END, iid=iid, values=(item.id, item.servico.nome, f"{item.valor_cobrado:.2f}")
            )
            self._id_servico_por_item[iid] = item.id_servico

    # ------------------------------------------------------------------
    # Aba "Serviços Prestados" — seleção e ações
    # ------------------------------------------------------------------

    def _preencher_valor_padrao_servico(self, event=None):
        if not self.combo_servico_aba.get():
            return
        servico_id = int(self.combo_servico_aba.get().split(" - ")[0])
        servico = next((s for s in self.servicos_disponiveis if s.id == servico_id), None)
        if servico is None:
            return

        self.entry_valor_cobrado_aba.delete(0, tk.END)
        self.entry_valor_cobrado_aba.insert(0, f"{servico.valor_padrao:.2f}")

    def _selecionar_servico_da_aba(self, event=None):
        selecao = self.tbl_servicos.selection()
        if not selecao:
            return

        iid = selecao[0]
        self.id_item_servico_selecionado = int(iid)

        id_servico = self._id_servico_por_item.get(iid)
        texto_combo = next(
            (v for v in self.combo_servico_aba["values"] if v.split(" - ")[0] == str(id_servico)), ""
        )
        self.combo_servico_aba.config(state="readonly")
        self.combo_servico_aba.set(texto_combo)
        # O serviço vinculado não muda depois de criado — só o valor cobrado é editável
        self.combo_servico_aba.config(state="disabled")

        valores = self.tbl_servicos.item(iid, "values")
        self.entry_valor_cobrado_aba.delete(0, tk.END)
        self.entry_valor_cobrado_aba.insert(0, valores[2])

    def _limpar_form_servico(self):
        self.id_item_servico_selecionado = None
        if self.id_selecionado is not None:
            self.combo_servico_aba.config(state="readonly")
        self.combo_servico_aba.set("")

        # Um Entry desabilitado recusa delete(); habilita só o tempo da limpeza
        estado_original = str(self.entry_valor_cobrado_aba["state"])
        self.entry_valor_cobrado_aba.config(state="normal")
        self.entry_valor_cobrado_aba.delete(0, tk.END)
        self.entry_valor_cobrado_aba.config(state=estado_original)

    def _adicionar_servico(self):
        if self.id_selecionado is None:
            self._exibir_mensagem("Aviso", "Selecione ou salve uma ordem de serviço primeiro.", sucesso=False)
            return
        if not self.combo_servico_aba.get():
            self._exibir_mensagem("Aviso", "Selecione um serviço.", sucesso=False)
            return

        servico_id = int(self.combo_servico_aba.get().split(" - ")[0])
        sucesso, resultado = self.ordem_servico_servico_controller.cadastrar(
            ordem_servico_id=self.id_selecionado,
            servico_id=servico_id,
            valor_cobrado=self.entry_valor_cobrado_aba.get(),
        )

        if sucesso:
            self._exibir_mensagem("Sucesso", "Serviço adicionado com sucesso!")
            self._atualizar_aba_servicos()
        else:
            self._exibir_mensagem("Erro", resultado, sucesso=False)

    def _atualizar_servico(self):
        if self.id_item_servico_selecionado is None:
            self._exibir_mensagem("Aviso", "Selecione um serviço na lista para atualizar.", sucesso=False)
            return

        sucesso, resultado = self.ordem_servico_servico_controller.atualizar(
            id=self.id_item_servico_selecionado,
            valor_cobrado=self.entry_valor_cobrado_aba.get(),
        )

        if sucesso:
            self._exibir_mensagem("Sucesso", resultado)
            self._atualizar_aba_servicos()
        else:
            self._exibir_mensagem("Erro", resultado, sucesso=False)

    def _remover_servico(self):
        if self.id_item_servico_selecionado is None:
            self._exibir_mensagem("Aviso", "Selecione um serviço na lista para remover.", sucesso=False)
            return

        if not messagebox.askyesno("Confirmação", "Remover este serviço da ordem?"):
            return

        sucesso, resultado = self.ordem_servico_servico_controller.deletar(self.id_item_servico_selecionado)
        if sucesso:
            self._exibir_mensagem("Sucesso", resultado)
            self._atualizar_aba_servicos()
        else:
            self._exibir_mensagem("Erro", resultado, sucesso=False)

    # ------------------------------------------------------------------
    # Aba "Peças Utilizadas" — carregamento de dados
    # ------------------------------------------------------------------

    def _carregar_combo_peca_aba(self):
        if self.ordem_servico_peca_controller is None or self.peca_dao is None:
            return
        self.pecas_disponiveis = self.peca_dao.get_all()
        self.combo_peca_aba["values"] = [f"{p.id} - {p.nome}" for p in self.pecas_disponiveis]

    def _atualizar_aba_pecas(self):
        """Recarrega a lista de trabalho de peças a partir do banco, descartando edições não salvas."""
        if self.ordem_servico_peca_controller is None or self.peca_dao is None:
            return

        habilitado = self.id_selecionado is not None

        self.combo_peca_aba.config(state="readonly" if habilitado else "disabled")
        estado = "normal" if habilitado else "disabled"
        self.btn_add_peca.config(state=estado)
        self.btn_remover_peca.config(state=estado)
        self.btn_salvar_pecas.config(state=estado)

        self._lista_pecas_local = {}
        # Limpa os campos enquanto ainda estão habilitados, depois aplica o estado final
        self._limpar_form_peca()
        self.entry_quantidade_peca_aba.config(state=estado)
        self.entry_valor_unitario_peca_aba.config(state=estado)

        if not habilitado:
            self.lbl_ordem_pecas.config(
                text='Selecione ou salve uma ordem na aba "Dados da Ordem" para gerenciar as peças.'
            )
            self._renderizar_tabela_pecas()
            return

        self.lbl_ordem_pecas.config(text=f"Peças da ordem #{self.id_selecionado}")

        sucesso, resultado = self.ordem_servico_peca_controller.listar_pecas_da_ordem(self.id_selecionado)
        if not sucesso:
            self._exibir_mensagem("Erro", resultado, sucesso=False)
            self._renderizar_tabela_pecas()
            return

        for peca in resultado:
            self._lista_pecas_local[peca.id] = {
                "nome": peca.nome,
                "quantidade": peca.quantidade_os,
                "valor_unitario": peca.valor_unitario_os,
            }

        self._renderizar_tabela_pecas()

    def _renderizar_tabela_pecas(self):
        """Redesenha a Treeview e o total a partir da lista de trabalho em memória."""
        self.tbl_pecas.delete(*self.tbl_pecas.get_children())
        total = 0.0
        for peca_id, dados in self._lista_pecas_local.items():
            subtotal = float(dados["quantidade"]) * float(dados["valor_unitario"])
            total += subtotal
            self.tbl_pecas.insert("", tk.END, iid=str(peca_id), values=(
                dados["nome"],
                dados["quantidade"],
                f"{float(dados['valor_unitario']):.2f}",
                f"{subtotal:.2f}",
            ))
        self.lbl_total_pecas.config(text=f"Total peças: R$ {total:.2f}")

    # ------------------------------------------------------------------
    # Aba "Peças Utilizadas" — seleção e ações
    # ------------------------------------------------------------------

    def _preencher_valor_padrao_peca(self, event=None):
        if not self.combo_peca_aba.get():
            return
        peca_id = int(self.combo_peca_aba.get().split(" - ")[0])
        peca = next((p for p in self.pecas_disponiveis if p.id == peca_id), None)
        if peca is None:
            return

        self.entry_valor_unitario_peca_aba.delete(0, tk.END)
        self.entry_valor_unitario_peca_aba.insert(0, f"{peca.preco_venda:.2f}")
        self.entry_quantidade_peca_aba.delete(0, tk.END)
        self.entry_quantidade_peca_aba.insert(0, "1")

    def _selecionar_peca_da_aba(self, event=None):
        """Ao clicar numa peça já na lista, carrega os valores dela no formulário pra editar."""
        selecao = self.tbl_pecas.selection()
        if not selecao:
            return

        peca_id = int(selecao[0])
        dados = self._lista_pecas_local.get(peca_id)
        if dados is None:
            return

        texto_combo = next(
            (v for v in self.combo_peca_aba["values"] if v.split(" - ")[0] == str(peca_id)), ""
        )
        self.combo_peca_aba.set(texto_combo)
        self.entry_quantidade_peca_aba.delete(0, tk.END)
        self.entry_quantidade_peca_aba.insert(0, str(dados["quantidade"]))
        self.entry_valor_unitario_peca_aba.delete(0, tk.END)
        self.entry_valor_unitario_peca_aba.insert(0, f"{float(dados['valor_unitario']):.2f}")

    def _limpar_form_peca(self):
        self.combo_peca_aba.set("")
        for entrada in (self.entry_quantidade_peca_aba, self.entry_valor_unitario_peca_aba):
            estado_original = str(entrada["state"])
            entrada.config(state="normal")
            entrada.delete(0, tk.END)
            entrada.config(state=estado_original)

    def _adicionar_peca_na_lista(self):
        """Adiciona (ou atualiza, se a peça já estiver na lista) um item na lista de trabalho.
        Não persiste no banco ainda — isso só acontece em 'Salvar peças da ordem'."""
        if self.id_selecionado is None:
            self._exibir_mensagem("Aviso", "Selecione ou salve uma ordem de serviço primeiro.", sucesso=False)
            return
        if not self.combo_peca_aba.get():
            self._exibir_mensagem("Aviso", "Selecione uma peça.", sucesso=False)
            return

        peca_id = int(self.combo_peca_aba.get().split(" - ")[0])
        peca = next((p for p in self.pecas_disponiveis if p.id == peca_id), None)
        if peca is None:
            self._exibir_mensagem("Erro", "Peça não encontrada na lista de peças disponíveis.", sucesso=False)
            return

        try:
            quantidade = int(self.entry_quantidade_peca_aba.get())
        except ValueError:
            self._exibir_mensagem("Erro de validação", "Quantidade precisa ser um número inteiro.", sucesso=False)
            return
        if quantidade <= 0:
            self._exibir_mensagem("Erro de validação", "Quantidade deve ser maior que zero.", sucesso=False)
            return

        try:
            valor_unitario = float(self.entry_valor_unitario_peca_aba.get())
        except ValueError:
            self._exibir_mensagem("Erro de validação", "Valor unitário precisa ser um número.", sucesso=False)
            return
        if valor_unitario < 0:
            self._exibir_mensagem("Erro de validação", "Valor unitário não pode ser negativo.", sucesso=False)
            return

        self._lista_pecas_local[peca_id] = {
            "nome": peca.nome,
            "quantidade": quantidade,
            "valor_unitario": valor_unitario,
        }
        self._renderizar_tabela_pecas()
        self._limpar_form_peca()

    def _remover_peca_da_lista(self):
        """Remove da lista de trabalho (em memória) — só efetiva no banco após 'Salvar peças da ordem'."""
        selecao = self.tbl_pecas.selection()
        if not selecao:
            self._exibir_mensagem("Aviso", "Selecione uma peça na lista para remover.", sucesso=False)
            return

        peca_id = int(selecao[0])
        self._lista_pecas_local.pop(peca_id, None)
        self._renderizar_tabela_pecas()
        self._limpar_form_peca()

    def _salvar_pecas(self):
        """Persiste a lista de trabalho inteira, substituindo tudo que a ordem tinha antes."""
        if self.id_selecionado is None:
            self._exibir_mensagem("Aviso", "Selecione ou salve uma ordem de serviço primeiro.", sucesso=False)
            return

        itens = [
            {"peca_id": peca_id, "quantidade": dados["quantidade"], "valor_unitario": dados["valor_unitario"]}
            for peca_id, dados in self._lista_pecas_local.items()
        ]

        sucesso, resultado = self.ordem_servico_peca_controller.salvar_pecas_da_ordem(self.id_selecionado, itens)
        if sucesso:
            self._exibir_mensagem("Sucesso", resultado)
            self._atualizar_aba_pecas()
        else:
            self._exibir_mensagem("Erro", resultado, sucesso=False)