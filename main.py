# TRADUÇÃO PT/EN: título da janela e cartões do menu usam chaves do idioma.py (t()).
# Novo: _alternar_idioma() (troca PT <-> EN, fecha as telas abertas e remonta o menu), ligado ao botão 🌐 do menu.

# Coloque este arquivo na RAIZ do projeto (onde está o main.py atual), com o nome main.py.
import traceback
import tkinter as tk
from tkinter import messagebox

from app.core.database import Database
from app.core.idioma import t, carregar_idioma, idioma_atual  # TRADUÇÃO: + carregar_idioma/idioma_atual para trocar PT <-> EN
from app.view.estilo_view import COR_FUNDO_JANELA, CORES_MODULOS

# DAOs
from app.dao.cliente_dao import ClienteDAO
from app.dao.funcionario_dao import FuncionarioDAO
from app.dao.equipamento_dao import EquipamentoDAO
from app.dao.ordem_servico_dao import OrdemServicoDAO
from app.dao.ordem_servico_pecas_dao import OrdemServicoPecaDAO
from app.dao.peca_dao import PecaDAO
from app.dao.servico_dao import ServicoDAO
from app.dao.ordem_servico_servico_dao import Ordem_servico_Servico_Dao
# Controllers
from app.controller.ordem_servico_controller import Ordem_servico_Controller
from app.controller.cliente_controller import ClienteController
from app.controller.funcionario_controller import FuncionarioController
from app.controller.peca_controller import PecaController
from app.controller.servico_controller import ServicoController
from app.controller.equipamento_controller import EquipamentoController
from app.controller.ordem_servico_servico_controller import Ordem_servico_Servico_Controller
from app.controller.ordem_servico_pecas_controller import Ordem_Servico_Peca_Controller
# Views
from app.view.menu_view import MenuPrincipal
from app.view.ordem_servico_view import Ordem_servico_View
from app.view.cliente_view import Cliente_View
from app.view.equipamento_view import Equipamento_View
from app.view.funcionario_view import Funcionario_View
from app.view.servico_view import Servico_View
from app.view.peca_view import Peca_View


class ErpApplication:
    """
    Raiz da aplicação: conecta no banco, monta os DAOs e Controllers de cada
    módulo, mostra o menu principal e abre a janela de cada módulo quando o
    usuário clica no cartão dele.
    """

    def __init__(self):
        self._root = tk.Tk()
        self._root.withdraw()  # não mostra a janela vazia enquanto conecta
        # qualquer erro dentro de um botão/callback vira popup (e sai no terminal)
        self._root.report_callback_exception = self._mostrar_erro_inesperado

        try:
            self._database = Database()
        except Exception as erro:
            traceback.print_exc()
            messagebox.showerror(
                t("Banco de dados"),
                f"{t('Não foi possível conectar ao MySQL:')}\n\n{erro}",
                parent=self._root,
            )
            self._root.destroy()
            raise SystemExit(1)

        self._janelas = {}

        self._configurar_janela()
        self._montar_daos_e_controllers()
        self._criar_menu_principal()
        self._root.deiconify()

    @staticmethod
    def _mostrar_erro_inesperado(exc, valor, tb):
        traceback.print_exception(exc, valor, tb)
        messagebox.showerror(t("Erro inesperado"), f"{exc.__name__}: {valor}")

    def _configurar_janela(self):
        self._root.title(t("app.titulo"))  # TRADUÇÃO: título da janela principal
        self._root.configure(bg=COR_FUNDO_JANELA)
        try:
            self._root.state("zoomed")              # Windows
        except tk.TclError:
            try:
                self._root.attributes("-zoomed", True)  # Linux
            except tk.TclError:
                pass

    def _montar_daos_e_controllers(self):
        # DAOs independentes
        self._dao_cliente = ClienteDAO(self._database)
        self._dao_funcionario = FuncionarioDAO(self._database)
        self._dao_equipamento = EquipamentoDAO(self._database, self._dao_cliente)
        self._dao_peca = PecaDAO(self._database)
        self._dao_servico = ServicoDAO(self._database)
        self._dao_servico_servico = Ordem_servico_Servico_Dao(self._database)
        self._dao_ordem_servico_peca = OrdemServicoPecaDAO(self._database)

        # DAO principal, que depende dos DAOs acima
        self._dao_ordem_servico = OrdemServicoDAO(
            self._database, self._dao_cliente, self._dao_funcionario, self._dao_equipamento
        )

        # Controllers
        self._controller_ordem_servico = Ordem_servico_Controller(
            self._dao_ordem_servico, self._dao_cliente, self._dao_funcionario, self._dao_equipamento
        )
        self._controller_cliente = ClienteController(self._dao_cliente)
        self._controller_funcionario = FuncionarioController(self._dao_funcionario)
        self._controller_peca = PecaController(self._dao_peca)
        self._controller_servico = ServicoController(self._dao_servico)
        self._controller_equipamento = EquipamentoController(self._dao_equipamento, self._dao_cliente)
        self._controller_servico_servico = Ordem_servico_Servico_Controller(
            self._dao_servico_servico, self._dao_servico, self._dao_ordem_servico
        )
        self._controller_ordem_servico_peca = Ordem_Servico_Peca_Controller(
            self._dao_ordem_servico_peca, self._dao_peca, self._dao_ordem_servico
        )

    # ------------------------------------------------------------------
    # Menu principal
    # ------------------------------------------------------------------

    def _criar_menu_principal(self):
        cores = CORES_MODULOS  # mesma paleta das telas (antes estava repetida aqui)
        modulos = [  # TRADUÇÃO: títulos/descrições trocados por chaves do idioma.py
            ("🧾", t("modulo.os.titulo"), t("modulo.os.descricao"),
             self._abrir_ordem_servico, cores["ordem_servico"]),
            ("👤", t("modulo.cliente.titulo"), t("modulo.cliente.descricao"),
             self._abrir_cliente, cores["cliente"]),
            ("👷", t("modulo.funcionario.titulo"), t("modulo.funcionario.descricao"),
             self._abrir_funcionario, cores["funcionario"]),
            ("💻", t("modulo.equipamento.titulo"), t("modulo.equipamento.descricao"),
             self._abrir_equipamento, cores["equipamento"]),
            ("🔧", t("modulo.servico.titulo"), t("modulo.servico.descricao"),
             self._abrir_servico, cores["servico"]),
            ("🔩", t("modulo.peca.titulo"), t("modulo.peca.descricao"),
             self._abrir_peca, cores["peca"]),
        ]
        self._menu = MenuPrincipal(self._root, modulos, self._root.destroy, self._alternar_idioma)  # TRADUÇÃO: guarda o menu e passa o comando de idioma

    def _alternar_idioma(self):
        """Troca PT <-> EN: fecha as telas abertas (só leem t() ao serem criadas) e remonta o menu."""
        carregar_idioma("en" if idioma_atual() == "pt" else "pt")
        for janela in self._janelas.values():
            if janela.winfo_exists():
                janela.destroy()
        self._janelas.clear()
        self._menu.destroy()
        self._root.title(t("app.titulo"))
        self._criar_menu_principal()

    # ------------------------------------------------------------------
    # Abertura das telas (janelas Toplevel)
    # ------------------------------------------------------------------

    def _abrir_janela(self, chave, view_class, *args):
        """
        Abre a view numa Toplevel nova, ou traz pra frente a que já está aberta.
        Se a construção da view falhar, a janela quebrada é fechada e o erro
        aparece num popup (antes ficava uma janela vazia e o erro só no terminal).
        """
        janela = self._janelas.get(chave)
        if janela is not None and janela.winfo_exists():
            janela.lift()
            janela.focus_force()
            return

        janela = tk.Toplevel(self._root)
        try:
            view_class(janela, *args)
        except Exception as erro:
            traceback.print_exc()
            janela.destroy()
            messagebox.showerror(
                t("Erro ao abrir a tela"),
                f"{type(erro).__name__}: {erro}",
                parent=self._root,
            )
            return
        self._janelas[chave] = janela

    def _abrir_ordem_servico(self):
        self._abrir_janela(
            "ordem_servico", Ordem_servico_View,
            self._controller_ordem_servico, self._dao_cliente, self._dao_funcionario,
            self._dao_equipamento, self._controller_servico_servico, self._dao_servico,
            self._controller_ordem_servico_peca, self._dao_peca,
        )

    def _abrir_cliente(self):
        self._abrir_janela("cliente", Cliente_View, self._controller_cliente)

    def _abrir_funcionario(self):
        self._abrir_janela("funcionario", Funcionario_View, self._controller_funcionario)

    def _abrir_equipamento(self):
        self._abrir_janela(
            "equipamento", Equipamento_View, self._controller_equipamento, self._dao_cliente
        )

    def _abrir_servico(self):
        self._abrir_janela("servico", Servico_View, self._controller_servico)

    def _abrir_peca(self):
        self._abrir_janela("peca", Peca_View, self._controller_peca)

    def run(self):
        self._root.mainloop()


if __name__ == "__main__":
    app = ErpApplication()
    app.run()