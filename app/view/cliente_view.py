import tkinter as tk
from tkinter import messagebox


class Cliente_View(tk.Frame):
    def __init__(self, master, cliente_controller):
        super().__init__(master)
        self.master = master
        self.controller = cliente_controller

        self.master.title("Cadastro de Cliente")
        self._criar_widgets()

        self.pack(fill="both", expand=True)

    def _criar_widgets(self):
        linha = 0

        tk.Label(self, text="Nome:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_nome = tk.Entry(self, width=40)
        self.entry_nome.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        tk.Label(self, text="CPF:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_cpf = tk.Entry(self, width=40)
        self.entry_cpf.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        tk.Label(self, text="Telefone:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_telefone = tk.Entry(self, width=40)
        self.entry_telefone.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        tk.Label(self, text="Email:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_email = tk.Entry(self, width=40)
        self.entry_email.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        btn_salvar = tk.Button(self, text="Salvar", command=self._salvar)
        btn_salvar.grid(row=linha, column=0, columnspan=2, pady=15)

    def _salvar(self):
        sucesso, resultado = self.controller.cadastrar(
            nome=self.entry_nome.get(),
            cpf=self.entry_cpf.get(),
            telefone=self.entry_telefone.get(),
            email=self.entry_email.get()
        )

        if sucesso:
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self._limpar_campos()
        else:
            messagebox.showerror("Erro", resultado)

    def _limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)