import tkinter as tk
from tkinter import ttk, messagebox

from app.view.estilo_view import (
    COR_FUNDO_JANELA, CORES_MODULOS,
    configurar_janela, criar_cabecalho, criar_cartao, criar_label,
    criar_botao, estilizar_entry, aplicar_tema_widgets,
)


class Servico_View(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg=COR_FUNDO_JANELA)
        self.master = master
        self.controller = controller  # Controller que faz as validações e fala com o banco

        configurar_janela(self.master, "Serviços")
        self._criar_widgets()
        self._carregar_lista()

        # Sem isso, o Frame nunca aparece dentro da janela (Toplevel fica em branco)
        self.pack(fill=tk.BOTH, expand=True)

    def _criar_widgets(self):
        """Monta o cabeçalho, o formulário (num cartão) e a lista de serviços."""
        criar_cabecalho(
            self, "Serviços", "Catálogo de serviços prestados pela oficina",
            cor_destaque=CORES_MODULOS["servico"],
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

        # --- Descrição ---
        criar_label(form, "Descrição:").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_descricao = tk.Entry(form, width=40)
        estilizar_entry(self.entry_descricao)
        self.entry_descricao.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Valor padrão ---
        criar_label(form, "Valor padrão (R$):").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_valor_padrao = tk.Entry(form, width=40)
        estilizar_entry(self.entry_valor_padrao)
        self.entry_valor_padrao.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Botões de ação ---
        frame_botoes = tk.Frame(form, bg=form["bg"])
        frame_botoes.grid(row=linha, column=0, columnspan=2, pady=(16, 0))

        criar_botao(frame_botoes, "Salvar", self._salvar).pack(side="left", padx=5)
        criar_botao(frame_botoes, "Atualizar", self._atualizar).pack(side="left", padx=5)
        criar_botao(frame_botoes, "Excluir", self._excluir, estilo="perigo").pack(side="left", padx=5)
        criar_botao(frame_botoes, "Novo", self._limpar_campos).pack(side="left", padx=5)

        # --- Lista de serviços já cadastrados ---
        cartao_lista = criar_cartao(corpo)
        cartao_lista.pack(fill="both", expand=True)

        estilo_tabela = aplicar_tema_widgets()

        colunas = ("id", "nome", "descricao", "valor_padrao")
        self.tree = ttk.Treeview(cartao_lista, columns=colunas, show="headings", style=estilo_tabela)
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("valor_padrao", text="Valor Padrão")

        self.tree.column("id", width=40)
        self.tree.column("nome", width=180)
        self.tree.column("descricao", width=250)
        self.tree.column("valor_padrao", width=110)

        self.tree.pack(fill="both", expand=True, side="left", padx=(16, 0), pady=16)

        scrollbar = ttk.Scrollbar(cartao_lista, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 16), pady=16)
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