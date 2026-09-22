import tkinter as tk
from tkinter import ttk, messagebox

from app.view.estilo_view import (
    COR_FUNDO_JANELA, CORES_MODULOS,
    configurar_janela, criar_cabecalho, criar_cartao, criar_label,
    criar_botao, estilizar_entry, aplicar_tema_widgets,
)


class Funcionario_View(tk.Frame):
    def __init__(self, master, funcionario_controller):
        super().__init__(master, bg=COR_FUNDO_JANELA)
        self.master = master
        self.controller = funcionario_controller  # Controller que faz as validações com o banco

        configurar_janela(self.master, "Funcionários")
        self._criar_widgets()
        self._carregar_lista()

        # Sem isso, o Frame nunca aparece dentro da janela (Toplevel fica em branco)
        self.pack(fill=tk.BOTH, expand=True)

    def _criar_widgets(self):
        """Monta o cabeçalho, o formulário (num cartão) e a lista de funcionários."""
        criar_cabecalho(
            self, "Funcionários", "Equipe técnica e administrativa",
            cor_destaque=CORES_MODULOS["funcionario"],
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

        # --- CPF ---
        criar_label(form, "CPF:").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_cpf = tk.Entry(form, width=40)
        estilizar_entry(self.entry_cpf)
        self.entry_cpf.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Cargo ---
        criar_label(form, "Cargo:").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_cargo = tk.Entry(form, width=40)
        estilizar_entry(self.entry_cargo)
        self.entry_cargo.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Botões de ação, um do lado do outro na mesma linha ---
        frame_botoes = tk.Frame(form, bg=form["bg"])
        frame_botoes.grid(row=linha, column=0, columnspan=2, pady=(16, 0))

        criar_botao(frame_botoes, "Salvar", self._salvar).pack(side="left", padx=5)
        criar_botao(frame_botoes, "Atualizar", self._atualizar).pack(side="left", padx=5)
        criar_botao(frame_botoes, "Deletar", self._deletar, estilo="perigo").pack(side="left", padx=5)
        criar_botao(frame_botoes, "Novo", self._limpar_campos).pack(side="left", padx=5)

        # --- Lista de funcionários já cadastrados ---
        cartao_lista = criar_cartao(corpo)
        cartao_lista.pack(fill="both", expand=True)

        estilo_tabela = aplicar_tema_widgets()

        colunas = ("id", "nome", "cpf", "cargo")
        self.tree = ttk.Treeview(cartao_lista, columns=colunas, show="headings", style=estilo_tabela)
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("cargo", text="Cargo")

        self.tree.column("id", width=40)
        self.tree.column("nome", width=220)
        self.tree.column("cpf", width=130)
        self.tree.column("cargo", width=180)

        self.tree.pack(fill="both", expand=True, side="left", padx=(16, 0), pady=16)

        scrollbar = ttk.Scrollbar(cartao_lista, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 16), pady=16)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self._selecionar_funcionario)

    def _carregar_lista(self):
        """Atualiza a Treeview com os funcionários cadastrados, vindos do Controller."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        sucesso, resultado = self.controller.buscar_todos()
        if not sucesso:
            messagebox.showerror("Erro", resultado)
            return

        for funcionario in resultado:
            self.tree.insert(
                "", "end",
                values=(funcionario.id, funcionario.nome, funcionario.cpf, funcionario.cargo)
            )

    def _selecionar_funcionario(self, event):
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

        self.entry_cpf.delete(0, tk.END)
        self.entry_cpf.insert(0, valores[2])

        self.entry_cargo.delete(0, tk.END)
        self.entry_cargo.insert(0, valores[3])

    def _set_id(self, valor):
        """
        Escreve (ou limpa) o campo ID mesmo ele estando readonly.
        Usado pelo próprio sistema: depois de salvar (mostra o ID gerado pelo banco),
        ao selecionar um funcionário na lista, ou ao limpar o formulário.
        """
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        if valor is not None:
            self.entry_id.insert(0, str(valor))
        self.entry_id.config(state="readonly")

    def _pegar_id(self):
        """
        Lê o campo de ID e valida se é um número.
        Se estiver vazio ou inválido, já mostra o erro na tela e retorna None
        (quem chamar essa função só precisa checar 'if id_funcionario is None: return').
        """
        id_texto = self.entry_id.get()
        if not id_texto.strip():
            messagebox.showerror("Erro", "Nenhum funcionário selecionado (ID vazio).")
            return None
        try:
            return int(id_texto)
        except ValueError:
            messagebox.showerror("Erro", "O campo ID deve ser um número inteiro.")
            return None

    def _salvar(self):
        """Cadastra um funcionário novo. O ID nunca vem do usuário: é gerado pelo banco."""
        sucesso, resultado = self.controller.cadastrar(
            nome=self.entry_nome.get(),
            cpf=self.entry_cpf.get(),
            cargo=self.entry_cargo.get()
        )

        if sucesso:
            novo_id = resultado.id  # 'resultado' é o objeto Funcionario; o ID gerado está em .id
            messagebox.showinfo("Sucesso", f"Funcionário cadastrado com sucesso!")
            self._limpar_campos()
            self._carregar_lista()
        else:
            # 'resultado' aqui é a mensagem de erro vinda do Controller (validação ou CPF duplicado)
            messagebox.showerror("Erro", resultado)

    def _atualizar(self):
        """Atualiza o funcionário do ID informado com os dados atuais dos campos."""
        id_funcionario = self._pegar_id()
        if id_funcionario is None:
            return  # _pegar_id já mostrou o erro, só interrompe aqui

        sucesso, resultado = self.controller.atualizar(
            id=id_funcionario,
            nome=self.entry_nome.get(),
            cpf=self.entry_cpf.get(),
            cargo=self.entry_cargo.get()
        )

        if sucesso:
            messagebox.showinfo("Sucesso", resultado)
            self._limpar_campos()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", resultado)

    def _deletar(self):
        """Exclui o funcionário do ID informado, pedindo confirmação antes."""
        id_funcionario = self._pegar_id()
        if id_funcionario is None:
            return

        confirmar = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esse funcionário?")
        if not confirmar:
            return

        sucesso, resultado = self.controller.deletar(id_funcionario)
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
        self.entry_cpf.delete(0, tk.END)
        self.entry_cargo.delete(0, tk.END)