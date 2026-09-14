import tkinter as tk
from tkinter import ttk, messagebox

class Servico_View(tk.Frame):
    """
    Tela para gerenciar os serviços de uma Ordem de Serviço """

    def __init__(self, master, controller, servico_dao):
        super().__init__(master)
        self.controller = controller 
        self.servico_dao = servico_dao

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
        # Preenche o valor unitário automaticamente ao escolher o serviço
        self.combo_servico.bind("<<ComboboxSelected>>", self._preencher_valor_padrao)

        tk.Label(form, text="Valor Unitário:").grid(row=1, column=0, sticky="w")
        self.entry_valor_unitario = tk.Entry(form, width=10)
        self.entry_valor_unitario.grid(row=1, column=1, padx=5, sticky="w")
        