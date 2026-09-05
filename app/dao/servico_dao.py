from app.dao.dao import DAO
from app.models.servico import Servico

class ServicoDAO(DAO):
    def __init__(self, database):
        super().__init__(database)
        