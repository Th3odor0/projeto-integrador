import tkinter as tk
from tkinter import ttk, messagebox


class Ordem_servico_Servico_View(tk.Frame):
    """
    Tela para gerenciar os serviços prestados em uma Ordem de Serviço específica.
    Segue o mesmo padrão da Cliente_view: campo ID readonly preenchido pelo
    sistema, botões Salvar/Atualizar/Deletar/Novo, e uma lista com scrollbar.
    Precisa saber o id da ordem de serviço (ordem_servico_id) para funcionar.
    """

    def __init__(self, master, ordem_servico_id, controller, servico_dao):
        super().__init__(master)
        self.master = master
        self.ordem_servico_id = ordem_servico_id
        self.controller = controller     # Ordem_servico_Servico_Controller
        self.servico_dao = servico_dao   # usado só para listar serviços no combobox

        self._id_servico_por_item = {}   # id do vínculo -> id do serviço (pra reselecionar no combo)

        self.master.title("Serviços da Ordem de Serviço")
        self._criar_widgets()
        self._carregar_combo_servicos()
        self._carregar_lista()

        # Sem isso, o Frame nunca aparece dentro do Toplevel (janela fica em branco)
        self.pack(fill=tk.BOTH, expand=True)

    def _criar_widgets(self):
        """Monta os campos de entrada, os botões e a lista da tela."""
        linha = 0

        # --- Campo ID (somente leitura: só é preenchido automaticamente pelo sistema) ---
        tk.Label(self, text="ID:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_id = tk.Entry(self, width=40, state="readonly")
        self.entry_id.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Campo Serviço ---
        tk.Label(self, text="Serviço:").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.combo_servico = ttk.Combobox(self, state="readonly", width=38)
        self.combo_servico.grid(row=linha, column=1, padx=5, pady=5)
        # Preenche o valor cobrado automaticamente ao escolher o serviço
        self.combo_servico.bind("<<ComboboxSelected>>", self._preencher_valor_padrao)
        linha += 1

        # --- Campo Valor cobrado ---
        tk.Label(self, text="Valor cobrado (R$):").grid(row=linha, column=0, sticky="w", padx=5, pady=5)
        self.entry_valor_cobrado = tk.Entry(self, width=40)
        self.entry_valor_cobrado.grid(row=linha, column=1, padx=5, pady=5)
        linha += 1

        # --- Botões de ação, um do lado do outro na mesma linha ---
        frame_botoes = tk.Frame(self)
        frame_botoes.grid(row=linha, column=0, columnspan=2, pady=10)
        linha += 1

        tk.Button(frame_botoes, text="Salvar", command=self._salvar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Atualizar", command=self._atualizar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Deletar", command=self._deletar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Novo", command=self._limpar_campos).pack(side="left", padx=5)

        # --- Lista de serviços já adicionados ---
        frame_lista = tk.Frame(self)
        frame_lista.grid(row=linha, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))

        # Deixa a lista esticar quando a janela for redimensionada
        self.grid_rowconfigure(linha, weight=1)
        self.grid_columnconfigure(1, weight=1)

        colunas = ("id", "servico", "valor_cobrado")
        self.tree = ttk.Treeview(frame_lista, columns=colunas, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("servico", text="Serviço")
        self.tree.heading("valor_cobrado", text="Valor Cobrado")

        self.tree.column("id", width=40)
        self.tree.column("servico", width=200)
        self.tree.column("valor_cobrado", width=100)

        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self._selecionar_item)

    # ---------- carregamento de dados ----------

    def _carregar_combo_servicos(self):
        """Busca todos os serviços do banco e guarda numa lista, pra usar no combobox e no preenchimento automático."""
        self.servicos_disponiveis = self.servico_dao.get_all()
        self.combo_servico["values"] = [f"{s.id} - {s.nome}" for s in self.servicos_disponiveis]

    def _carregar_lista(self):
        """Atualiza a Treeview com os serviços já vinculados a essa ordem de serviço."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._id_servico_por_item.clear()

        sucesso, resultado = self.controller.buscar_por_ordem(self.ordem_servico_id)
        if not sucesso:
            messagebox.showerror("Erro", resultado)
            return

        for item in resultado:
            iid = str(item.id)
            self.tree.insert(
                "", "end", iid=iid,
                values=(item.id, item.servico.nome, f"{item.valor_cobrado:.2f}")
            )
            self._id_servico_por_item[iid] = item.id_servico

    # ---------- seleção ----------

    def _selecionar_item(self, event):
        """Ao clicar numa linha da lista, carrega os dados no formulário (inclusive o ID)."""
        selecionado = self.tree.focus()
        if not selecionado:
            return

        valores = self.tree.item(selecionado, "values")
        if not valores:
            return

        self._set_id(valores[0])

        # Reconstrói o texto do combobox ("3 - Nome") a partir do id_servico salvo,
        # já que o combobox readonly não guarda id, só o texto exibido.
        id_servico = self._id_servico_por_item.get(selecionado)
        texto_combo = next(
            (v for v in self.combo_servico["values"] if v.split(" - ")[0] == str(id_servico)), ""
        )
        self.combo_servico.config(state="readonly")
        self.combo_servico.set(texto_combo)
        # O serviço vinculado não muda depois de criado — só o valor cobrado é editável
        self.combo_servico.config(state="disabled")

        self.entry_valor_cobrado.delete(0, tk.END)
        self.entry_valor_cobrado.insert(0, valores[2])

    def _set_id(self, valor):
        """
        Escreve (ou limpa) o campo ID mesmo ele estando readonly.
        Usado pelo próprio sistema: depois de salvar (mostra o ID gerado pelo MySQL),
        ao selecionar um item na lista, ou ao limpar o formulário.
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
        (quem chamar essa função só precisa checar 'if id_item is None: return').
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

    # ---------- ações do usuário ----------

    def _preencher_valor_padrao(self, event):
        """Ao selecionar um serviço, sugere o valor padrão cadastrado (usuário pode editar depois)."""
        if not self.combo_servico.get():
            return
        servico_id = int(self.combo_servico.get().split(" - ")[0])
        servico = next(s for s in self.servicos_disponiveis if s.id == servico_id)

        self.entry_valor_cobrado.delete(0, tk.END)
        self.entry_valor_cobrado.insert(0, f"{servico.valor_padrao:.2f}")

    def _salvar(self):
        """Vincula um novo serviço a essa ordem. O ID nunca vem do usuário: é gerado pelo banco."""
        if not self.combo_servico.get():
            messagebox.showerror("Erro", "Selecione um serviço.")
            return

        servico_id = int(self.combo_servico.get().split(" - ")[0])

        sucesso, resultado = self.controller.cadastrar(
            ordem_servico_id=self.ordem_servico_id,
            servico_id=servico_id,
            valor_cobrado=self.entry_valor_cobrado.get()
        )

        if sucesso:
            messagebox.showinfo("Sucesso", "Serviço adicionado com sucesso!")
            self._limpar_campos()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", resultado)

    def _atualizar(self):
        """Atualiza o valor cobrado do item selecionado (o serviço vinculado não muda)."""
        id_item = self._pegar_id()
        if id_item is None:
            return

        sucesso, resultado = self.controller.atualizar(
            id=id_item,
            valor_cobrado=self.entry_valor_cobrado.get()
        )

        if sucesso:
            messagebox.showinfo("Sucesso", resultado)
            self._limpar_campos()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", resultado)

    def _deletar(self):
        """Remove o serviço do ID informado, pedindo confirmação antes."""
        id_item = self._pegar_id()
        if id_item is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar", "Tem certeza que deseja remover esse serviço da ordem?"
        )
        if not confirmar:
            return

        sucesso, resultado = self.controller.deletar(id_item)
        if sucesso:
            messagebox.showinfo("Sucesso", resultado)
            self._limpar_campos()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", resultado)

    def _limpar_campos(self):
        """Limpa todos os campos, incluindo o ID (usado pelo botão 'Novo')."""
        self._set_id(None)
        self.combo_servico.config(state="readonly")
        self.combo_servico.set("")
        self.entry_valor_cobrado.delete(0, tk.END)