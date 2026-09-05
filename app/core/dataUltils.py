from datetime import datetime, date

class DataUtils:
    # d = dia de 2 dígitos, m = mês de 2 dígitos, Y = ano de 4 dígitos
    FORMATO_DATA = "%d/%m/%Y"

    # Recebe um texto (string) e converte para objeto date
    @staticmethod
    def string_para_data(data_texto):
        if not data_texto:
            return None
        try:
            return datetime.strptime(data_texto, DataUtils.FORMATO_DATA).date()
        except (ValueError, TypeError):
            return None

    # Recebe uma data e converte para texto (string)
    @staticmethod
    def data_para_string(data_objeto):
        # Se for None, retorna uma string vazia
        if data_objeto is None:
            return ""
        return data_objeto.strftime(DataUtils.FORMATO_DATA)

    # Tentativa de converter texto para data, se der certo True, caso contrário False
    @staticmethod
    def validar_data(data_texto):
        if not data_texto:
            return False
        try:
            datetime.strptime(data_texto, DataUtils.FORMATO_DATA)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def calcular_idade(data_texto):
        # Convertemos o texto recebido para um objeto date
        data_inicio = DataUtils.string_para_data(data_texto)

        # Se a data for inválida ou não informada, não dá pra calcular idade
        if data_inicio is None:
            raise ValueError("Data inválida ou não informada para cálculo de idade.")

        hoje = date.today()

        # Impede idade negativa caso a data seja no futuro
        if data_inicio > hoje:
            raise ValueError("Data não pode ser no futuro.")

        idade = hoje.year - data_inicio.year
        # Ajusta se a pessoa ainda não fez aniversário este ano
        if (hoje.month, hoje.day) < (data_inicio.month, data_inicio.day):
            idade -= 1

        return idade