import tkinter as tk
from tkinter import ttk, messagebox


class Servico_View(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller  # Controller que faz as validações e fala com o banco

        self.master.title("Cadastro de Serviços")
        self._criar_widgets()
        self._carregar_lista()

        # Sem isso, o Frame nunca aparece dentro da janela (Toplevel fica em branco)
        self.pack(fill=tk.BOTH, expand=True)

    def _criar_widgets(self):
        """Monta os campos de entrada, os botões e a lista da tela."""
        linha = 0

        # --- Campo ID (somente leitura: preenchido pelo sistema, nunca digitado) ---
        tk.Label(self, text="ID:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_id = tk.Entry(self, width=40, state="readonly")
        self.entry_id.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Nome ---
        tk.Label(self, text="Nome:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_nome = tk.Entry(self, width=40)
        self.entry_nome.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Descrição ---
        tk.Label(self, text="Descrição:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_descricao = tk.Entry(self, width=40)
        self.entry_descricao.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Valor padrão ---
        tk.Label(self, text="Valor padrão (R$):").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_valor_padrao = tk.Entry(self, width=40)
        self.entry_valor_padrao.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Botões de ação ---
        frame_botoes = tk.Frame(self)
        frame_botoes.grid(row=linha, column=0, columnspan=2, pady=10)
        linha += 1

        tk.Button(frame_botoes, text="Salvar", command=self._salvar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Atualizar", command=self._atualizar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Excluir", command=self._excluir).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Novo", command=self._limpar_campos).pack(side="left", padx=5)

        # --- Lista de serviços já cadastrados ---
        frame_lista = tk.Frame(self)
        frame_lista.grid(row=linha, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))

        # Deixa a lista esticar quando a janela for redimensionada
        self.grid_rowconfigure(linha, weight=1)
        self.grid_columnconfigure(1, weight=1)

        colunas = ("id", "nome", "descricao", "valor_padrao")
        self.tree = ttk.Treeview(frame_lista, columns=colunas, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("valor_padrao", text="Valor Padrão")

        self.tree.column("id", width=40)
        self.tree.column("nome", width=180)
        self.tree.column("descricao", width=250)
        self.tree.column("valor_padrao", width=110)

        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self._selecionar_servico)

    def _carregar_lista(self):
        """
        Atualiza a Treeview com os serviços cadastrados.
        Atenção: o ServicoController.listar_todos() devolve a lista direto (sem tupla),
        diferente do ClienteController.buscar_todos(), que devolve (sucesso, lista).
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            servicos = self.controller.listar_todos()
        except Exception as erro:
            messagebox.showerror("Erro", f"Erro ao buscar serviços: {erro}")
            return

        for servico in servicos:
            self.tree.insert(
                "", "end",
                values=(servico.id, servico.nome, servico.descricao, servico.valor_padrao)
            )

    def _selecionar_servico(self, event):
        """Ao clicar numa linha da lista, carrega os dados no formulário (inclusive o ID)."""
        selecionado = self.tree.focus()
        if not selecionado:
            return

        valores = self.tree.item(selecionado, "values")
        if not valores:
            return

        self._set_id(valores[0])

        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, valores[1])

        self.entry_descricao.delete(0, tk.END)
        self.entry_descricao.insert(0, valores[2])

        self.entry_valor_padrao.delete(0, tk.END)
        self.entry_valor_padrao.insert(0, valores[3])

    def _set_id(self, valor):
        """
        Escreve (ou limpa) o campo ID mesmo ele estando readonly.
        Usado pelo próprio sistema: depois de salvar (mostra o ID gerado pelo banco),
        ao selecionar um serviço na lista, ou ao limpar o formulário.
        """
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        if valor is not None:
            self.entry_id.insert(0, str(valor))
        self.entry_id.config(state="readonly")

    def _pegar_id(self):
        """
        Lê o campo de ID e valida se é um número.
        Se estiver vazio ou inválido, já mostra o erro na tela e retorna None.
        """
        id_texto = self.entry_id.get()
        if not id_texto.strip():
            messagebox.showerror("Erro", "Nenhum serviço selecionado (ID vazio).")
            return None
        try:
            return int(id_texto)
        except ValueError:
            messagebox.showerror("Erro", "O campo ID deve ser um número inteiro.")
            return None

    def _salvar(self):
        """Cadastra um serviço novo. O ID nunca vem do usuário: é gerado pelo banco."""
        sucesso, resultado = self.controller.cadastrar(
            nome=self.entry_nome.get(),
            descricao=self.entry_descricao.get(),
            valor_padrao=self.entry_valor_padrao.get()
        )

        if sucesso:
            novo_id = resultado.id  # 'resultado' é o objeto Servico; o ID gerado está em .id
            messagebox.showinfo("Sucesso", f"Serviço cadastrado com sucesso!")
            self._limpar_campos()
            self._carregar_lista()
        else:
            # 'resultado' aqui é a mensagem de erro vinda do Controller
            messagebox.showerror("Erro", resultado)

    def _atualizar(self):
        """Atualiza o serviço do ID informado com os dados atuais dos campos."""
        id_servico = self._pegar_id()
        if id_servico is None:
            return

        sucesso, resultado = self.controller.atualizar(
            id=id_servico,
            nome=self.entry_nome.get(),
            descricao=self.entry_descricao.get(),
            valor_padrao=self.entry_valor_padrao.get()
        )

        if sucesso:
            messagebox.showinfo("Sucesso", resultado)
            self._limpar_campos()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", resultado)

    def _excluir(self):
        """Exclui o serviço do ID informado, pedindo confirmação antes."""
        id_servico = self._pegar_id()
        if id_servico is None:
            return

        confirmar = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esse serviço?")
        if not confirmar:
            return

        sucesso, resultado = self.controller.excluir(id_servico)
        if sucesso:
            messagebox.showinfo("Sucesso", resultado)
            self._limpar_campos()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", resultado)

    def _limpar_campos(self):
        """Limpa todos os campos, incluindo o ID (usado pelo botão 'Novo')."""
        self._set_id(None)
        self.entry_nome.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_valor_padrao.delete(0, tk.END)