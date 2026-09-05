import tkinter as tk
from app.core.database import Database
from app.dao.ordem_servico_dao import OrdemServicoDAO
from app.view.ordem_servico_view import OrdemServicoView

class ErpApplication:
    def __init__(self):
        self._database = Database()
        self._ordem_servico_dao = OrdemServicoDAO(self._database)
        
        self._root = tk.Tk()
        self._root.title("Sistema ERP - Assistência Técnica")
        self._root.geometry("800x600")

        # Passa a DAO para a View, e não a conexão do banco bruta
        self._janela_ordem_servico = OrdemServicoView(self._root, self._ordem_servico_dao)

    def run(self):
        self._root.mainloop()

if __name__ == "__main__":
    app = ErpApplication()
    app.run()