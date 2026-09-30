import tkinter as tk
from tkinter import ttk, messagebox

from app.core.idioma import t
from app.view.estilo_view import (
    COR_FUNDO_JANELA, CORES_MODULOS,
    configurar_janela, criar_cabecalho, criar_cartao, criar_label,
    criar_botao, estilizar_entry, aplicar_tema_widgets,
)


class Peca_View(tk.Frame):
    def __init__(self, master, peca_controller):
        super().__init__(master, bg=COR_FUNDO_JANELA)
        self.master = master
        self.controller = peca_controller  # Controller que faz as validações com o banco

        configurar_janela(self.master, t("Peças"))
        self._criar_widgets()
        self._carregar_lista()

        # Sem isso, o Frame nunca aparece dentro da janela (Toplevel fica em branco)
        self.pack(fill=tk.BOTH, expand=True)

    def _criar_widgets(self):
        """Monta o cabeçalho, o formulário (num cartão) e a lista de peças."""
        criar_cabecalho(
            self, t("Peças"), t("Estoque de peças utilizadas nos reparos"),
            cor_destaque=CORES_MODULOS.get("peca", CORES_MODULOS.get("pecas")),
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
        criar_label(form, t("ID:")).grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_id = tk.Entry(form, width=40, state="readonly")
        estilizar_entry(self.entry_id)
        self.entry_id.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Nome ---
        criar_label(form, t("Nome:")).grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_nome = tk.Entry(form, width=40)
        estilizar_entry(self.entry_nome)
        self.entry_nome.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Código ---
        criar_label(form, t("Código:")).grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_codigo = tk.Entry(form, width=40)
        estilizar_entry(self.entry_codigo)
        self.entry_codigo.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Quantidade em estoque ---
        criar_label(form, t("Quantidade em estoque:")).grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_quantidade = tk.Entry(form, width=40)
        estilizar_entry(self.entry_quantidade)
        self.entry_quantidade.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Preço de venda ---
        criar_label(form, t("Preço de venda (R$):")).grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_preco = tk.Entry(form, width=40)
        estilizar_entry(self.entry_preco)
        self.entry_preco.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Botões de ação, um do lado do outro na mesma linha ---
        frame_botoes = tk.Frame(form, bg=form["bg"])
        frame_botoes.grid(row=linha, column=0, columnspan=2, pady=(16, 0))

        criar_botao(frame_botoes, t("Salvar"), self._salvar).pack(side="left", padx=5)
        criar_botao(frame_botoes, t("Atualizar"), self._atualizar).pack(side="left", padx=5)
        criar_botao(frame_botoes, t("Excluir"), self._deletar, estilo="perigo").pack(side="left", padx=5)
        criar_botao(frame_botoes, t("Novo"), self._limpar_campos).pack(side="left", padx=5)

        # --- Lista de peças já cadastradas ---
        cartao_lista = criar_cartao(corpo)
        cartao_lista.pack(fill="both", expand=True)

        estilo_tabela = aplicar_tema_widgets()

        colunas = ("id", "nome", "codigo", "quantidade", "preco")
        self.tree = ttk.Treeview(cartao_lista, columns=colunas, show="headings", style=estilo_tabela)
        self.tree.heading("id", text=t("ID"))
        self.tree.heading("nome", text=t("Nome"))
        self.tree.heading("codigo", text=t("Código"))
        self.tree.heading("quantidade", text=t("Qtd. Estoque"))
        self.tree.heading("preco", text=t("Preço Venda"))

        self.tree.column("id", width=40)
        self.tree.column("nome", width=180)
        self.tree.column("codigo", width=110)
        self.tree.column("quantidade", width=100)
        self.tree.column("preco", width=100)

        self.tree.pack(fill="both", expand=True, side="left", padx=(16, 0), pady=16)

        scrollbar = ttk.Scrollbar(cartao_lista, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 16), pady=16)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self._selecionar_peca)

    def _carregar_lista(self):
        """Atualiza a Treeview com as peças cadastradas, vindas do Controller."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Atenção: PecaController.listar_todos() devolve a lista direto (sem tupla),
        # igual ao ServicoController.
        try:
            pecas = self.controller.listar_todos()
        except Exception as erro:
            messagebox.showerror(t("Erro"), f"{t('Erro ao buscar peças:')} {erro}")
            return

        for peca in pecas:
            self.tree.insert(
                "", "end",
                values=(
                    peca.id, peca.nome, peca.codigo,
                    peca.quantidade_estoque, peca.preco_venda,
                )
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

        self.entry_quantidade.delete(0, tk.END)
        self.entry_quantidade.insert(0, valores[3])

        self.entry_preco.delete(0, tk.END)
        self.entry_preco.insert(0, valores[4])

    def _set_id(self, valor):
        """Escreve (ou limpa) o campo ID mesmo ele estando readonly."""
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
            messagebox.showerror(t("Erro"), t("Nenhuma peça selecionada (ID vazio)."))
            return None
        try:
            return int(id_texto)
        except ValueError:
            messagebox.showerror(t("Erro"), t("O campo ID deve ser um número inteiro."))
            return None

    def _salvar(self):
        """Cadastra uma peça nova. O ID nunca vem do usuário: é gerado pelo banco."""
        sucesso, resultado = self.controller.cadastrar(
            nome=self.entry_nome.get(),
            codigo=self.entry_codigo.get(),
            quantidade_estoque=self.entry_quantidade.get(),
            preco_venda=self.entry_preco.get()
        )

        if sucesso:
            messagebox.showinfo(t("Sucesso"), t("Peça cadastrada com sucesso!"))
            self._limpar_campos()
            self._carregar_lista()
        else:
            # 'resultado' aqui é a mensagem de erro vinda do Controller
            messagebox.showerror(t("Erro"), resultado)

    def _atualizar(self):
        """Atualiza a peça do ID informado com os dados atuais dos campos."""
        id_peca = self._pegar_id()
        if id_peca is None:
            return

        sucesso, resultado = self.controller.atualizar(
            id=id_peca,
            nome=self.entry_nome.get(),
            codigo=self.entry_codigo.get(),
            quantidade_estoque=self.entry_quantidade.get(),
            preco_venda=self.entry_preco.get()
        )

        if sucesso:
            messagebox.showinfo(t("Sucesso"), resultado)
            self._limpar_campos()
            self._carregar_lista()
        else:
            messagebox.showerror(t("Erro"), resultado)

    def _deletar(self):
        """Exclui a peça do ID informado, pedindo confirmação antes."""
        id_peca = self._pegar_id()
        if id_peca is None:
            return

        confirmar = messagebox.askyesno(t("Confirmar"), t("Tem certeza que deseja excluir essa peça?"))
        if not confirmar:
            return

        sucesso, resultado = self.controller.excluir(id_peca)
        if sucesso:
            messagebox.showinfo(t("Sucesso"), resultado)
            self._limpar_campos()
            self._carregar_lista()
        else:
            messagebox.showerror(t("Erro"), resultado)

    def _limpar_campos(self):
        """Limpa todos os campos, incluindo o ID (usado pelo botão 'Novo')."""
        self._set_id(None)
        self.entry_nome.delete(0, tk.END)
        self.entry_codigo.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)