#DAOs(parametro)
from app.dao.cliente_dao import Cliente_DAO
from app.dao.funcionario_dao import Funcionario_DAO
from app.dao.equipamento_dao import EquipamentoDAO
from app.dao.ordem_servico_dao import Ordem_servico_DAO
from app.dao.peca_dao import PecaDAO
from app.dao.servico_dao import ServicoDAO
from app.dao.ordem_servico_servico_dao import Ordem_servico_Servico_Dao
from app.dao.ordem_servico_pecas_dao import Ordem_Servico_Peca_DAO
#controller(parametro)
from app.controller.cliente_controller import ClienteController
from app.controller.equipamento_controller import EquipamentoController
from app.controller.funcionario_controller import FuncionarioController 
from app.controller.ordem_servico_controller import Ordem_servico_Controller
from app.controller.ordem_servico_pecas_controller import Ordem_Servico_Peca_Controller
from app.controller.ordem_servico_servico_controller import Ordem_servico_Servico_Controller
#view(parametro)
from.app.view.cliente_view import Cliente_view
from app.view.equipamento_view import Equipamento_View
from app.view.funcionario_view import Funcionario_View
from app.view.ordem_servico_view import Ordem_servico_Controller
from app.view.peca_view import Peca_View
from app.view.servico_view import Servico_View
#o que faz a main rodar
import tkinter as tk
from datetime import datetime
from app.core.database import Database

#criação do menu

class ErpApplication:

    def __init__(self):
        self._database = Database()
        self._self = tk.Tk()