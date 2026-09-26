import tkinter as tk
from tkinter import ttk, messagebox

from app.core.dataUltils import DataUtils
from app.view.estilo_view import (
    COR_FUNDO_JANELA, COR_TITULO, COR_SUBTITULO, CORES_MODULOS,
    FONTE_LABEL, FONTE_LABEL_NEGRITO,
    configurar_janela, criar_cabecalho, criar_botao, estilizar_entry,
    estilizar_botao_tk, aplicar_tema_widgets,
)

class Ordem_servico_View(tk.Frame):
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
    CAMPOS_ATUALIZAVEIS = [c for c, _ in CAMPOS_TEXTO if c != "data_entrada_texto"]
    CAMPOS_IMUTAVEIS_NA_EDICAO = ["cliente", "funcionario", "equipamento"]

    def __init__(self, master, ordem_servico_controller, cliente_dao, funcionario_dao, equipamento_dao,
                 ordem_servico_servico_controller, servico_dao,
                 ordem_servico_peca_controller=None, peca_dao=None):
        super().__init__(master, bg=COR_FUNDO_JANELA)
        self.master = master
        self.controller = ordem_servico_controller
        self.cliente_dao = cliente_dao
        self.funcionario_dao = funcionario_dao
        self.equipamento_dao = equipamento_dao

        self.ordem_servico_servico_controller = ordem_servico_servico_controller
        self.servico_dao = servico_dao
        self.ordem_servico_peca_controller = ordem_servico_peca_controller
        self.peca_dao = peca_dao

        self.id_selecionado = None
        self.id_item_servico_selecionado = None
        self.combos = {}
        self.entradas = {}
        self._lista_pecas_local = {}

        configurar_janela(self.master, "Ordens de Serviço")
        self._estilo_tabela = aplicar_tema_widgets()

        criar_cabecalho(
            self, "Ordens de Serviço", "Abrir, acompanhar e concluir atendimentos",
            cor_destaque=CORES_MODULOS["ordem_servico"],
        )

        self._iniciar_interface()
        self._carregar_dados_iniciais()
        self.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # CONSTRUÇÃO DA INTERFACE (Helpers e Abas)
    # ------------------------------------------------------------------
    
    def _iniciar_interface(self):
        corpo = tk.Frame(self, bg=COR_FUNDO_JANELA)
        corpo.pack(fill="both", expand=True, padx=30, pady=(0, 24))

        self.notebook = ttk.Notebook(corpo)
        self.aba_dados = ttk.Frame(self.notebook)
        self.aba_servicos = ttk.Frame(self.notebook)
        self.aba_pecas = ttk.Frame(self.notebook)
        
        self.notebook.add(self.aba_dados, text="Dados da Ordem")
        self.notebook.add(self.aba_servicos, text="Serviços Prestados")
        self.notebook.add(self.aba_pecas, text="Peças Utilizadas")
        self.notebook.pack(fill="both", expand=True)

        self._criar_aba_dados()
        self._criar_aba_servicos()
        self._criar_aba_pecas()

    def _criar_campo_form(self, parent, label_texto, widget, row=None, col=None, pack=False):
        """Helper para criar Label + Widget reduzindo duplicação."""
        lbl = tk.Label(parent, text=label_texto, bg=COR_FUNDO_JANELA, fg=COR_SUBTITULO, font=FONTE_LABEL)
        if pack:
            lbl.pack(anchor="w", pady=(4, 0))
            widget.pack(fill="x", pady=(0, 4))
        else:
            lbl.grid(row=row, column=col, sticky="w", padx=8, pady=4)
            widget.grid(row=row, column=col+1, sticky="w", padx=8, pady=4)
        return widget

    def _criar_tabela(self, parent, colunas_config, height=8):
        """Helper genérico para criar Treeviews configuradas."""
        colunas_ids = [c[0] for c in colunas_config]
        tabela = ttk.Treeview(parent, columns=colunas_ids, show="headings", height=height, style=self._estilo_tabela)
        for col_id, titulo, largura, alinhamento in colunas_config:
            tabela.heading(col_id, text=titulo)
            tabela.column(col_id, width=largura, anchor=alinhamento)
        return tabela

    # --- ABA 1: DADOS DA ORDEM ---
    def _criar_aba_dados(self):
        linha = 0
        for chave, lbl in [("cliente", "Cliente:"), ("funcionario", "Funcionário:"), ("equipamento", "Equipamento:")]:
            self.combos[chave] = self._criar_campo_form(self.aba_dados, lbl, ttk.Combobox(self.aba_dados, state="readonly", width=40), row=linha, col=0)
            linha += 1

        for chave, label in self.CAMPOS_TEXTO:
            entry = tk.Entry(self.aba_dados, width=42)
            estilizar_entry(entry)
            self.entradas[chave] = self._criar_campo_form(self.aba_dados, label, entry, row=linha, col=0)
            
            if chave == "data_conclusao_texto":
                self.combos["status"] = self._criar_campo_form(self.aba_dados, "Status:", ttk.Combobox(self.aba_dados, state="readonly", width=40, values=self.STATUS_OPCOES), row=linha, col=0)
                self.combos["status"].current(0)
                linha += 1
            linha += 1

        self.tbl_ordens = self._criar_tabela(self.aba_dados, [
            ("id", "ID", 40, "center"), ("cliente", "Cliente", 140, "w"),
            ("equipamento", "Equipamento", 140, "w"), ("status", "Status", 100, "center"),
            ("data_entrada", "Entrada", 90, "center")
        ])
        self.tbl_ordens.grid(row=linha, column=0, columnspan=2, padx=8, pady=14, sticky="nsew")
        self.tbl_ordens.bind("<<TreeviewSelect>>", self._selecionar_ordem)
        linha += 1

        frame_btn = tk.Frame(self.aba_dados, bg=COR_FUNDO_JANELA)
        frame_btn.grid(row=linha, column=0, columnspan=2, pady=14)
        for c, (txt, cmd, est) in enumerate([("Novo", self._novo, "primario"), ("Salvar", self._salvar, "primario"), ("Alterar", self._alterar, "primario"), ("Excluir", self._excluir, "perigo")]):
            criar_botao(frame_btn, txt, cmd, estilo=est).grid(row=0, column=c, padx=6)

    # --- ABA 2: SERVIÇOS PRESTADOS ---
    def _criar_aba_servicos(self):
        self.lbl_ordem_servicos = tk.Label(self.aba_servicos, text="", bg=COR_FUNDO_JANELA, fg=COR_TITULO, font=FONTE_LABEL_NEGRITO)
        self.lbl_ordem_servicos.pack(fill="x", padx=14, pady=(14, 8), anchor="w")

        form = tk.Frame(self.aba_servicos, bg=COR_FUNDO_JANELA)
        form.pack(fill="x", padx=14, pady=5)

        self.combo_servico_aba = self._criar_campo_form(form, "Serviço:", ttk.Combobox(form, state="readonly", width=35), row=0, col=0)
        self.combo_servico_aba.bind("<<ComboboxSelected>>", self._preencher_valor_padrao_servico)
        
        self.entry_valor_cobrado_aba = tk.Entry(form, width=12)
        estilizar_entry(self.entry_valor_cobrado_aba)
        self._criar_campo_form(form, "Valor cobrado (R$):", self.entry_valor_cobrado_aba, row=1, col=0)

        frame_btn = tk.Frame(self.aba_servicos, bg=COR_FUNDO_JANELA)
        frame_btn.pack(pady=8)
        self.botoes_servico = []
        for txt, cmd, width, est in [("Adicionar", self._adicionar_servico, 14, None), ("Atualizar valor", self._atualizar_servico, 14, None), ("Remover", self._remover_servico, 14, "perigo")]:
            btn = tk.Button(frame_btn, text=txt, width=width, command=cmd)
            estilizar_botao_tk(btn, estilo=est) if est else estilizar_botao_tk(btn)
            btn.pack(side="left", padx=5)
            self.botoes_servico.append(btn)

        self.tbl_servicos = self._criar_tabela(self.aba_servicos, [("id", "ID", 40, "center"), ("servico", "Serviço", 220, "w"), ("valor", "Valor Cobrado", 100, "center")])
        self.tbl_servicos.pack(fill="both", expand=True, padx=14, pady=14)
        self.tbl_servicos.bind("<<TreeviewSelect>>", self._selecionar_servico_da_aba)
        self._id_servico_por_item = {}

    # --- ABA 3: PEÇAS UTILIZADAS ---
    def _criar_aba_pecas(self):
        if not self.ordem_servico_peca_controller:
            tk.Label(self.aba_pecas, text="Gerenciamento de peças não conectado.", bg=COR_FUNDO_JANELA, font=FONTE_LABEL).pack(padx=15, pady=15, anchor="w")
            return

        self.lbl_ordem_pecas = tk.Label(self.aba_pecas, text="", bg=COR_FUNDO_JANELA, fg=COR_TITULO, font=FONTE_LABEL_NEGRITO)
        self.lbl_ordem_pecas.pack(fill="x", padx=14, pady=(14, 8), anchor="w")

        form = tk.Frame(self.aba_pecas, bg=COR_FUNDO_JANELA)
        form.pack(fill="x", padx=14, pady=5)

        self.combo_peca_aba = self._criar_campo_form(form, "Peça:", ttk.Combobox(form, state="readonly", width=35), row=0, col=0)
        self.combo_peca_aba.bind("<<ComboboxSelected>>", self._preencher_valor_padrao_peca)

        self.entry_quantidade_peca_aba = tk.Entry(form, width=10)
        estilizar_entry(self.entry_quantidade_peca_aba)
        self._criar_campo_form(form, "Quantidade:", self.entry_quantidade_peca_aba, row=1, col=0)

        self.entry_valor_unitario_peca_aba = tk.Entry(form, width=12)
        estilizar_entry(self.entry_valor_unitario_peca_aba)
        self._criar_campo_form(form, "Valor unit. (R$):", self.entry_valor_unitario_peca_aba, row=2, col=0)

        frame_btn = tk.Frame(self.aba_pecas, bg=COR_FUNDO_JANELA)
        frame_btn.pack(pady=8)
        self.botoes_peca = []
        for txt, cmd, width, est in [("Adicionar à lista", self._adicionar_peca_na_lista, 16, None), ("Remover da lista", self._remover_peca_da_lista, 16, "perigo")]:
            btn = tk.Button(frame_btn, text=txt, width=width, command=cmd)
            estilizar_botao_tk(btn, estilo=est) if est else estilizar_botao_tk(btn)
            btn.pack(side="left", padx=5)
            self.botoes_peca.append(btn)

        self.tbl_pecas = self._criar_tabela(self.aba_pecas, [("peca", "Peça", 200, "w"), ("qtd", "Qtd.", 60, "center"), ("valor", "Valor unit.", 90, "center"), ("subtotal", "Subtotal", 90, "center")], height=7)
        self.tbl_pecas.pack(fill="both", expand=True, padx=14, pady=14)
        self.tbl_pecas.bind("<<TreeviewSelect>>", self._selecionar_peca_da_aba)

        self.lbl_total_pecas = tk.Label(self.aba_pecas, text="Total peças: R$ 0.00", bg=COR_FUNDO_JANELA, fg=COR_TITULO, font=FONTE_LABEL_NEGRITO)
        self.lbl_total_pecas.pack(side="right", padx=14, pady=8)

        self.btn_salvar_pecas = tk.Button(self.aba_pecas, text="Salvar peças da ordem", command=self._salvar_pecas)
        estilizar_botao_tk(self.btn_salvar_pecas)
        self.btn_salvar_pecas.pack(pady=12)

    # ------------------------------------------------------------------
    # CARREGAMENTO E SINCRONIZAÇÃO
    # ------------------------------------------------------------------
    
    def _carregar_dados_iniciais(self):
        self.combos["cliente"]["values"] = [f"{c.id} - {c.nome}" for c in self.cliente_dao.get_all()]
        self.combos["funcionario"]["values"] = [f"{f.id} - {f.nome}" for f in self.funcionario_dao.get_all()]
        self.combos["equipamento"]["values"] = [f"{e.id} - {e.tipo} {e.marca}" for e in self.equipamento_dao.get_all()]
        
        self._atualizar_treeview()
        self._carregar_combo_servico_aba()
        self._carregar_combo_peca_aba()
        self._atualizar_aba_servicos()
        self._atualizar_aba_pecas()

    def _atualizar_treeview(self):
        self.tbl_ordens.delete(*self.tbl_ordens.get_children())
        for o in self.controller.listar_todas():
            self.tbl_ordens.insert("", tk.END, values=(o.id, o.cliente.nome, f"{o.equipamento.tipo} {o.equipamento.marca}", o.status, DataUtils.data_para_string(o.data_entrada)))

    def _alternar_estado_widgets(self, widgets, estado):
        """Ativa/Desativa listas de widgets."""
        for w in widgets: w.config(state=estado)

    # ------------------------------------------------------------------
    # LÓGICA DE DADOS DA ORDEM (CRUD)
    # ------------------------------------------------------------------
    # (Toda a lógica de tratamento de dados mantida idêntica para não quebrar validações)
    
    def _selecionar_ordem(self, event=None):
        if not (sel := self.tbl_ordens.selection()): return
        try:
            ordem = self.controller.buscar_por_id(self.tbl_ordens.item(sel[0])["values"][0])
            self.id_selecionado = ordem.id
            self._travar_campos_imutaveis(False)
            
            for c, v in [("cliente", ordem.cliente.id), ("funcionario", ordem.funcionario.id), ("equipamento", ordem.equipamento.id)]:
                self._selecionar_valor_combo(self.combos[c], v)
            self.combos["status"].set(ordem.status)

            valores = {
                "data_entrada_texto": DataUtils.data_para_string(ordem.data_entrada),
                "data_conclusao_texto": DataUtils.data_para_string(ordem.data_conclusao),
                "problema": ordem.problema, "diagnostico": ordem.diagnostico,
                "valor_total": self._formatar_valor(ordem.valor_total),
                "forma_pagamento": ordem.forma_pagamento, "dias_garantia": ordem.dias_garantia,
            }
            for k, v in valores.items():
                self.entradas[k].delete(0, tk.END)
                self.entradas[k].insert(0, "" if v is None else str(v))

            self._travar_campos_imutaveis(True)
            self._atualizar_aba_servicos()
            self._atualizar_aba_pecas()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _travar_campos_imutaveis(self, travar):
        estado_combo = "disabled" if travar else "readonly"
        for c in self.CAMPOS_IMUTAVEIS_NA_EDICAO: self.combos[c].config(state=estado_combo)
        self.entradas["data_entrada_texto"].config(state="disabled" if travar else "normal")

    def _limpar_campos(self):
        self.id_selecionado = None
        self._travar_campos_imutaveis(False)
        for c in self.combos.values(): c.set("")
        self.combos["status"].current(0)
        for e in self.entradas.values(): e.delete(0, tk.END)
        self._atualizar_aba_servicos()
        self._atualizar_aba_pecas()

    def _coletar_dados_cadastro(self):
        dados = {k: self.entradas[k].get().strip() for k, _ in self.CAMPOS_TEXTO}
        dados.update(
            id_cliente=self._extrair_id_combo(self.combos["cliente"].get()),
            id_funcionario=self._extrair_id_combo(self.combos["funcionario"].get()),
            id_equipamento=self._extrair_id_combo(self.combos["equipamento"].get()),
            status=self.combos["status"].get()
        )
        return dados

    def _coletar_dados_atualizacao(self):
        dados = {k: self.entradas[k].get().strip() for k in self.CAMPOS_ATUALIZAVEIS}
        dados["status"] = self.combos["status"].get()
        return dados

    def _novo(self): self._limpar_campos(); self.tbl_ordens.selection_remove(self.tbl_ordens.selection())
    def _salvar(self): 
        if self.id_selecionado: return messagebox.showwarning("Aviso", "Use 'Alterar' para editar ou 'Novo' para cadastrar.")
        self._executar_operacao(lambda: self.controller.cadastrar(**self._coletar_dados_cadastro()), "Cadastrada com sucesso!")
    def _alterar(self): self._executar_operacao(lambda: self.controller.atualizar(self.id_selecionado, **self._coletar_dados_atualizacao()), "Alterada com sucesso!") if self.id_selecionado else messagebox.showwarning("Aviso", "Selecione uma ordem.")
    def _excluir(self): self._executar_operacao(lambda: self.controller.excluir(self.id_selecionado), "Excluída com sucesso!") if self.id_selecionado and messagebox.askyesno("Confirmação", "Excluir ordem?") else None

    # ------------------------------------------------------------------
    # LÓGICA DE SERVIÇOS PRESTADOS
    # ------------------------------------------------------------------
    
    def _carregar_combo_servico_aba(self):
        self.servicos_disp = self.servico_dao.get_all()
        self.combo_servico_aba["values"] = [f"{s.id} - {s.nome}" for s in self.servicos_disp]

    def _atualizar_aba_servicos(self):
        habilitado = self.id_selecionado is not None
        self._alternar_estado_widgets([self.combo_servico_aba], "readonly" if habilitado else "disabled")
        self._alternar_estado_widgets([self.entry_valor_cobrado_aba] + self.botoes_servico, "normal" if habilitado else "disabled")
        self.tbl_servicos.delete(*self.tbl_servicos.get_children())
        self._id_servico_por_item.clear()
        
        if not habilitado:
            self.lbl_ordem_servicos.config(text="Selecione/salve uma ordem para gerir serviços.")
            return

        self.lbl_ordem_servicos.config(text=f"Serviços da ordem #{self.id_selecionado}")
        suc, res = self.ordem_servico_servico_controller.buscar_por_ordem(self.id_selecionado)
        if suc:
            for i in res:
                self.tbl_servicos.insert("", tk.END, iid=str(i.id), values=(i.id, i.servico.nome, f"{i.valor_cobrado:.2f}"))
                self._id_servico_por_item[str(i.id)] = i.id_servico

    def _preencher_valor_padrao_servico(self, e=None):
        if s := next((x for x in self.servicos_disp if x.id == self._extrair_id_combo(self.combo_servico_aba.get())), None):
            self.entry_valor_cobrado_aba.delete(0, tk.END); self.entry_valor_cobrado_aba.insert(0, f"{s.valor_padrao:.2f}")

    def _selecionar_servico_da_aba(self, e=None):
        if not (sel := self.tbl_servicos.selection()): return
        self.id_item_servico_selecionado = int(sel[0])
        self.combo_servico_aba.config(state="readonly")
        self._selecionar_valor_combo(self.combo_servico_aba, self._id_servico_por_item.get(sel[0]))
        self.combo_servico_aba.config(state="disabled")
        self.entry_valor_cobrado_aba.delete(0, tk.END); self.entry_valor_cobrado_aba.insert(0, self.tbl_servicos.item(sel[0], "values")[2])

    def _adicionar_servico(self):
        if not self.combo_servico_aba.get(): return messagebox.showwarning("Aviso", "Selecione um serviço.")
        suc, res = self.ordem_servico_servico_controller.cadastrar(self.id_selecionado, self._extrair_id_combo(self.combo_servico_aba.get()), self.entry_valor_cobrado_aba.get())
        self._atualizar_aba_servicos() if suc else messagebox.showerror("Erro", res)

    def _atualizar_servico(self):
        if not self.id_item_servico_selecionado: return
        suc, res = self.ordem_servico_servico_controller.atualizar(self.id_item_servico_selecionado, self.entry_valor_cobrado_aba.get())
        self._atualizar_aba_servicos() if suc else messagebox.showerror("Erro", res)

    def _remover_servico(self):
        if self.id_item_servico_selecionado and messagebox.askyesno("Confirmar", "Remover serviço?"):
            suc, res = self.ordem_servico_servico_controller.deletar(self.id_item_servico_selecionado)
            self._atualizar_aba_servicos() if suc else messagebox.showerror("Erro", res)

    # ------------------------------------------------------------------
    # LÓGICA DE PEÇAS UTILIZADAS (Completada)
    # ------------------------------------------------------------------
    
    def _carregar_combo_peca_aba(self):
        if not self.peca_dao: return
        self.pecas_disp = self.peca_dao.get_all()
        self.combo_peca_aba["values"] = [f"{p.id} - {p.nome}" for p in self.pecas_disp]

    def _atualizar_aba_pecas(self):
        if not self.peca_dao: return
        habilitado = self.id_selecionado is not None
        
        self._alternar_estado_widgets([self.combo_peca_aba], "readonly" if habilitado else "disabled")
        self._alternar_estado_widgets([self.entry_quantidade_peca_aba, self.entry_valor_unitario_peca_aba, self.btn_salvar_pecas] + self.botoes_peca, "normal" if habilitado else "disabled")
        self._lista_pecas_local.clear()

        if not habilitado:
            self.lbl_ordem_pecas.config(text="Selecione/salve uma ordem para gerir peças.")
            self._renderizar_tabela_pecas()
            return

        self.lbl_ordem_pecas.config(text=f"Peças da ordem #{self.id_selecionado}")
        suc, res = self.ordem_servico_peca_controller.listar_pecas_da_ordem(self.id_selecionado)
        if suc:
            for p in res: self._lista_pecas_local[p.id] = {"nome": p.nome, "quantidade": p.quantidade_os, "valor_unitario": p.valor_unitario_os}
        self._renderizar_tabela_pecas()

    def _preencher_valor_padrao_peca(self, e=None):
        if p := next((x for x in self.pecas_disp if x.id == self._extrair_id_combo(self.combo_peca_aba.get())), None):
            self.entry_valor_unitario_peca_aba.delete(0, tk.END); self.entry_valor_unitario_peca_aba.insert(0, f"{p.valor:.2f}")
            self.entry_quantidade_peca_aba.delete(0, tk.END); self.entry_quantidade_peca_aba.insert(0, "1")

    def _selecionar_peca_da_aba(self, e=None):
        if sel := self.tbl_pecas.selection(): self._selecionar_valor_combo(self.combo_peca_aba, sel[0])

    def _renderizar_tabela_pecas(self):
        self.tbl_pecas.delete(*self.tbl_pecas.get_children())
        total = 0.0
        for pid, data in self._lista_pecas_local.items():
            sub = float(data["quantidade"]) * float(data["valor_unitario"])
            total += sub
            self.tbl_pecas.insert("", tk.END, iid=str(pid), values=(data["nome"], data["quantidade"], f"{float(data['valor_unitario']):.2f}", f"{sub:.2f}"))
        self.lbl_total_pecas.config(text=f"Total peças: R$ {total:.2f}")

    def _adicionar_peca_na_lista(self):
        pid = self._extrair_id_combo(self.combo_peca_aba.get())
        if not pid: return messagebox.showwarning("Aviso", "Selecione uma peça.")
        try:
            self._lista_pecas_local[pid] = {
                "nome": self.combo_peca_aba.get().split(" - ", 1)[1],
                "quantidade": int(self.entry_quantidade_peca_aba.get()),
                "valor_unitario": float(self.entry_valor_unitario_peca_aba.get())
            }
            self._renderizar_tabela_pecas()
        except ValueError: messagebox.showerror("Erro", "Quantidade ou valor inválidos.")

    def _remover_peca_da_lista(self):
        if sel := self.tbl_pecas.selection():
            del self._lista_pecas_local[int(sel[0])]
            self._renderizar_tabela_pecas()

    def _salvar_pecas(self):
        itens = [{"peca_id": k, "quantidade": v["quantidade"], "valor_unitario": v["valor_unitario"]} for k, v in self._lista_pecas_local.items()]
        suc, res = self.ordem_servico_peca_controller.salvar_pecas_da_ordem(self.id_selecionado, itens)
        messagebox.showinfo("Sucesso", res) if suc else messagebox.showerror("Erro", res)

    # ------------------------------------------------------------------
    # UTILS INTERNOS 
    # ------------------------------------------------------------------
    
    def _extrair_id_combo(self, txt): return int(txt.split(" - ")[0]) if txt else None
    def _selecionar_valor_combo(self, cb, id_p): cb.set(next((v for v in cb["values"] if v.split(" - ")[0] == str(id_p)), ""))
    def _formatar_valor(self, v): return f"{float(v):.2f}" if v is not None else ""
    def _executar_operacao(self, op, msg):
        try:
            op(); messagebox.showinfo("Sucesso", msg); self._limpar_campos(); self._atualizar_treeview()
        except Exception as e: messagebox.showerror("Erro", str(e))