import os

from dotenv import load_dotenv
from mysql.connector import pooling

load_dotenv()


class Database:
    """
    Conexão com o MySQL via pool.

    Antes, cada conectar() abria uma conexão nova (TCP + login). A listagem de
    ordens de serviço faz várias consultas por linha, então isso multiplicava
    conexões. Com o pool, conectar() pega uma conexão já aberta e o close()
    (em desconectar) só a devolve ao pool.

    O pool é criado no __init__: se o MySQL estiver desligado ou o .env
    estiver errado, o erro acontece AQUI, ao iniciar o programa, e não no
    meio de uma tela. Deixe o main.py capturar essa exceção e mostrar um popup.

    pool_size=5 é suficiente: no pior caso há 3 conexões abertas ao mesmo
    tempo (o DAO de ordens chama os DAOs de cliente/funcionário/equipamento
    enquanto ainda está com a sua conexão aberta).
    """

    _OBRIGATORIAS = ("DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD")

    def __init__(self, pool_size=5):
        faltando = [v for v in self._OBRIGATORIAS if os.getenv(v) is None]
        if faltando:
            raise RuntimeError(
                "Faltam variáveis no arquivo .env: " + ", ".join(faltando)
                + ". Copie .env.example para .env e preencha."
            )

        self._pool = pooling.MySQLConnectionPool(
            pool_name="assistencia_tecnica_pool",
            pool_size=pool_size,
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", "3306")),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            charset="utf8mb4",
        )

    def conectar(self):
        return self._pool.get_connection()

    def desconectar(self, cursor=None, conexao=None):
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if conexao is not None:
            # Em conexão de pool, close() devolve ao pool (não fecha de verdade).
            try:
                conexao.close()
            except Exception:
                pass