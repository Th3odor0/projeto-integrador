import tkinter as tk
from tkinter import ttk, messagebox


class Ordem_servico_View(tk.Frame):
    def __init__(self, master, ordem_servico_controller, cliente_dao, funcionario_dao, equipamento_dao):
        super().__init__(master)
        self.master = master
        self.controller = ordem_servico_controller

        # DAOs usados só para popular os comboboxes (listar clientes, funcionários, equipamentos)
        self.cliente_dao = cliente_dao
        self.funcionario_dao = funcionario_dao
        self.equipamento_dao = equipamento_dao

        self.master.title("Cadastro de Ordem de Serviço")
        self._criar_widgets()
        self._carregar_combos()

        # Sem isso, o Frame nunca aparece dentro do Toplevel (janela fica em branco)
        self.pack(fill="both", expand=True)

    def _criar_widgets(self):
        linha = 0

        # --- Cliente ---
        tk.Label(self, text="Cliente:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.combo_cliente = ttk.Combobox(self, state="readonly", width=40)
        self.combo_cliente.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Funcionário ---
        tk.Label(self, text="Funcionário:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.combo_funcionario = ttk.Combobox(self, state="readonly", width=40)
        self.combo_funcionario.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Equipamento ---
        tk.Label(self, text="Equipamento:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.combo_equipamento = ttk.Combobox(self, state="readonly", width=40)
        self.combo_equipamento.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Data de entrada ---
        tk.Label(self, text="Data de entrada (dd/mm/aaaa):").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_data_entrada = tk.Entry(self, width=42)
        self.entry_data_entrada.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Data de conclusão (opcional) ---
        tk.Label(self, text="Data de conclusão (opcional):").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_data_conclusao = tk.Entry(self, width=42)
        self.entry_data_conclusao.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Status ---
        tk.Label(self, text="Status:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.combo_status = ttk.Combobox(
            self, state="readonly", width=40,
            values=["aberta", "em andamento", "concluida", "cancelada"]
        )
        self.combo_status.grid(row=linha, column=1, padx=5, pady=5)
        self.combo_status.current(0)
        linha += 1

        # --- Problema ---
        tk.Label(self, text="Problema:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_problema = tk.Entry(self, width=42)
        self.entry_problema.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Diagnóstico ---
        tk.Label(self, text="Diagnóstico:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_diagnostico = tk.Entry(self, width=42)
        self.entry_diagnostico.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Valor total ---
        tk.Label(self, text="Valor total (R$):").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_valor_total = tk.Entry(self, width=42)
        self.entry_valor_total.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Forma de pagamento ---
        tk.Label(self, text="Forma de pagamento:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_forma_pagamento = tk.Entry(self, width=42)
        self.entry_forma_pagamento.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Dias de garantia ---
        tk.Label(self, text="Dias de garantia:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_dias_garantia = tk.Entry(self, width=42)
        self.entry_dias_garantia.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Botão de salvar ---
        btn_salvar = tk.Button(self, text="Salvar", command=self._salvar)
        btn_salvar.grid(row=linha, column=0, columnspan=2, pady=15)

    def _carregar_combos(self):
        """Popula os comboboxes com dados vindos do banco via DAO."""
        clientes = self.cliente_dao.get_all()
        self.combo_cliente["values"] = [f"{c.id} - {c.nome}" for c in clientes]

        funcionarios = self.funcionario_dao.get_all()
        self.combo_funcionario["values"] = [f"{f.id} - {f.nome}" for f in funcionarios]

        equipamentos = self.equipamento_dao.get_all()
        self.combo_equipamento["values"] = [f"{e.id} - {e.tipo} {e.marca} {e.modelo}" for e in equipamentos]

    def _extrair_id_do_combo(self, texto_combo):
        """Extrai o id numérico do texto '3 - Nome do Cliente' -> 3"""
        if not texto_combo:
            return None
        return int(texto_combo.split(" - ")[0])

    def _salvar(self):
        try:
            id_cliente = self._extrair_id_do_combo(self.combo_cliente.get())
            id_funcionario = self._extrair_id_do_combo(self.combo_funcionario.get())
            id_equipamento = self._extrair_id_do_combo(self.combo_equipamento.get())

            if id_cliente is None or id_funcionario is None or id_equipamento is None:
                messagebox.showerror("Erro", "Selecione cliente, funcionário e equipamento.")
                return

            self.controller.cadastrar(
                id_cliente=id_cliente,
                id_funcionario=id_funcionario,
                id_equipamento=id_equipamento,
                data_entrada_texto=self.entry_data_entrada.get(),
                data_conclusao_texto=self.entry_data_conclusao.get(),
                status=self.combo_status.get(),
                problema=self.entry_problema.get(),
                diagnostico=self.entry_diagnostico.get(),
                valor_total=self.entry_valor_total.get(),
                forma_pagamento=self.entry_forma_pagamento.get(),
                dias_garantia=self.entry_dias_garantia.get()
            )

            messagebox.showinfo("Sucesso", "Ordem de serviço cadastrada com sucesso!")
            self._limpar_campos()

        except ValueError as erro:
            # Erros de validação (data inválida, valor inválido, entidade não encontrada etc.)
            messagebox.showerror("Erro de validação", str(erro))

        except Exception as erro:
            # Qualquer outro erro inesperado (ex: falha de conexão com banco)
            messagebox.showerror("Erro inesperado", f"Ocorreu um erro: {erro}")

    def _limpar_campos(self):
        self.combo_cliente.set("")
        self.combo_funcionario.set("")
        self.combo_equipamento.set("")
        self.entry_data_entrada.delete(0, tk.END)
        self.entry_data_conclusao.delete(0, tk.END)
        self.combo_status.current(0)
        self.entry_problema.delete(0, tk.END)
        self.entry_diagnostico.delete(0, tk.END)
        self.entry_valor_total.delete(0, tk.END)
        self.entry_forma_pagamento.delete(0, tk.END)
        self.entry_dias_garantia.delete(0, tk.END)