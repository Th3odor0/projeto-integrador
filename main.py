from app.core.database import Database

from app.view.ordem_servico_view import Ordem_servico_View
from app.dao.ordem_servico_dao import Ordem_servico_DAO

class ErpAplication:
    def __init__(self):

        init(autoreset=True)

        self._database = Database()

        self._root = tk.Tk()

        self._janela_ordem_servico = Ordem_servico_View(self._root, self._database)