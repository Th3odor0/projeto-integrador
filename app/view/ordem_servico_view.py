import tkinter as tk
from tkinter import ttk, messagebox


class Ordem_servico_View(ttk.Frame):

    def __init__(
        self,
        master,
        controller_os,
        controller_servico_servico,
        dao_cliente,
        dao_funcionario,
        dao_equipamento,
        dao_servico,
        dao_peca
    ):
        super().__init__(master)
        self.master = master
        self.controller_os = controller_os
        self.controller_servico_servico = controller_servico_servico
        self.dao_cliente = dao_cliente
        self.dao_funcionario = dao_funcionario
        self.dao_equipamento = dao_equipamento
        self.dao_servico = dao_servico
        self.dao_peca = dao_peca

        self.os_selecionada_id = None

        # Exibe o frame principal na janela Toplevel
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._criar_layout()
        self._carregar_ordens_servico()

    def _criar_layout(self):
        # Frame Superior: Tabela de Ordens de Serviço
        frame_os = ttk.LabelFrame(self, text="Ordens de Serviço")
        frame_os.pack(fill=tk.BOTH, expand=True, pady=5)

        self.tree_os = ttk.Treeview(
            frame_os,
            columns=("id", "cliente", "equipamento", "funcionario", "status"),
            show="headings"
        )
        self.tree_os.heading("id", text="ID OS")
        self.tree_os.heading("cliente", text="Cliente")
        self.tree_os.heading("equipamento", text="Equipamento")
        self.tree_os.heading("funcionario", text="Técnico")
        self.tree_os.heading("status", text="Status")
        
        self.tree_os.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree_os.bind("<<TreeviewSelect>>", self._on_os_select)

        # Frame Inferior: Notebook com Abas de Detalhes
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        # Aba 1: Serviços Prestados
        self.tab_servicos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_servicos, text="Serviços Prestados")
        self._montar_aba_servicos(self.tab_servicos)

        # Aba 2: Peças Utilizadas
        self.tab_pecas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pecas, text="Peças Utilizadas")
        self._montar_aba_pecas(self.tab_pecas)

    def _montar_aba_servicos(self, parent):
        frame_form = ttk.Frame(parent)
        frame_form.pack(fill=tk.X, pady=5, padx=5)

        ttk.Label(frame_form, text="Serviço:").pack(side=tk.LEFT, padx=2)
        self.cb_servicos = ttk.Combobox(frame_form, state="readonly")
        self.cb_servicos.pack(side=tk.LEFT, padx=5)

        ttk.Label(frame_form, text="Valor (R$):").pack(side=tk.LEFT, padx=2)
        self.txt_valor_servico = ttk.Entry(frame_form, width=10)
        self.txt_valor_servico.pack(side=tk.LEFT, padx=5)

        btn_add = ttk.Button(frame_form, text="Adicionar Serviço", command=self._adicionar_servico)
        btn_add.pack(side=tk.LEFT, padx=5)

        self.tree_servicos = ttk.Treeview(
            parent,
            columns=("id", "nome", "valor"),
            show="headings"
        )
        self.tree_servicos.heading("id", text="ID")
        self.tree_servicos.heading("nome", text="Serviço")
        self.tree_servicos.heading("valor", text="Valor Cobrado")
        self.tree_servicos.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _montar_aba_pecas(self, parent):
        frame_form = ttk.Frame(parent)
        frame_form.pack(fill=tk.X, pady=5, padx=5)

        ttk.Label(frame_form, text="Peça:").pack(side=tk.LEFT, padx=2)
        self.cb_pecas = ttk.Combobox(frame_form, state="readonly")
        self.cb_pecas.pack(side=tk.LEFT, padx=5)

        ttk.Label(frame_form, text="Qtd:").pack(side=tk.LEFT, padx=2)
        self.txt_qtd_peca = ttk.Entry(frame_form, width=5)
        self.txt_qtd_peca.pack(side=tk.LEFT, padx=5)

        btn_add = ttk.Button(frame_form, text="Adicionar Peça", command=self._adicionar_peca)
        btn_add.pack(side=tk.LEFT, padx=5)

        self.tree_pecas = ttk.Treeview(
            parent,
            columns=("id", "nome", "qtd", "subtotal"),
            show="headings"
        )
        self.tree_pecas.heading("id", text="ID")
        self.tree_pecas.heading("nome", text="Peça")
        self.tree_pecas.heading("qtd", text="Qtd")
        self.tree_pecas.heading("subtotal", text="Subtotal")
        self.tree_pecas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _carregar_ordens_servico(self):
        for row in self.tree_os.get_children():
            self.tree_os.delete(row)
        
        # Chama a listagem do seu controller principal
        ordens = self.controller_os.listar_ordens() if hasattr(self.controller_os, 'listar_ordens') else []
        for os in ordens:
            self.tree_os.insert("", tk.END, values=(os.id, os.cliente_id, os.equipamento_id, os.funcionario_id, os.status))

    def _on_os_select(self, event):
        selecao = self.tree_os.selection()
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