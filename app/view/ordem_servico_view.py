import tkinter as tk
from tkinter import ttk, messagebox

from app.view.ordem_servico_servico_view import Ordem_servico_Servico_View


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

    def __init__(self, master, ordem_servico_controller, cliente_dao, funcionario_dao,
                 equipamento_dao, controller_servico_servico, servico_dao):
        super().__init__(master)
        self.master = master
        self.controller = ordem_servico_controller
        self.cliente_dao = cliente_dao
        self.funcionario_dao = funcionario_dao
        self.equipamento_dao = equipamento_dao
        self.controller_servico_servico = controller_servico_servico
        self.dao_servico = servico_dao

        self.id_selecionado = None  # None = modo "novo cadastro"
        self.combos = {}            # chave -> Combobox
        self.entradas = {}          # chave -> Entry
        self._janela_servicos = None  # controla se a sub-tela de serviços já está aberta

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

    def _montar_aba_pecas(self, parent):
        frame_form = ttk.Frame(parent)
        frame_form.pack(fill=tk.X, pady=5, padx=5)

        botoes = [
            ("Novo", self._novo),
            ("Salvar", self._salvar),
            ("Alterar", self._alterar),
            ("Excluir", self._excluir),
            ("Serviços", self._abrir_servicos),
        ]
        for coluna, (texto, comando) in enumerate(botoes):
            tk.Button(frame_form, text=texto, width=15, command=comando).grid(row=0, column=coluna, padx=5)

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

        item = self.tree_os.item(selecao[0])
        self.os_selecionada_id = item["values"][0]
        self._carregar_servicos_os()

    def _carregar_servicos_os(self):
        for row in self.tree_servicos.get_children():
            self.tree_servicos.delete(row)

        if not self.os_selecionada_id:
            return

        if hasattr(self.controller_servico_servico, 'listar_por_ordem'):
            itens = self.controller_servico_servico.listar_por_ordem(self.os_selecionada_id)
            for item in itens:
                nome = getattr(item, 'servico', 'Serviço')
                self.tree_servicos.insert("", tk.END, values=(item.id, nome, item.valor_cobrado))

    def _adicionar_servico(self):
        if not self.os_selecionada_id:
            messagebox.showerror("Erro", "Selecione uma Ordem de Serviço primeiro.")
            return

    def _adicionar_peca(self):
        if not self.os_selecionada_id:
            messagebox.showerror("Erro", "Selecione uma Ordem de Serviço primeiro.")
            return

        self._executar_operacao(
            lambda: self.controller.excluir(self.id_selecionado),
            "Ordem de serviço excluída com sucesso!",
        )

    # ------------------------------------------------------------------
    # Sub-tela de Serviços Prestados
    # ------------------------------------------------------------------

    def _abrir_servicos(self):
        """Abre a tela de serviços prestados vinculada à ordem selecionada na lista."""
        if self.id_selecionado is None:
            self._exibir_mensagem(
                "Aviso", "Selecione uma ordem na lista para gerenciar os serviços.", sucesso=False
            )
            return

        if self._janela_servicos is not None and self._janela_servicos.winfo_exists():
            self._janela_servicos.lift()
            self._janela_servicos.focus_force()
            return

        janela = tk.Toplevel(self)
        self._janela_servicos = janela
        Ordem_servico_Servico_View(
            janela,
            self.id_selecionado,
            self.controller_servico_servico,
            self.dao_servico
        )