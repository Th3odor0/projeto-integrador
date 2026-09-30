from datetime import datetime, date


class DataUtils:
    FORMATO_DATA = "%d/%m/%Y"                 # formato canônico, usado na exibição
    FORMATOS_ACEITOS = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d/%m/%y", "%Y-%m-%d"]

    @staticmethod
    def string_para_data(data_texto):
        if not data_texto:
            return None
        # datetime é subclasse de date, por isso é testado primeiro
        if isinstance(data_texto, datetime):
            return data_texto.date()
        if isinstance(data_texto, date):
            return data_texto

        texto = str(data_texto).strip()
        for formato in DataUtils.FORMATOS_ACEITOS:
            try:
                return datetime.strptime(texto, formato).date()
            except ValueError:
                continue  # tenta o próximo formato
        return None

    @staticmethod
    def data_para_string(data_objeto):
        if data_objeto is None or data_objeto == "":
            return ""
        if isinstance(data_objeto, str):
            return data_objeto
        return data_objeto.strftime(DataUtils.FORMATO_DATA)

    @staticmethod
    def validar_data(data_texto):
        return DataUtils.string_para_data(data_texto) is not None