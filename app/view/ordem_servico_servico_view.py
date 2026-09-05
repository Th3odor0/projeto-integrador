import tkinter as tk
from tkinter import ttk, messagebox


class Ordem_servico_Servico_View(tk.Frame):
    """
    Tela para gerenciar os serviços prestados em uma Ordem de Serviço específica.
    Precisa saber o id da ordem de serviço (ordem_servico_id) para funcionar.
    """

    def __init__(self, master, ordem_servico_id, controller, servico_dao):
        super().__init__(master)
        self.ordem_servico_id = ordem_servico_id
        self.controller = controller     # Ordem_servico_Servico_Controller
        self.servico_dao = servico_dao   # usado só para listar serviços no combobox

        self._criar_widgets()
        self._carregar_combo_servicos()
        self._atualizar_lista()

    # ---------- construção da tela ----------

    def _criar_widgets(self):
        # --- Formulário de adição ---
        form = tk.Frame(self)
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Serviço:").grid(row=0, column=0, sticky="w")
        self.combo_servico = ttk.Combobox(form, state="readonly", width=35)
        self.combo_servico.grid(row=0, column=1, padx=5)
        # Preenche o valor cobrado automaticamente ao escolher o serviço
        self.combo_servico.bind("<<ComboboxSelected>>", self._preencher_valor_padrao)

        tk.Label(form, text="Valor cobrado (R$):").grid(row=1, column=0, sticky="w")
        self.entry_valor_cobrado = tk.Entry(form, width=10)
        self.entry_valor_cobrado.grid(row=1, column=1, sticky="w", padx=5)

        tk.Button(form, text="Adicionar serviço", command=self._adicionar).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        # --- Lista de serviços já adicionados ---
        colunas = ("id", "servico", "valor_cobrado")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=8)

        for coluna, titulo in zip(colunas, ["ID", "Serviço", "Valor Cobrado"]):
            self.tabela.heading(coluna, text=titulo)

        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(self, text="Remover serviço selecionado", command=self._remover).pack(pady=5)

    # ---------- carregamento de dados ----------

    def _carregar_combo_servicos(self):
        """Busca todos os serviços do banco e guarda numa lista, pra usar no combobox e no preenchimento automático."""
        self.servicos_disponiveis = self.servico_dao.get_all()
        self.combo_servico["values"] = [f"{s.id} - {s.nome}" for s in self.servicos_disponiveis]

    def _atualizar_lista(self):
        """Limpa e recarrega a Treeview com os serviços já vinculados a essa ordem de serviço."""
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)

        itens = self.controller.listar_por_ordem(self.ordem_servico_id)
        for item in itens:
            self.tabela.insert("", tk.END, iid=item.id, values=(
                item.id, item.servico.nome, f"{item.valor_cobrado:.2f}"
            ))

    # ---------- ações do usuário ----------

    def _preencher_valor_padrao(self, event):
        """Ao selecionar um serviço, sugere o valor padrão cadastrado (usuário pode editar depois)."""
        servico_id = int(self.combo_servico.get().split(" - ")[0])
        servico = next(s for s in self.servicos_disponiveis if s.id == servico_id)

        self.entry_valor_cobrado.delete(0, tk.END)
        self.entry_valor_cobrado.insert(0, f"{servico.valor_padrao:.2f}")

    def _adicionar(self):
        try:
            if not self.combo_servico.get():
                messagebox.showerror("Erro", "Selecione um serviço.")
                return

            servico_id = int(self.combo_servico.get().split(" - ")[0])

            self.controller.adicionar(
                ordem_servico_id=self.ordem_servico_id,
                servico_id=servico_id,
                valor_cobrado=self.entry_valor_cobrado.get()
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
        self.combo_servico.set("")
        self.entry_valor_cobrado.delete(0, tk.END)