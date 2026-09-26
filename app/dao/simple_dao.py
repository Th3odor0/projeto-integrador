from app.dao.dao import DAO


class SimpleDAO(DAO):
    """
    DAO genérico para entidades "simples": uma tabela, uma linha por objeto,
    sem relacionamento com outra tabela (Cliente, Funcionario, Peca, Servico
    se encaixam aqui; Equipamento e OrdemServico não, porque dependem de
    outros DAOs para montar o objeto).

    Quem usa só precisa informar, no __init__ da subclasse:
      - tabela:      nome da tabela no banco (minúsculo, igual ao DDL)
      - colunas:     colunas da tabela, NA MESMA ORDEM dos parâmetros do
                     construtor da entidade (sem o id)
      - construtor:  a classe da entidade (Cliente, Peca, ...)
      - para_tupla:  função (objeto) -> tupla de valores, na mesma ordem de
                     'colunas' (o que entra no INSERT/UPDATE)

    'tabela' e 'colunas' são definidos pela própria subclasse (nunca vêm de
    entrada do usuário), então montar o SQL com f-string aqui é seguro —
    os valores de fato variáveis (nome, cpf, etc.) continuam indo via `%s`.
    """

    def __init__(self, database, tabela, colunas, construtor, para_tupla):
        super().__init__(database)
        self._tabela = tabela
        self._colunas = colunas
        self._construtor = construtor
        self._para_tupla = para_tupla

    def _montar_objeto(self, registro):
        # registro[0] é sempre o id; o resto segue a ordem de 'colunas'
        return self._construtor(registro[0], *registro[1:])

    def save(self, objeto):
        conexao, cursor = self.conectar()
        try:
            placeholders = ", ".join(["%s"] * len(self._colunas))
            sql = f"""
                INSERT INTO {self._tabela} ({", ".join(self._colunas)})
                VALUES ({placeholders})
            """
            cursor.execute(sql, self._para_tupla(objeto))
            conexao.commit()
            objeto.id = cursor.lastrowid
            return objeto
        except Exception:
            conexao.rollback()
            raise
        finally:
            self.desconectar(cursor, conexao)

    def get_all(self, order_by=None):
        conexao, cursor = self.conectar()
        try:
            colunas_sql = ", ".join(["id"] + self._colunas)
            sql = f"SELECT {colunas_sql} FROM {self._tabela}"
            if order_by:
                sql += f" ORDER BY {order_by}"
            cursor.execute(sql)
            return [self._montar_objeto(registro) for registro in cursor.fetchall()]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        conexao, cursor = self.conectar()
        try:
            colunas_sql = ", ".join(["id"] + self._colunas)
            sql = f"SELECT {colunas_sql} FROM {self._tabela} WHERE id = %s"
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
            return self._montar_objeto(registro) if registro else None
        finally:
            self.desconectar(cursor, conexao)

    def update(self, objeto):
        conexao, cursor = self.conectar()
        try:
            set_sql = ", ".join(f"{coluna} = %s" for coluna in self._colunas)
            sql = f"UPDATE {self._tabela} SET {set_sql} WHERE id = %s"
            cursor.execute(sql, self._para_tupla(objeto) + (objeto.id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception:
            conexao.rollback()
            raise
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        conexao, cursor = self.conectar()
        try:
            sql = f"DELETE FROM {self._tabela} WHERE id = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception:
            conexao.rollback()
            raise
        finally:
            self.desconectar(cursor, conexao)