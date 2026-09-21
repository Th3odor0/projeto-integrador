from datetime import datetime, date


class DataUtils:
    # d = dia de 2 dígitos, m = mês de 2 dígitos, Y = ano de 4 dígitos
    FORMATO_DATA = "%d/%m/%Y"                 # formato canônico, usado na exibição
    FORMATOS_ACEITOS = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d/%m/%y", "%Y-%m-%d"]
    # Recebe um texto (string) e converte para objeto date
    @staticmethod
    def string_para_data(data_texto):
        if not data_texto:
            return None
        # Se já for um date/datetime, apenas normaliza para date
        if isinstance(data_texto, datetime):
            return data_texto.date()
        if isinstance(data_texto, date):
            return data_texto
        texto = str(data_texto).strip()
        for formato in DataUtils.FORMATOS_ACEITOS:
            try:
                return datetime.strptime(data_texto, DataUtils.FORMATO_DATA).date()
            except (ValueError, TypeError):
                return None

    # Recebe uma data e converte para texto (string)
    @staticmethod
    def data_para_string(data_objeto):
        # None ou vazio viram string vazia
        if data_objeto is None or data_objeto == "":
            return ""
        # Se já veio como texto (ex.: driver que devolve a data em string), devolve como está
        if isinstance(data_objeto, str):
            return data_objeto
        return data_objeto.strftime(DataUtils.FORMATO_DATA)

    # Tentativa de converter texto para data, se der certo True, caso contrário False
    @staticmethod
    def validar_data(data_texto):
        return DataUtils.string_para_data(data_texto) is not None
        
        ##if not data_texto:
            #return False
        #if isinstance(data_texto, (date, datetime)):
           # return True
        #try:
           # datetime.strptime(data_texto, DataUtils.FORMATO_DATA)
            #return True
        #except (ValueError, TypeError):
          #  return False


    