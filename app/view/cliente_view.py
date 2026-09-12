import tkinter as tk
from tkinter import messagebox

class Cliente_view(tk.Frame):
    def __init__(self, master, cliente_controller):
        super().__init__(master)
        self.master = master
        self.controller = cliente_controller #Controller que faz as validações com o banco

        self.master.title("Cadastro de Clientes")
        self._criar_widgets()

        #Sem isso, o Frame nunca aparece dentro da janela (Toplevel fica em branco)
        self.pack(fill=tk.BOTH, expand=True)

    def _criar_widgets(self):
        """Monta todos os campos de entrada e os botões da tela."""
        linha = 0

        # --- Campo ID (usando só pra localizar o cliente ao atualizar/excluir) ---
        tk.Label(self, text="ID (para atualizar/excluir):").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_id = tk.Entry(self, width=40)
        self.entry_id.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Campo Nome ---
        tk.Label(self, text="Nome:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_nome = tk.Entry(self, width=40)
        self.entry_nome.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Campo CPF ---
        tk.Label(self, text="CPF:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_cpf = tk.Entry(self, width=40)
        self.entry_cpf.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Campo Telefone ---
        tk.Label(self, text="Telefone:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_telefone = tk.Entry(self, width=40)
        self.entry_telefone.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Campo Email ---
        tk.Label(self, text="Email:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_email = tk.Entry(self, width=40)
        self.entry_email.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Botões de ação, um do lado do outro na mesma linha ---
        frame_botoes = tk.Frame(self)
        frame_botoes.grid(row=linha, column=0, columnspan=2, pady=10)

        tk.Button(frame_botoes, text="Salvar", command=self._salvar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Atualizar", command=self._atualizar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Deletar", command=self._deletar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Novo", command=self._limpar_campos).pack(side="left", padx=5)

    def _pegar_id(self):
        """
        Lê o campo de ID e valida se é um número.
        Se estiver vazio ou inválido, já mostra o erro na tela e retorna None
        (quem chamar essa funcção só precisa checar 'if id_cliente is None: return').
        """
        id_texto = self.entry_id.get()
        if not id_texto.strip():
            messagebox.showerror("Erro", "O campo ID não pode estar vazio.")
            return None
        try:
            return int(id_texto)
        except ValueError:
            messagebox.showerror("Erro", "O campo ID deve ser um número inteiro.")
            return None
        
    def _salvar(self):
        """Cadastra um cliente novo. O campo ID é ignorado aqui de propósito"""
        sucesso, resultado = self.constroller.cadastrar(
            nome=self.entry_nome.get(),
            cpf=self.entry_cpf.get(),
            telefone=self.entry_telefone.get(),
            email=self.entry_email.get()
        )

        if sucesso:
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self._limpar_campos()
        else:
            # 'resultado' aqui é a mensagem de erro vinda do Controller (validação ou CPF duplicado)
            messagebox.showerror("Erro", resultado)


    def _atualizar(self):
        """Atualiza o cliente do ID informado com os dados atuais dos campos"""
        id_cliente = self._pegar_id()
        if id_cliente is None:
            return # _pegar_id já mostrou o erro, só interrompe aqui
        
        sucesso, resultado = self.controller.atualizar(
            id=id_cliente,
            nome=self.entry_nome.get(),
            cpf=self.entry_cpf.get(),
            telefone=self.entry_telefone.get(),
            email=self.entry_email.get()
        )

        if sucesso:
            messagebox.showinfo("Sucesso", resultado)
            self._limpar_campos()
        else:
            messagebox.showerror("Erro", resultado)

    def _deletar(self):
        """Deletar o cliente do ID informado, pedindo confirmação antes."""
        id_cliente = self._pegar_id()
        if id_cliente is None:
            return
        
        confirmar = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esse cliente?")
        if not confirmar:
            return
        
        sucesso, resultado = self.controller.deletar(id_cliente)
        if sucesso:
            messagebox.showinfo("Sucesso", resultado)
            self._limpar_campos()
        else:
            messagebox.showerror("Erro", resultado)

    def _limpar_campos(self):
        """"Limpa todos os campos, incluindo o ID (usado pelo botão 'Novo')"""
        self.entry_id.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)