import tkinter as tk
from tkinter import ttk, messagebox

from app.view.estilo_view import (
    COR_FUNDO_JANELA, CORES_MODULOS,
    configurar_janela, criar_cabecalho, criar_cartao, criar_label,
    criar_botao, estilizar_entry, aplicar_tema_widgets,
)


class Equipamento_View(tk.Frame):
    def __init__(self, master, equipamento_controller, cliente_dao):
        super().__init__(master, bg=COR_FUNDO_JANELA)
        self.master = master
        self.controller = equipamento_controller
        self.cliente_dao = cliente_dao  # usado só para popular o combobox de clientes

        configurar_janela(self.master, "Equipamentos")
        self._criar_widgets()
        self._carregar_combo_cliente()
        self._carregar_lista()

        # Sem isso, o Frame nunca aparece dentro da janela (Toplevel fica em branco)
        self.pack(fill=tk.BOTH, expand=True)

    def _criar_widgets(self):
        """Monta o cabeçalho, o formulário (num cartão) e a lista de equipamentos."""
        criar_cabecalho(
            self, "Equipamentos", "Aparelhos recebidos para reparo",
            cor_destaque=CORES_MODULOS["equipamento"],
        )

        estilo_tabela = aplicar_tema_widgets()  # também deixa o Combobox abaixo no tema certo

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

        # --- Cliente ---
        criar_label(form, "Cliente:").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.combo_cliente = ttk.Combobox(form, state="readonly", width=38)
        self.combo_cliente.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Tipo ---
        criar_label(form, "Tipo:").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_tipo = tk.Entry(form, width=40)
        estilizar_entry(self.entry_tipo)
        self.entry_tipo.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Marca ---
        criar_label(form, "Marca:").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_marca = tk.Entry(form, width=40)
        estilizar_entry(self.entry_marca)
        self.entry_marca.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Modelo ---
        criar_label(form, "Modelo:").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_modelo = tk.Entry(form, width=40)
        estilizar_entry(self.entry_modelo)
        self.entry_modelo.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Número de série ---
        criar_label(form, "Número de série:").grid(row=linha, column=0, sticky="w", padx=5, pady=6)
        self.entry_numero_serie = tk.Entry(form, width=40)
        estilizar_entry(self.entry_numero_serie)
        self.entry_numero_serie.grid(row=linha, column=1, padx=5, pady=6)
        linha += 1

        # --- Botões de ação ---
        frame_botoes = tk.Frame(form, bg=form["bg"])
        frame_botoes.grid(row=linha, column=0, columnspan=2, pady=(16, 0))

        criar_botao(frame_botoes, "Salvar", self._salvar).pack(side="left", padx=5)
        criar_botao(frame_botoes, "Atualizar", self._atualizar).pack(side="left", padx=5)
        criar_botao(frame_botoes, "Deletar", self._deletar, estilo="perigo").pack(side="left", padx=5)
        criar_botao(frame_botoes, "Novo", self._limpar_campos).pack(side="left", padx=5)

        # --- Lista de equipamentos já cadastrados ---
        cartao_lista = criar_cartao(corpo)
        cartao_lista.pack(fill="both", expand=True)

        # 'cliente_id' fica escondido (não aparece na tela, só em displaycolumns abaixo),
        # mas é guardado no values da linha pra dar pra reselecionar o combo certo depois.
        colunas = ("id", "tipo", "marca", "modelo", "numero_serie", "cliente_id", "cliente_nome")
        self.tree = ttk.Treeview(
            cartao_lista,
            columns=colunas,
            show="headings",
            displaycolumns=("id", "tipo", "marca", "modelo", "numero_serie", "cliente_nome"),
            style=estilo_tabela,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("marca", text="Marca")
        self.tree.heading("modelo", text="Modelo")
        self.tree.heading("numero_serie", text="Nº Série")
        self.tree.heading("cliente_nome", text="Cliente")

        self.tree.column("id", width=40)
        self.tree.column("tipo", width=100)
        self.tree.column("marca", width=100)
        self.tree.column("modelo", width=100)
        self.tree.column("numero_serie", width=100)
        self.tree.column("cliente_nome", width=160)

        self.tree.pack(fill="both", expand=True, side="left", padx=(16, 0), pady=16)

        scrollbar = ttk.Scrollbar(cartao_lista, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 16), pady=16)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self._selecionar_equipamento)

    def _carregar_combo_cliente(self):
        """Popula o combobox de clientes com dados vindos do banco via DAO."""
        self.combo_cliente["values"] = [f"{c.id} - {c.nome}" for c in self.cliente_dao.get_all()]

    def _carregar_lista(self):
        """Atualiza a Treeview com os equipamentos cadastrados, vindos do Controller."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for equipamento in self.controller.listar_todos():
            # equipamento.id_cliente pode vir como objeto Cliente ou como int puro
            cliente = equipamento.id_cliente
            cliente_id = getattr(cliente, "id", cliente)
            cliente_nome = getattr(cliente, "nome", cliente)

            self.tree.insert(
                "", "end",
                values=(
                    equipamento.id,
                    equipamento.tipo,
                    equipamento.marca,
                    equipamento.modelo,
                    equipamento.numero_serie,
                    cliente_id,
                    cliente_nome,
                )
            )

    def _selecionar_equipamento(self, event):
        """Ao clicar numa linha da lista, carrega os dados no formulário (inclusive o ID e o Cliente)."""
        selecionado = self.tree.focus()
        if not selecionado:
            return

        valores = self.tree.item(selecionado, "values")
        if not valores:
            return

        self._set_id(valores[0])

        self.entry_tipo.delete(0, tk.END)
        self.entry_tipo.insert(0, valores[1])

        self.entry_marca.delete(0, tk.END)
        self.entry_marca.insert(0, valores[2])

        self.entry_modelo.delete(0, tk.END)
        self.entry_modelo.insert(0, valores[3])

        self.entry_numero_serie.delete(0, tk.END)
        self.entry_numero_serie.insert(0, valores[4])

        self._selecionar_valor_combo(self.combo_cliente, valores[5])

    @staticmethod
    def _selecionar_valor_combo(combobox, id_procurado):
        """Seleciona no combobox o item cujo texto começa com 'id_procurado - '."""
        valor = next((v for v in combobox["values"] if v.split(" - ")[0] == str(id_procurado)), "")
        combobox.set(valor)

    @staticmethod
    def _extrair_id_do_combo(texto_combo):
        """Extrai o id numérico do texto '3 - Nome do Cliente' -> 3"""
        return int(texto_combo.split(" - ")[0]) if texto_combo else None

    def _set_id(self, valor):
        """
        Escreve (ou limpa) o campo ID mesmo ele estando readonly.
        Usado pelo próprio sistema: depois de salvar, ao selecionar um equipamento
        na lista, ou ao limpar o formulário.
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
            messagebox.showerror("Erro", "Nenhum equipamento selecionado (ID vazio).")
            return None
        try:
            return int(id_texto)
        except ValueError:
            messagebox.showerror("Erro", "O campo ID deve ser um número inteiro.")
            return None

    def _coletar_dados_formulario(self):
        """Lê os campos do formulário. Levanta ValueError se o cliente não foi selecionado."""
        id_cliente = self._extrair_id_do_combo(self.combo_cliente.get())
        if id_cliente is None:
            raise ValueError("Selecione um cliente.")

        return {
            "tipo": self.entry_tipo.get(),
            "marca": self.entry_marca.get(),
            "modelo": self.entry_modelo.get(),
            "numero_serie": self.entry_numero_serie.get(),
            "id_cliente": id_cliente,
        }

    def _salvar(self):
        """Cadastra um equipamento novo. O ID nunca vem do usuário: é gerado pelo banco."""
        try:
            dados = self._coletar_dados_formulario()
        except ValueError as erro:
            messagebox.showerror("Erro de validação", str(erro))
            return

        sucesso, resultado = self.controller.cadastrar(**dados)
        if sucesso:
            messagebox.showinfo("Sucesso", "Equipamento cadastrado com sucesso!")
            self._limpar_campos()
            self._carregar_lista()
        else:
            # 'resultado' aqui é a mensagem de erro vinda do Controller
            messagebox.showerror("Erro", resultado)

    def _atualizar(self):
        """Atualiza o equipamento do ID informado com os dados atuais dos campos."""
        id_equipamento = self._pegar_id()
        if id_equipamento is None:
            return

        try:
            dados = self._coletar_dados_formulario()
        except ValueError as erro:
            messagebox.showerror("Erro de validação", str(erro))
            return

        sucesso, resultado = self.controller.atualizar(id_equipamento, **dados)
        if sucesso:
            messagebox.showinfo("Sucesso", "Equipamento atualizado com sucesso!")
            self._limpar_campos()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", resultado)

    def _deletar(self):
        """Exclui o equipamento do ID informado, pedindo confirmação antes."""
        id_equipamento = self._pegar_id()
        if id_equipamento is None:
            return

        confirmar = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esse equipamento?")
        if not confirmar:
            return

        sucesso, resultado = self.controller.excluir(id_equipamento)
        if sucesso:
            messagebox.showinfo("Sucesso", "Equipamento excluído com sucesso!")
            self._limpar_campos()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", resultado)

    def _limpar_campos(self):
        """Limpa todos os campos, incluindo o ID (usado pelo botão 'Novo')."""
        self._set_id(None)
        self.combo_cliente.set("")
        self.entry_tipo.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_modelo.delete(0, tk.END)
        self.entry_numero_serie.delete(0, tk.END)