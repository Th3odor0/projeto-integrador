import tkinter as tk
from tkinter import ttk, messagebox


class Ordem_servico_Peca_View(tk.Frame):
    """
    Tela para gerenciar as peças utilizadas em uma Ordem de Serviço específica.
    Precisa saber o id da ordem de serviço (ordem_servico_id) para funcionar.
    """

    def __init__(self, master, ordem_servico_id, controller, peca_dao):
        super().__init__(master)
        self.ordem_servico_id = ordem_servico_id
        self.controller = controller   # Ordem_servico_Peca_Controller
        self.peca_dao = peca_dao       # usado só para listar peças no combobox

        self._criar_widgets()
        self._carregar_combo_pecas()
        self._atualizar_lista()

    # ---------- construção da tela ----------

    def _criar_widgets(self):
        # --- Formulário de adição ---
        form = tk.Frame(self)
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Peça:").grid(row=0, column=0, sticky="w")
        self.combo_peca = ttk.Combobox(form, state="readonly", width=35)
        self.combo_peca.grid(row=0, column=1, padx=5)
        # Preenche o valor unitário automaticamente ao escolher a peça
        self.combo_peca.bind("<<ComboboxSelected>>", self._preencher_valor_padrao)

        tk.Label(form, text="Quantidade:").grid(row=1, column=0, sticky="w")
        self.entry_quantidade = tk.Entry(form, width=10)
        self.entry_quantidade.grid(row=1, column=1, sticky="w", padx=5)

        tk.Label(form, text="Valor unitário (R$):").grid(row=2, column=0, sticky="w")
        self.entry_valor_unitario = tk.Entry(form, width=10)
        self.entry_valor_unitario.grid(row=2, column=1, sticky="w", padx=5)

        tk.Button(form, text="Adicionar peça", command=self._adicionar).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # --- Lista de peças já adicionadas ---
        colunas = ("id", "peca", "quantidade", "valor_unitario", "subtotal")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=8)

        for coluna, titulo in zip(colunas, ["ID", "Peça", "Qtd", "Valor Unit.", "Subtotal"]):
            self.tabela.heading(coluna, text=titulo)

        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(self, text="Remover peça selecionada", command=self._remover).pack(pady=5)

    # ---------- carregamento de dados ----------

    def _carregar_combo_pecas(self):
        """Busca todas as peças do banco e guarda numa lista, pra depois usar no combobox e no subtotal."""
        self.pecas_disponiveis = self.peca_dao.get_all()
        self.combo_peca["values"] = [f"{p.id} - {p.nome}" for p in self.pecas_disponiveis]

    def _atualizar_lista(self):
        """Limpa e recarrega a Treeview com os itens já vinculados a essa ordem de serviço."""
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)

        itens = self.controller.listar_por_ordem(self.ordem_servico_id)
        for item in itens:
            subtotal = item.quantidade * item.valor_unitario
            self.tabela.insert("", tk.END, iid=item.id, values=(
                item.id, item.peca.nome, item.quantidade,
                f"{item.valor_unitario:.2f}", f"{subtotal:.2f}"
            ))

    # ---------- ações do usuário ----------

    def _preencher_valor_padrao(self, event):
        """Ao selecionar uma peça, sugere o preço de venda cadastrado (usuário pode editar depois)."""
        peca_id = int(self.combo_peca.get().split(" - ")[0])
        peca = next(p for p in self.pecas_disponiveis if p.id == peca_id)

        self.entry_valor_unitario.delete(0, tk.END)
        self.entry_valor_unitario.insert(0, f"{peca.preco_venda:.2f}")

    def _adicionar(self):
        try:
            if not self.combo_peca.get():
                messagebox.showerror("Erro", "Selecione uma peça.")
                return

            peca_id = int(self.combo_peca.get().split(" - ")[0])

            self.controller.adicionar(
                ordem_servico_id=self.ordem_servico_id,
                peca_id=peca_id,
                quantidade=self.entry_quantidade.get(),
                valor_unitario=self.entry_valor_unitario.get()
            )

            self._atualizar_lista()
            self._limpar_formulario()

        except ValueError as erro:
            messagebox.showerror("Erro de validação", str(erro))
        except Exception as erro:
            messagebox.showerror("Erro inesperado", str(erro))

    def _remover(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um item na lista para remover.")
            return

        item_id = int(selecionado[0])
        self.controller.remover(item_id)
        self._atualizar_lista()

    def _limpar_formulario(self):
        self.combo_peca.set("")
        self.entry_quantidade.delete(0, tk.END)
        self.entry_valor_unitario.delete(0, tk.END)