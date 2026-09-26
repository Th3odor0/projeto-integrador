import tkinter as tk
from tkinter import ttk, messagebox

from app.view.estilo_view import (
    COR_FUNDO_JANELA, CORES_MODULOS,
    configurar_janela, criar_cabecalho, criar_cartao, criar_label,
    criar_botao, estilizar_entry, aplicar_tema_widgets,
)


class CrudViewBase(tk.Frame):
    """
    Esqueleto genérico para telas de cadastro simples.

    Cada item de CAMPOS pode ser:
      - uma tupla (chave, rotulo)                          -> campo de texto
      - um dict com chave/rotulo/tipo="combo"/...          -> campo relacional

    Um campo "combo" precisa de:
        chave:            atributo do objeto onde mora o valor relacionado
                           (ex.: "id_cliente" -- no seu Equipamento, esse
                           atributo já guarda o objeto Cliente inteiro)
        rotulo:           texto do label
        tipo:             "combo"
        carregar_opcoes:  função (self) -> lista de objetos disponíveis
                           (ex.: lambda self: self.cliente_dao.get_all())
        texto_opcao:      função (objeto) -> string mostrada no combobox e
                           na coluna da Treeview (ex.: lambda c: f"{c.id} - {c.nome}")

    Isso já cobre UM campo relacional (o caso do Equipamento). Duas ou mais
    comboboxes interdependentes, abas, ou sub-cadastro dentro da mesma tela
    (o caso da Ordem de Serviço) não devem tentar caber aqui -- ver o
    comentário no fim do arquivo.
    """

    TITULO = ""
    SUBTITULO = ""
    MODULO = ""
    CAMPOS = []
    COLUNAS_LARGURA = {}

    def __init__(self, master, controller):
        super().__init__(master, bg=COR_FUNDO_JANELA)
        self.master = master
        self.controller = controller
        self.entradas = {}
        self.combos = {}
        self._opcoes_combo = {}

        configurar_janela(self.master, self.TITULO)
        self._criar_widgets()
        self._carregar_opcoes_combos()
        self._carregar_lista()
        self.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    # Normalização dos campos (texto vs. combo)
    # ------------------------------------------------------------------

    @staticmethod
    def _normalizar_campo(campo):
        if isinstance(campo, dict):
            campo.setdefault("tipo", "combo")
            return campo
        chave, rotulo = campo
        return {"chave": chave, "rotulo": rotulo, "tipo": "texto"}

    @property
    def _campos_normalizados(self):
        return [self._normalizar_campo(c) for c in self.CAMPOS]

    # ------------------------------------------------------------------
    # Montagem da tela
    # ------------------------------------------------------------------

    def _criar_widgets(self):
        criar_cabecalho(
            self, self.TITULO, self.SUBTITULO,
            cor_destaque=CORES_MODULOS[self.MODULO],
        )

        corpo = tk.Frame(self, bg=COR_FUNDO_JANELA)
        corpo.pack(fill="both", expand=True, padx=30, pady=(0, 24))

        self._montar_formulario(corpo)
        self._montar_lista(corpo)

    def _montar_formulario(self, corpo):
        cartao_form = criar_cartao(corpo)
        cartao_form.pack(fill="x", pady=(0, 20))

        form = tk.Frame(cartao_form, bg=cartao_form["bg"])
        form.pack(fill="x", padx=24, pady=20)

        criar_label(form, "ID:").grid(row=0, column=0, sticky="w", padx=5, pady=6)
        self.entry_id = tk.Entry(form, width=40, state="readonly")
        estilizar_entry(self.entry_id)
        self.entry_id.grid(row=0, column=1, padx=5, pady=6)

        campos = self._campos_normalizados
        for linha, campo in enumerate(campos, start=1):
            criar_label(form, campo["rotulo"]).grid(row=linha, column=0, sticky="w", padx=5, pady=6)

            if campo["tipo"] == "combo":
                combo = ttk.Combobox(form, state="readonly", width=38)
                combo.grid(row=linha, column=1, padx=5, pady=6)
                self.combos[campo["chave"]] = combo
            else:
                entry = tk.Entry(form, width=40)
                estilizar_entry(entry)
                entry.grid(row=linha, column=1, padx=5, pady=6)
                self.entradas[campo["chave"]] = entry

        frame_botoes = tk.Frame(form, bg=form["bg"])
        frame_botoes.grid(row=len(campos) + 1, column=0, columnspan=2, pady=(16, 0))

        criar_botao(frame_botoes, "Salvar", self._salvar).pack(side="left", padx=5)
        criar_botao(frame_botoes, "Atualizar", self._atualizar).pack(side="left", padx=5)
        criar_botao(frame_botoes, "Deletar", self._excluir, estilo="perigo").pack(side="left", padx=5)
        criar_botao(frame_botoes, "Novo", self._limpar_campos).pack(side="left", padx=5)

    def _montar_lista(self, corpo):
        cartao_lista = criar_cartao(corpo)
        cartao_lista.pack(fill="both", expand=True)

        estilo_tabela = aplicar_tema_widgets()
        colunas = ["id"] + [c["chave"] for c in self._campos_normalizados]
        self.tree = ttk.Treeview(cartao_lista, columns=colunas, show="headings", style=estilo_tabela)

        self.tree.heading("id", text="ID")
        self.tree.column("id", width=40)
        for campo in self._campos_normalizados:
            self.tree.heading(campo["chave"], text=campo["rotulo"].rstrip(":"))
            self.tree.column(campo["chave"], width=self.COLUNAS_LARGURA.get(campo["chave"], 140))

        self.tree.pack(fill="both", expand=True, side="left", padx=(16, 0), pady=16)

        scrollbar = ttk.Scrollbar(cartao_lista, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 16), pady=16)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self._selecionar)

    # ------------------------------------------------------------------
    # Opções das comboboxes
    # ------------------------------------------------------------------

    def _carregar_opcoes_combos(self):
        for campo in self._campos_normalizados:
            if campo["tipo"] != "combo":
                continue
            opcoes = campo["carregar_opcoes"](self)
            textos = [campo["texto_opcao"](opcao) for opcao in opcoes]
            self._opcoes_combo[campo["chave"]] = dict(zip(textos, opcoes))
            self.combos[campo["chave"]]["values"] = textos

    # ------------------------------------------------------------------
    # Dados <-> formulário
    # ------------------------------------------------------------------

    def _selecionar(self, event):
        selecionado = self.tree.focus()
        if not selecionado:
            return
        valores = self.tree.item(selecionado, "values")
        if not valores:
            return

        self._set_id(valores[0])
        campos = self._campos_normalizados
        for campo, valor in zip(campos, valores[1:]):
            if campo["tipo"] == "combo":
                self.combos[campo["chave"]].set(valor)
            else:
                entry = self.entradas[campo["chave"]]
                entry.delete(0, tk.END)
                entry.insert(0, valor)

    def _set_id(self, valor):
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        if valor is not None:
            self.entry_id.insert(0, str(valor))
        self.entry_id.config(state="readonly")

    def _pegar_id(self):
        id_texto = self.entry_id.get()
        if not id_texto.strip():
            messagebox.showerror("Erro", "Nenhum registro selecionado (ID vazio).")
            return None
        try:
            return int(id_texto)
        except ValueError:
            messagebox.showerror("Erro", "O campo ID deve ser um número inteiro.")
            return None

    def _coletar_campos(self):
        dados = {chave: entry.get() for chave, entry in self.entradas.items()}
        for chave, combo in self.combos.items():
            objeto_selecionado = self._opcoes_combo.get(chave, {}).get(combo.get())
            dados[chave] = objeto_selecionado.id if objeto_selecionado else None
        return dados

    def _limpar_campos(self):
        self._set_id(None)
        for entry in self.entradas.values():
            entry.delete(0, tk.END)
        for combo in self.combos.values():
            combo.set("")

    # ------------------------------------------------------------------
    # Ações (Salvar / Atualizar / Excluir / Listar)
    # ------------------------------------------------------------------

    def _carregar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        sucesso, resultado = self.controller.buscar_todos()
        if not sucesso:
            messagebox.showerror("Erro", resultado)
            return

        campos = self._campos_normalizados
        for objeto in resultado:
            valores = [objeto.id]
            for campo in campos:
                bruto = getattr(objeto, campo["chave"])
                if campo["tipo"] == "combo":
                    valores.append(campo["texto_opcao"](bruto) if bruto else "")
                else:
                    valores.append(bruto)
            self.tree.insert("", "end", values=valores)

    def _salvar(self):
        sucesso, resultado = self.controller.cadastrar(**self._coletar_campos())
        self._tratar_resultado(sucesso, resultado, "Cadastrado com sucesso.")

    def _atualizar(self):
        id_atual = self._pegar_id()
        if id_atual is None:
            return
        sucesso, resultado = self.controller.atualizar(id_atual, **self._coletar_campos())
        self._tratar_resultado(sucesso, resultado, "Atualizado com sucesso.")

    def _excluir(self):
        id_atual = self._pegar_id()
        if id_atual is None:
            return
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esse registro?"):
            return
        sucesso, resultado = self.controller.excluir(id_atual)
        self._tratar_resultado(sucesso, resultado, "Excluído com sucesso.")

    def _tratar_resultado(self, sucesso, resultado, mensagem_padrao):
        if sucesso:
            texto = resultado if isinstance(resultado, str) else mensagem_padrao
            messagebox.showinfo("Sucesso", texto)
            self._limpar_campos()
            self._carregar_lista()
            self._carregar_opcoes_combos()
        else:
            messagebox.showerror("Erro", resultado)

# Sobre Ordem de Serviço: propositalmente NÃO herda daqui. Teria 3 comboboxes
# (cliente/funcionário/equipamento) + abas de Serviços/Peças com sub-cadastro
# embutido + total calculado -- forçar isso aqui tornaria a base tão cheia de
# casos especiais quanto a view dedicada que já existe, só que mais confusa.