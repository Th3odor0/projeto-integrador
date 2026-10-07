# TRADUÇÃO PT/EN: todos os textos mostrados ao usuário passam por t() (título, subtítulo, rótulos,
# cabeçalhos da tabela, botões e mensagens). As views filhas não precisam mudar: o texto em português
# delas já é a chave de tradução no idioma.py.
import traceback
import tkinter as tk
from tkinter import ttk, messagebox

from app.core.idioma import t  # TRADUÇÃO: import novo
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

    IMPORTANTE: 'chave' precisa ser, ao mesmo tempo,
      1) o nome de um atributo do model (usado com getattr para listar), e
      2) o nome de um parâmetro de controller.cadastrar / controller.atualizar.
    Se a chave não existir no model, a tela quebra ao carregar a lista.

    Um campo "combo" precisa de:
        chave:            atributo do objeto onde mora o valor relacionado
                           (pode guardar o objeto inteiro OU só o id — os dois
                           casos são tratados por _texto_combo)
        rotulo:           texto do label
        tipo:             "combo"
        carregar_opcoes:  função (self) -> lista de objetos disponíveis
        texto_opcao:      função (objeto) -> string mostrada no combobox e
                           na coluna da Treeview

    Ordem de Serviço NÃO herda daqui (3 combos + abas + sub-cadastros).
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
        self._objetos = {}  # iid da Treeview -> objeto do model

        configurar_janela(self.master, t(self.TITULO))  # TRADUÇÃO
        self._criar_widgets()
        # Empacota ANTES de carregar os dados: se o carregamento falhar, a
        # janela continua montada e o erro aparece na tela (não em branco).
        self.pack(fill=tk.BOTH, expand=True)
        try:
            self._carregar_opcoes_combos()
            self._carregar_lista()
        except Exception as erro:
            traceback.print_exc()
            messagebox.showerror(
                t("Erro ao carregar a tela"),  # TRADUÇÃO
                f"{type(erro).__name__}: {erro}",
                parent=self.master,
            )

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
            self, t(self.TITULO), t(self.SUBTITULO),  # TRADUÇÃO
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

        criar_label(form, t("ID:")).grid(row=0, column=0, sticky="w", padx=5, pady=6)  # TRADUÇÃO
        self.entry_id = tk.Entry(form, width=40, state="readonly")
        estilizar_entry(self.entry_id)
        self.entry_id.grid(row=0, column=1, padx=5, pady=6)

        campos = self._campos_normalizados
        for linha, campo in enumerate(campos, start=1):
            criar_label(form, t(campo["rotulo"])).grid(row=linha, column=0, sticky="w", padx=5, pady=6)  # TRADUÇÃO

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

        criar_botao(frame_botoes, t("Salvar"), self._salvar).pack(side="left", padx=5)  # TRADUÇÃO
        criar_botao(frame_botoes, t("Atualizar"), self._atualizar).pack(side="left", padx=5)  # TRADUÇÃO
        criar_botao(frame_botoes, t("Deletar"), self._excluir, estilo="perigo").pack(side="left", padx=5)  # TRADUÇÃO
        criar_botao(frame_botoes, t("Novo"), self._limpar_campos).pack(side="left", padx=5)  # TRADUÇÃO

    def _montar_lista(self, corpo):
        cartao_lista = criar_cartao(corpo)
        cartao_lista.pack(fill="both", expand=True)

        estilo_tabela = aplicar_tema_widgets()
        colunas = ["id"] + [c["chave"] for c in self._campos_normalizados]
        self.tree = ttk.Treeview(cartao_lista, columns=colunas, show="headings", style=estilo_tabela)

        self.tree.heading("id", text=t("ID"))  # TRADUÇÃO
        self.tree.column("id", width=40)
        for campo in self._campos_normalizados:
            # TRADUÇÃO: traduz o rótulo com os dois pontos (a chave existe no idioma.py) e tira os ":" depois
            self.tree.heading(campo["chave"], text=t(campo["rotulo"]).rstrip(":"))
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

    def _texto_combo(self, campo, bruto):
        """
        Texto do combo para o valor guardado no model. Aceita tanto o objeto
        relacionado (com .id) quanto só o id inteiro — o model Equipamento
        hoje guarda o id, mas o DAO pode devolver o objeto.
        """
        if bruto is None or bruto == "":
            return ""
        id_ref = getattr(bruto, "id", bruto)
        for opcao in self._opcoes_combo.get(campo["chave"], {}).values():
            if opcao.id == id_ref:
                return campo["texto_opcao"](opcao)
        return ""

    # ------------------------------------------------------------------
    # Dados <-> formulário
    # ------------------------------------------------------------------

    def _selecionar(self, event):
        # Lê do objeto guardado (e não dos valores da Treeview): o Tkinter
        # converte "01234567890" em número e perderia o zero à esquerda do
        # CPF / código.
        objeto = self._objetos.get(self.tree.focus())
        if objeto is None:
            return

        self._set_id(objeto.id)
        for campo in self._campos_normalizados:
            bruto = getattr(objeto, campo["chave"], None)
            if campo["tipo"] == "combo":
                self.combos[campo["chave"]].set(self._texto_combo(campo, bruto))
            else:
                entry = self.entradas[campo["chave"]]
                entry.delete(0, tk.END)
                entry.insert(0, "" if bruto is None else str(bruto))

    def _set_id(self, valor):
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        if valor is not None:
            self.entry_id.insert(0, str(valor))
        self.entry_id.config(state="readonly")

    def _pegar_id(self):
        id_texto = self.entry_id.get()
        if not id_texto.strip():
            messagebox.showerror(t("Erro"), t("Nenhum registro selecionado (ID vazio)."))  # TRADUÇÃO
            return None
        try:
            return int(id_texto)
        except ValueError:
            messagebox.showerror(t("Erro"), t("O campo ID deve ser um número inteiro."))  # TRADUÇÃO
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
        self.tree.delete(*self.tree.get_children())
        self._objetos.clear()

        sucesso, resultado = self.controller.buscar_todos()
        if not sucesso:
            messagebox.showerror(t("Erro"), resultado)  # TRADUÇÃO
            return

        campos = self._campos_normalizados
        for objeto in resultado:
            valores = [objeto.id]
            for campo in campos:
                bruto = getattr(objeto, campo["chave"])
                if campo["tipo"] == "combo":
                    valores.append(self._texto_combo(campo, bruto))
                else:
                    valores.append("" if bruto is None else bruto)
            iid = str(objeto.id)
            self._objetos[iid] = objeto
            self.tree.insert("", "end", iid=iid, values=valores)

    def _salvar(self):
        sucesso, resultado = self.controller.cadastrar(**self._coletar_campos())
        self._tratar_resultado(sucesso, resultado, t("Cadastrado com sucesso."))  # TRADUÇÃO

    def _atualizar(self):
        id_atual = self._pegar_id()
        if id_atual is None:
            return
        sucesso, resultado = self.controller.atualizar(id_atual, **self._coletar_campos())
        self._tratar_resultado(sucesso, resultado, t("Atualizado com sucesso."))  # TRADUÇÃO

    def _excluir(self):
        id_atual = self._pegar_id()
        if id_atual is None:
            return
        if not messagebox.askyesno(t("Confirmar"), t("Tem certeza que deseja excluir esse registro?")):  # TRADUÇÃO
            return
        sucesso, resultado = self.controller.excluir(id_atual)
        self._tratar_resultado(sucesso, resultado, t("Excluído com sucesso."))  # TRADUÇÃO

    def _tratar_resultado(self, sucesso, resultado, mensagem_padrao):
        if sucesso:
            texto = resultado if isinstance(resultado, str) else mensagem_padrao
            messagebox.showinfo(t("Sucesso"), texto)  # TRADUÇÃO
            self._limpar_campos()
            self._carregar_lista()
            self._carregar_opcoes_combos()
        else:
            messagebox.showerror(t("Erro"), resultado)  # TRADUÇÃO