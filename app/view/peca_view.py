import tkinter as tk
from tkinter import ttk, messagebox

from app.view.estilo_view import (
    COR_FUNDO_JANELA, CORES_MODULOS,
    configurar_janela, criar_cabecalho, criar_cartao, criar_label,
    criar_botao, estilizar_entry, aplicar_tema_widgets,
)


class Peca_View(tk.Frame):
    def __init__(self, master, peca_controller):
        super().__init__(master, bg=COR_FUNDO_JANELA)
        self.master = master
        self.controller = peca_controller  # Controller que faz as validações e fala com o banco

        configurar_janela(self.master, "Peças")
        self._criar_widgets()
        self._carregar_lista()

        # Sem isso, o Frame nunca aparece dentro da janela (Toplevel fica em branco)
        self.pack(fill=tk.BOTH, expand=True)

    def _criar_widgets(self):
        """Monta o cabeçalho, o formulário (num cartão) e a lista de peças."""
        criar_cabecalho(
            self, "Peças", "Estoque de peças utilizadas nos reparos",
            cor_destaque=CORES_MODULOS["peca"],
        )

        corpo = tk.Frame(self, bg=COR_FUNDO_JANELA)
        corpo.pack(fill="both", expand=True, padx=30, pady=(0, 24))

        # --- Cartão do formulário ---
        cartao_form = criar_cartao(corpo)
        cartao_form.pack(fill="x", pady=(0, 20))

        form = tk.Frame(cartao_form, bg=cartao_form["bg"])
        form.pack(fill="x", padx=24, pady=20)

        linha = 0

        # --- Campo ID (somente leitura: preenchido pelo sistema, nunca digitado) ---
        criar_label(form, "ID:").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_id = tk.Entry(form, width=40, state="readonly")
        estilizar_entry(self.entry_id)
        self.entry_id.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Nome ---
        criar_label(form, "Nome:").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_nome = tk.Entry(form, width=40)
        estilizar_entry(self.entry_nome)
        self.entry_nome.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Código ---
        criar_label(form, "Código:").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_codigo = tk.Entry(form, width=40)
        estilizar_entry(self.entry_codigo)
        self.entry_codigo.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Quantidade em estoque ---
        criar_label(form, "Quantidade em estoque:").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_quantidade_estoque = tk.Entry(form, width=40)
        estilizar_entry(self.entry_quantidade_estoque)
        self.entry_quantidade_estoque.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Preço de venda ---
        criar_label(form, "Preço de venda (R$):").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_preco_venda = tk.Entry(form, width=40)
        estilizar_entry(self.entry_preco_venda)
        self.entry_preco_venda.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Botões de ação ---
        frame_botoes = tk.Frame(form, bg=form["bg"])
        frame_botoes.grid(row=linha, column=0, columnspan=2, pady=(16, 0))

        criar_botao(frame_botoes, "Salvar", self._salvar).pack(side="left", padx=5)
        criar_botao(frame_botoes, "Atualizar", self._atualizar).pack(side="left", padx=5)
        criar_botao(frame_botoes, "Excluir", self._excluir, estilo="perigo").pack(side="left", padx=5)
        criar_botao(frame_botoes, "Novo", self._limpar_campos).pack(side="left", padx=5)

        # --- Lista de peças já cadastradas ---
        cartao_lista = criar_cartao(corpo)
        cartao_lista.pack(fill="both", expand=True)

        estilo_tabela = aplicar_tema_widgets()

        colunas = ("id", "nome", "codigo", "quantidade_estoque", "preco_venda")
        self.tree = ttk.Treeview(cartao_lista, columns=colunas, show="headings", style=estilo_tabela)
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("quantidade_estoque", text="Qtd. Estoque")
        self.tree.heading("preco_venda", text="Preço Venda")

        self.tree.column("id", width=40)
        self.tree.column("nome", width=200)
        self.tree.column("codigo", width=110)
        self.tree.column("quantidade_estoque", width=110)
        self.tree.column("preco_venda", width=110)

        self.tree.pack(fill="both", expand=True, side="left", padx=(16, 0), pady=16)

        scrollbar = ttk.Scrollbar(cartao_lista, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 16), pady=16)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self._selecionar_peca)

    def _carregar_lista(self):
        """
        Atualiza a Treeview com as peças cadastradas.
        Atenção: PecaController.listar_todos() devolve a lista direto (sem tupla),
        diferente do ClienteController.buscar_todos(), que devolve (sucesso, lista).
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            pecas = self.controller.listar_todos()
        except Exception as erro:
            messagebox.showerror("Erro", f"Erro ao buscar peças: {erro}")
            return

        for peca in pecas:
            self.tree.insert(
                "", "end",
                values=(peca.id, peca.nome, peca.codigo, peca.quantidade_estoque, peca.preco_venda)
            )

    def _selecionar_peca(self, event):
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

        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, valores[2])

        self.entry_quantidade_estoque.delete(0, tk.END)
        self.entry_quantidade_estoque.insert(0, valores[3])

        self.entry_preco_venda.delete(0, tk.END)
        self.entry_preco_venda.insert(0, valores[4])

    def _set_id(self, valor):
        """
        Escreve (ou limpa) o campo ID mesmo ele estando readonly.
        Usado pelo próprio sistema: depois de salvar (mostra o ID gerado pelo banco),
        ao selecionar uma peça na lista, ou ao limpar o formulário.
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
            messagebox.showerror("Erro", "Nenhuma peça selecionada (ID vazio).")
            return None
        try:
            return int(id_texto)
        except ValueError:
            messagebox.showerror("Erro", "O campo ID deve ser um número inteiro.")
            return None

    def _salvar(self):
        """Cadastra uma peça nova. O ID nunca vem do usuário: é gerado pelo banco."""
        sucesso, resultado = self.controller.cadastrar(
            nome=self.entry_nome.get(),
            codigo=self.entry_codigo.get(),
            quantidade_estoque=self.entry_quantidade_estoque.get(),
            preco_venda=self.entry_preco_venda.get()
        )

        if sucesso:
            novo_id = resultado.id  # 'resultado' é o objeto Peca; o ID gerado está em .id
            messagebox.showinfo("Sucesso", f"Peça cadastrada com sucesso!")
            self._limpar_campos()
            self._carregar_lista()
        else:
            # 'resultado' aqui é a mensagem de erro vinda do Controller
            messagebox.showerror("Erro", resultado)

    def _atualizar(self):
        """Atualiza a peça do ID informado com os dados atuais dos campos."""
        id_peca = self._pegar_id()
        if id_peca is None:
            return

        sucesso, resultado = self.controller.atualizar(
            id=id_peca,
            nome=self.entry_nome.get(),
            codigo=self.entry_codigo.get(),
            quantidade_estoque=self.entry_quantidade_estoque.get(),
            preco_venda=self.entry_preco_venda.get()
        )

        if sucesso:
            messagebox.showinfo("Sucesso", resultado)
            self._limpar_campos()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", resultado)

    def _excluir(self):
        """Exclui a peça do ID informado, pedindo confirmação antes."""
        id_peca = self._pegar_id()
        if id_peca is None:
            return

        confirmar = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir essa peça?")
        if not confirmar:
            return

        sucesso, resultado = self.controller.excluir(id_peca)
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
        self.entry_codigo.delete(0, tk.END)
        self.entry_quantidade_estoque.delete(0, tk.END)
        self.entry_preco_venda.delete(0, tk.END)