# AJUSTES: "idioma.trocar" (PT e EN) agora mostra o idioma ATUAL no botão 🌐 do menu
# (PT -> "Português", EN -> "English"); + bloco 4 com as chaves novas (main, menu, crud_view_base,
# ordem_servico_view e controllers). Nada foi removido: o resto do arquivo está igual ao que você enviou.
"""
Módulo central de internacionalização (i18n) do sistema.

Duas famílias de chaves convivem no mesmo dicionário, sem colidir:

  1. Chaves "namespaced" (com ponto), usadas pela main.py no menu/sidebar/
     painel inicial: t("app.titulo"), t("modulo.os.titulo"), t("data.dias").
     Para essas, tanto o dicionário PT quanto o EN precisam ter a entrada,
     porque a chave em si (ex.: "app.titulo") não é um texto legível — se
     não houver tradução cadastrada, t() devolve a própria chave, o que
     apareceria errado na tela.

  2. Chaves de texto literal, usadas pelas views (Cliente_view,
     Ordem_servico_View etc.): t("Cliente:"), t("Salvar"), t("aberta").
     Para essas, a CHAVE já É o texto em português, então o dicionário PT
     não precisa ter a entrada — t() cai no fallback e devolve a própria
     chave, que já é o texto certo. Só o dicionário EN precisa da entrada.

API:
  - IDIOMAS_DISPONIVEIS: lista de códigos de idioma suportados.
  - carregar_idioma(codigo): troca o idioma ativo.
  - idioma_atual(): devolve o código do idioma ativo no momento.
  - t(chave, **kwargs): traduz 'chave' para o idioma ativo. Se o valor
    encontrado for uma string e houver kwargs, aplica .format(**kwargs)
    nela (usado por "data.formato"). Se for uma lista (ex.: "data.dias"),
    devolve a lista como está, ignorando kwargs.
"""

_IDIOMA_ATUAL = "pt"

# --- Idioma "nativo": entradas com chave namespaced precisam de valor aqui
# (ver explicação acima). As chaves de texto literal das views não precisam
# ser duplicadas aqui — t() já devolve o próprio texto quando não encontra
# tradução.
_TEXTOS_PT = {
    # --- Janela e marca ---
    "app.titulo": "Sistema ERP - Assistência Técnica",
    "marca.sigla": "AT",
    "marca.nome": "Assistência Técnica",
    "marca.tagline": "Sistema ERP Corporativo",

    # --- Sidebar ---
    "tema.escuro": "Modo escuro",
    "tema.claro": "Modo claro",
    "nav.sair": "Sair",
    "idioma.trocar": "Português",  # AJUSTE: botão 🌐 mostra o idioma atual

    # --- Painel inicial ---
    "painel.titulo": "Painel Inicial",
    "painel.bemvindo": "Bem-vindo(a) 👋",
    "painel.subtitulo": "Selecione um módulo abaixo para começar o atendimento.",

    # --- Módulos (cartões) ---
    "modulo.os.titulo": "Ordens de Serviço",
    "modulo.os.descricao": "Abrir, acompanhar e concluir atendimentos",
    "modulo.cliente.titulo": "Clientes",
    "modulo.cliente.descricao": "Cadastro e histórico de clientes",
    "modulo.funcionario.titulo": "Funcionários",
    "modulo.funcionario.descricao": "Equipe técnica e administrativa",
    "modulo.equipamento.titulo": "Equipamentos",
    "modulo.equipamento.descricao": "Aparelhos recebidos para reparo",
    "modulo.servico.titulo": "Serviços",
    "modulo.servico.descricao": "Catálogo de serviços prestados pela oficina",
    "modulo.peca.titulo": "Peças",
    "modulo.peca.descricao": "Estoque de peças utilizadas nos reparos",

    # --- Data por extenso ---
    "data.dias": ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
                  "sexta-feira", "sábado", "domingo"],
    "data.meses": ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
                   "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"],
    "data.formato": "{dia_semana}, {dia} de {mes} de {ano}",
}

_TEXTOS_EN = {
    # --- Janela e marca ---
    "app.titulo": "ERP System - Technical Support",
    "marca.sigla": "TS",
    "marca.nome": "Technical Support",
    "marca.tagline": "Corporate ERP System",

    # --- Sidebar ---
    "tema.escuro": "Dark mode",
    "tema.claro": "Light mode",
    "nav.sair": "Exit",
    "idioma.trocar": "English",  # AJUSTE: botão 🌐 mostra o idioma atual

    # --- Painel inicial ---
    "painel.titulo": "Home Dashboard",
    "painel.bemvindo": "Welcome 👋",
    "painel.subtitulo": "Select a module below to start assisting customers.",

    # --- Módulos (cartões) ---
    "modulo.os.titulo": "Service Orders",
    "modulo.os.descricao": "Open, track and complete service requests",
    "modulo.cliente.titulo": "Customers",
    "modulo.cliente.descricao": "Customer records and history",
    "modulo.funcionario.titulo": "Employees",
    "modulo.funcionario.descricao": "Technical and administrative team",
    "modulo.equipamento.titulo": "Equipment",
    "modulo.equipamento.descricao": "Devices received for repair",
    "modulo.servico.titulo": "Services",
    "modulo.servico.descricao": "Catalog of services offered by the shop",
    "modulo.peca.titulo": "Parts",
    "modulo.peca.descricao": "Inventory of parts used in repairs",

    # --- Data por extenso ---
    "data.dias": ["Monday", "Tuesday", "Wednesday", "Thursday",
                  "Friday", "Saturday", "Sunday"],
    "data.meses": ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"],
    "data.formato": "{dia_semana}, {mes} {dia}, {ano}",

    # ==================================================================
    # A partir daqui: chaves de TEXTO LITERAL (o texto em português que já
    # é passado para t(...) dentro das views). Só o dicionário EN precisa
    # dessas entradas — no PT, t() já devolve a própria chave como fallback.
    # ==================================================================

    # --- Status da Ordem de Serviço (valor canônico gravado no banco) ---
    "aberta": "open",
    "em andamento": "in progress",
    "concluida": "completed",
    "cancelada": "cancelled",

    # --- Campos e ações comuns às views ---
    "Cliente:": "Customer:",
    "Funcionário:": "Employee:",
    "Equipamento:": "Equipment:",
    "Status:": "Status:",
    "Data de entrada (dd/mm/aaaa):": "Entry date (dd/mm/yyyy):",
    "Data de conclusão (opcional):": "Completion date (optional):",
    "Problema:": "Problem:",
    "Diagnóstico:": "Diagnosis:",
    "Valor total (R$):": "Total amount ($):",
    "Forma de pagamento:": "Payment method:",
    "Dias de garantia:": "Warranty (days):",
    "Novo": "New",
    "Salvar": "Save",
    "Alterar": "Edit",
    "Excluir": "Delete",
    "ID": "ID",
    "Entrada": "Entry",
    "Sucesso": "Success",
    "Erro": "Error",
    "Erro de validação": "Validation error",
    "Erro inesperado": "Unexpected error",
    "Aviso": "Warning",
    "Confirmação": "Confirmation",
    "Ocorreu um erro:": "An error occurred:",

    # --- Aba "Dados da Ordem" (Ordem_servico_View) ---
    "Dados da Ordem": "Order Data",
    "Serviços Prestados": "Services Provided",
    "Peças Utilizadas": "Parts Used",
    "Selecione cliente, funcionário e equipamento.": "Select customer, employee and equipment.",
    'Há uma ordem selecionada. Use "Alterar" para editá-la ou "Novo" para começar um cadastro.':
        'An order is selected. Use "Edit" to modify it or "New" to start a new one.',
    "Ordem de serviço cadastrada com sucesso!": "Service order created successfully!",
    "Selecione uma ordem na lista para alterar.": "Select an order in the list to edit.",
    "Ordem de serviço alterada com sucesso!": "Service order updated successfully!",
    "Selecione uma ordem na lista para excluir.": "Select an order in the list to delete.",
    "Deseja realmente excluir esta ordem de serviço?": "Are you sure you want to delete this service order?",
    "Ordem de serviço excluída com sucesso!": "Service order deleted successfully!",

    # --- Aba "Serviços Prestados" ---
    "Serviço:": "Service:",
    "Valor cobrado (R$):": "Charged amount ($):",
    "Adicionar": "Add",
    "Atualizar valor": "Update amount",
    "Remover": "Remove",
    "Valor Cobrado": "Charged Amount",
    'Selecione ou salve uma ordem na aba "Dados da Ordem" para gerenciar os serviços.':
        'Select or save an order in the "Order Data" tab to manage services.',
    "Serviços da ordem": "Services for order",
    "Selecione ou salve uma ordem de serviço primeiro.": "Select or save a service order first.",
    "Selecione um serviço.": "Select a service.",
    "Serviço adicionado com sucesso!": "Service added successfully!",
    "Selecione um serviço na lista para atualizar.": "Select a service in the list to update.",
    "Selecione um serviço na lista para remover.": "Select a service in the list to remove.",
    "Remover este serviço da ordem?": "Remove this service from the order?",

    # --- Aba "Peças Utilizadas" ---
    "Peça:": "Part:",
    "Quantidade:": "Quantity:",
    "Valor unitário (R$):": "Unit price ($):",
    "Adicionar à lista": "Add to list",
    "Remover da lista": "Remove from list",
    "Peça": "Part",
    "Qtd.": "Qty.",
    "Valor unit.": "Unit price",
    "Subtotal": "Subtotal",
    "Total peças: R$": "Total parts: $",
    "Salvar peças da ordem": "Save order's parts",
    "Gerenciamento de peças não conectado (controller/DAO não informados).":
        "Parts management not connected (controller/DAO not provided).",
    'Selecione ou salve uma ordem na aba "Dados da Ordem" para gerenciar as peças.':
        'Select or save an order in the "Order Data" tab to manage parts.',
    "Peças da ordem": "Parts for order",
    "Peça não encontrada na lista de peças disponíveis.": "Part not found in the list of available parts.",
    "Quantidade precisa ser um número inteiro.": "Quantity must be a whole number.",
    "Quantidade deve ser maior que zero.": "Quantity must be greater than zero.",
    "Valor unitário precisa ser um número.": "Unit price must be a number.",
    "Valor unitário não pode ser negativo.": "Unit price cannot be negative.",
    "Selecione uma peça.": "Select a part.",
    "Selecione uma peça na lista para remover.": "Select a part in the list to remove.",

    # --- Campos comuns a Cliente/Equipamento/Funcionario/Servico views ---
    "ID:": "ID:",
    "Nome:": "Name:",
    "CPF:": "SSN:",
    "Telefone:": "Phone:",
    "Email:": "Email:",
    "Tipo:": "Type:",
    "Marca:": "Brand:",
    "Modelo:": "Model:",
    "Número de série:": "Serial number:",
    "Cargo:": "Position:",
    "Descrição:": "Description:",
    "Valor padrão (R$):": "Default price ($):",
    "Atualizar": "Update",
    "Deletar": "Delete",
    "Nome": "Name",
    "CPF": "SSN",
    "Telefone": "Phone",
    "Email": "Email",
    "Tipo": "Type",
    "Marca": "Brand",
    "Modelo": "Model",
    "Nº Série": "Serial No.",
    "Cliente": "Customer",
    "Cargo": "Position",
    "Descrição": "Description",
    "Valor Padrão": "Default Price",
    "Confirmar": "Confirm",

    # --- Campos da tela de Peças (Peca_View) ---
    "Código:": "Code:",
    "Quantidade em estoque:": "Stock quantity:",
    "Preço de venda (R$):": "Sale price ($):",
    "Código": "Code",
    "Qtd. Estoque": "Stock Qty.",
    "Preço Venda": "Sale Price",

    # --- Mensagens de validação/estado comuns às views ---
    "Nenhum cliente selecionado (ID vazio).": "No customer selected (empty ID).",
    "O campo ID deve ser um número inteiro.": "The ID field must be a whole number.",
    "Nenhum equipamento selecionado (ID vazio).": "No equipment selected (empty ID).",
    "Nenhum funcionário selecionado (ID vazio).": "No employee selected (empty ID).",
    "Nenhum serviço selecionado (ID vazio).": "No service selected (empty ID).",
    "Selecione um cliente.": "Select a customer.",
    "Erro ao buscar serviços:": "Error fetching services:",

    # --- Mensagens de sucesso/confirmação comuns às views ---
    "Cliente cadastrado com sucesso!": "Customer created successfully!",
    "Tem certeza que deseja excluir esse cliente?": "Are you sure you want to delete this customer?",
    "Equipamento cadastrado com sucesso!": "Equipment created successfully!",
    "Equipamento atualizado com sucesso!": "Equipment updated successfully!",
    "Tem certeza que deseja excluir esse equipamento?": "Are you sure you want to delete this equipment?",
    "Equipamento excluído com sucesso!": "Equipment deleted successfully!",
    "Funcionário cadastrado com sucesso!": "Employee created successfully!",
    "Tem certeza que deseja excluir esse funcionário?": "Are you sure you want to delete this employee?",
    "Serviço cadastrado com sucesso!": "Service created successfully!",
    "Tem certeza que deseja excluir esse serviço?": "Are you sure you want to delete this service?",
}

# ======================================================================
# ADIÇÕES (bloco 1): títulos das telas, colunas, Peca_View e
# Funcionario_Controller
# ======================================================================
_TEXTOS_EN.update({
    # --- Títulos e subtítulos das telas (usados em configurar_janela / criar_cabecalho) ---
    "Ordens de Serviço": "Service Orders",
    "Abrir, acompanhar e concluir atendimentos": "Open, track and complete service requests",
    "Clientes": "Customers",
    "Cadastro e histórico de clientes": "Customer records and history",
    "Funcionários": "Employees",
    "Equipe técnica e administrativa": "Technical and administrative team",
    "Equipamentos": "Equipment",
    "Aparelhos recebidos para reparo": "Devices received for repair",
    "Serviços": "Services",
    "Catálogo de serviços prestados pela oficina": "Catalog of services offered by the shop",
    "Peças": "Parts",
    "Estoque de peças utilizadas nos reparos": "Inventory of parts used in repairs",

    # --- Títulos de coluna que faltavam (Ordem_servico_View) ---
    "Serviço": "Service",
    "Equipamento": "Equipment",
    "Status": "Status",

    # --- Peca_View ---
    "Nenhuma peça selecionada (ID vazio).": "No part selected (empty ID).",
    "Peça cadastrada com sucesso!": "Part created successfully!",
    "Tem certeza que deseja excluir essa peça?": "Are you sure you want to delete this part?",

    # --- Funcionario_Controller ---
    "O nome é obrigatório.": "Name is required.",
    "CPF inválido. Deve conter 11 dígitos.": "Invalid CPF. It must contain 11 digits.",
    "O cargo é obrigatório.": "Position is required.",
    "CPF já cadastrado.": "CPF already registered.",
    "Funcionário não encontrado.": "Employee not found.",
    "Funcionário atualizado com sucesso.": "Employee updated successfully.",
    "Funcionário excluído com sucesso.": "Employee deleted successfully.",
    "Não foi possível atualizar o funcionário.": "Could not update the employee.",
    "Não foi possível excluir o funcionário.": "Could not delete the employee.",
    "Erro ao cadastrar funcionário:": "Error creating employee:",
    "Erro ao atualizar funcionário:": "Error updating employee:",
    "Erro ao excluir funcionário:": "Error deleting employee:",
    "Erro ao buscar funcionários:": "Error fetching employees:",
})

# ======================================================================
# ADIÇÕES (bloco 2): Peca_View (listagem) e Peca_Controller
# ======================================================================
_TEXTOS_EN.update({
    # --- Peca_View ---
    "Erro ao buscar peças:": "Error fetching parts:",

    # --- Peca_Controller ---
    "O nome da peça é obrigatório.": "Part name is required.",
    "O código da peça é obrigatório.": "Part code is required.",
    "A quantidade em estoque não pode ser negativa.": "Stock quantity cannot be negative.",
    "Quantidade em estoque inválida. Informe um número inteiro.": "Invalid stock quantity. Enter a whole number.",
    "O preço de venda não pode ser negativo.": "Sale price cannot be negative.",
    "Preço de venda inválido. Informe um valor numérico.": "Invalid sale price. Enter a numeric value.",
    "Já existe uma peça cadastrada com esse código.": "A part with this code already exists.",
    "Já existe outra peça cadastrada com esse código.": "Another part with this code already exists.",
    "Peça não encontrada.": "Part not found.",
    "Peça atualizada com sucesso.": "Part updated successfully.",
    "Peça excluída com sucesso.": "Part deleted successfully.",
    "Não foi possível atualizar a peça.": "Could not update the part.",
    "Não foi possível excluir a peça.": "Could not delete the part.",
    "Erro ao cadastrar peça:": "Error creating part:",
    "Erro ao atualizar peça:": "Error updating part:",
    "Erro ao excluir peça:": "Error deleting part:",
    "Quantidade inválida.": "Invalid quantity.",
    "A quantidade utilizada deve ser maior que zero.": "The quantity used must be greater than zero.",
    "Estoque insuficiente para essa quantidade.": "Insufficient stock for this quantity.",
    "Baixa de estoque realizada. Restam {quantidade} unidades.": "Stock deducted. {quantidade} units remaining.",
    "Erro ao atualizar estoque:": "Error updating stock:",
})

# ======================================================================
# ADIÇÕES (bloco 3): mensagens dos controllers de Cliente, Equipamento,
# Serviço, Ordem de Serviço, Serviços da OS e Peças da OS
# (as mensagens com {chave} são preenchidas por t(..., chave=valor))
# ======================================================================
_TEXTOS_EN.update({
    # --- ClienteController ---
    "O telefone é obrigatório.": "Phone is required.",
    "O email é inválido.": "Email is invalid.",
    "Erro ao cadastrar cliente:": "Error creating customer:",
    "Cliente não encontrado.": "Customer not found.",
    "Já existe outro cliente cadastrado com esse CPF.": "Another customer is already registered with this CPF.",
    "Cliente atualizado com sucesso.": "Customer updated successfully.",
    "Não foi possível atualizar o cliente.": "Could not update the customer.",
    "Erro ao atualizar cliente:": "Error updating customer:",
    "Cliente deletado com sucesso.": "Customer deleted successfully.",
    "Falha ao deletar cliente.": "Failed to delete the customer.",
    "Erro ao deletar cliente:": "Error deleting customer:",
    "Erro ao buscar clientes:": "Error fetching customers:",

    # --- EquipamentoController ---
    "O tipo do equipamento é obrigatório.": "Equipment type is required.",
    "A marca é obrigatória.": "Brand is required.",
    "O modelo é obrigatório.": "Model is required.",
    "O número de série é obrigatório.": "Serial number is required.",
    "Já existe um equipamento cadastrado com esse número de série.": "An equipment with this serial number already exists.",
    "Já existe outro equipamento cadastrado com esse número de série.": "Another equipment with this serial number already exists.",
    "Equipamento não encontrado.": "Equipment not found.",
    "Equipamento atualizado com sucesso.": "Equipment updated successfully.",
    "Equipamento excluído com sucesso.": "Equipment deleted successfully.",
    "Não foi possível atualizar o equipamento.": "Could not update the equipment.",
    "Não foi possível excluir o equipamento.": "Could not delete the equipment.",
    "Erro ao cadastrar equipamento:": "Error creating equipment:",
    "Erro ao atualizar equipamento:": "Error updating equipment:",
    "Erro ao excluir equipamento:": "Error deleting equipment:",

    # --- ServicoController ---
    "O nome do serviço é obrigatório.": "Service name is required.",
    "A descrição é obrigatória.": "Description is required.",
    "O valor padrão não pode ser negativo.": "Default price cannot be negative.",
    "Valor padrão inválido. Informe um valor numérico.": "Invalid default price. Enter a numeric value.",
    "Serviço não encontrado.": "Service not found.",
    "Serviço atualizado com sucesso.": "Service updated successfully.",
    "Serviço excluído com sucesso.": "Service deleted successfully.",
    "Não foi possível atualizar o serviço.": "Could not update the service.",
    "Não foi possível excluir o serviço.": "Could not delete the service.",
    "Erro ao cadastrar serviço:": "Error creating service:",
    "Erro ao atualizar serviço:": "Error updating service:",
    "Erro ao excluir serviço:": "Error deleting service:",

    # --- Ordem_servico_Controller ---
    "Valor total precisa ser um número.": "Total amount must be a number.",
    "Valor total não pode ser negativo.": "Total amount cannot be negative.",
    "Dias de garantia precisa ser um número inteiro.": "Warranty days must be a whole number.",
    "Dias de garantia não pode ser negativo.": "Warranty days cannot be negative.",
    "Data de conclusão inválida. Use o formato dd/mm/aaaa.": "Invalid completion date. Use the format dd/mm/yyyy.",
    "O campo 'problema' é obrigatório.": "The 'problem' field is required.",
    "A data de entrada é obrigatória.": "Entry date is required.",
    "Data de entrada inválida: {data}. Use o formato dd/mm/aaaa.": "Invalid entry date: {data}. Use the format dd/mm/yyyy.",
    "Data de conclusão não pode ser anterior à data de entrada.": "Completion date cannot be earlier than the entry date.",
    "Cliente com id {id} não encontrado.": "Customer with id {id} not found.",
    "Funcionário com id {id} não encontrado.": "Employee with id {id} not found.",
    "Equipamento com id {id} não encontrado.": "Equipment with id {id} not found.",
    "Ordem de serviço com id {id} não encontrada.": "Service order with id {id} not found.",

    # --- Ordem_servico_Servico_Controller ---
    "Erro ao buscar serviços da ordem:": "Error fetching the order's services:",
    "Serviço com id {id} não encontrado.": "Service with id {id} not found.",
    "Valor cobrado precisa ser um número.": "Charged amount must be a number.",
    "Valor cobrado não pode ser negativo.": "Charged amount cannot be negative.",
    "Erro ao adicionar serviço:": "Error adding service:",
    "Item não encontrado.": "Item not found.",
    "Valor atualizado com sucesso.": "Amount updated successfully.",
    "Não foi possível atualizar o valor.": "Could not update the amount.",
    "Erro ao atualizar:": "Error updating:",
    "Serviço removido com sucesso.": "Service removed successfully.",
    "Não foi possível remover o serviço.": "Could not remove the service.",
    "Erro ao remover:": "Error removing:",

    # --- Ordem_Servico_Peca_Controller ---
    "Erro ao buscar peças da ordem:": "Error fetching the order's parts:",
    "Peça com id {id} não encontrada.": "Part with id {id} not found.",
    "Quantidade inválida para a peça '{nome}'.": "Invalid quantity for part '{nome}'.",
    "A quantidade da peça '{nome}' deve ser maior que zero.": "The quantity of part '{nome}' must be greater than zero.",
    "Estoque insuficiente para a peça '{nome}' (disponível: {disponivel}).": "Insufficient stock for part '{nome}' (available: {disponivel}).",
    "Valor unitário inválido para a peça '{nome}'.": "Invalid unit price for part '{nome}'.",
    "O valor unitário da peça '{nome}' não pode ser negativo.": "The unit price of part '{nome}' cannot be negative.",
    "Peças da ordem de serviço atualizadas com sucesso.": "Service order parts updated successfully.",
    "Erro ao salvar peças da ordem:": "Error saving the order's parts:",
})

# ======================================================================
# ADIÇÕES (bloco 4 — NOVO): main.py, crud_view_base, ordem_servico_view e
# os textos dos controllers que ainda não tinham tradução
# ======================================================================
_TEXTOS_EN.update({
    # --- main.py ---
    "Banco de dados": "Database",
    "Não foi possível conectar ao MySQL:": "Could not connect to MySQL:",
    "Erro ao abrir a tela": "Error opening the screen",

    # --- CrudViewBase (telas de Cliente, Equipamento, Funcionario, Peca e Servico) ---
    "Erro ao carregar a tela": "Error loading the screen",
    "Cadastro de clientes": "Customer registration",
    "Cadastro de funcionários": "Employee registration",
    "Qtd. em estoque:": "Stock quantity:",
    "Nenhum registro selecionado (ID vazio).": "No record selected (empty ID).",
    "Cadastrado com sucesso.": "Created successfully.",
    "Atualizado com sucesso.": "Updated successfully.",
    "Excluído com sucesso.": "Deleted successfully.",
    "Tem certeza que deseja excluir esse registro?": "Are you sure you want to delete this record?",

    # --- Ordem_servico_View ---
    "Conclusão": "Completion",
    "Valor unit. (R$):": "Unit price ($):",
    "Selecione/salve uma ordem para gerir serviços.": "Select/save an order to manage services.",
    "Selecione/salve uma ordem para gerir peças.": "Select/save an order to manage parts.",
    "Gerenciamento de peças não conectado.": "Parts management not connected.",
    "Em estoque:": "In stock:",
    "Quantidade ou valor inválidos.": "Invalid quantity or amount.",
    "Use 'Alterar' para editar ou 'Novo' para cadastrar.": "Use 'Edit' to modify or 'New' to create.",
    "Selecione uma ordem.": "Select an order.",
    "Excluir ordem?": "Delete order?",
    "Cadastrada com sucesso!": "Created successfully!",
    "Alterada com sucesso!": "Updated successfully!",
    "Excluída com sucesso!": "Deleted successfully!",
    "Remover serviço?": "Remove service?",

    # --- Controllers (textos que estavam sem tradução) ---
    "Cliente excluído com sucesso.": "Customer deleted successfully.",
    "Falha ao excluir cliente.": "Failed to delete the customer.",
    "Erro ao excluir cliente:": "Error deleting customer:",
    "Erro ao buscar equipamentos:": "Error fetching equipment:",
    "A mesma peça aparece mais de uma vez na lista.": "The same part appears more than once in the list.",
    "Selecione o cliente.": "Select the customer.",
    "Selecione o funcionário.": "Select the employee.",
    "Selecione o equipamento.": "Select the equipment.",
    "O problema deve ter no máximo 255 caracteres.": "The problem must be at most 255 characters.",

    # --- DAOs (mensagens de ValueError que chegam à tela) ---
    "Não é possível excluir: este registro está sendo usado em ordens de serviço ou em outros cadastros.": "Cannot delete: this record is in use by service orders or other records.",
    "Não é possível excluir: este equipamento está vinculado a ordens de serviço.": "Cannot delete: this equipment is linked to service orders.",
    "Estoque insuficiente para a peça '{nome}'.": "Insufficient stock for part '{nome}'.",

    # --- Models ---
    "Status inválido: {status}": "Invalid status: {status}",
})

IDIOMAS = {
    "pt": _TEXTOS_PT,
    "en": _TEXTOS_EN,
}

IDIOMAS_DISPONIVEIS = list(IDIOMAS.keys())


def carregar_idioma(codigo):
    """Troca o idioma ativo do sistema. codigo: 'pt' ou 'en'."""
    global _IDIOMA_ATUAL
    if codigo not in IDIOMAS:
        raise ValueError(f"Idioma '{codigo}' não suportado. Use um de: {IDIOMAS_DISPONIVEIS}")
    _IDIOMA_ATUAL = codigo


def idioma_atual():
    """Devolve o código do idioma ativo no momento (ex.: 'pt' ou 'en')."""
    return _IDIOMA_ATUAL


def t(chave, **kwargs):
    """
    Traduz 'chave' para o idioma ativo.

    - Se 'chave' for namespaced (ex.: "app.titulo") e não houver tradução
      cadastrada, devolve a própria chave (o que só deveria acontecer se
      uma chave nova ainda não foi cadastrada nos dois idiomas).
    - Se 'chave' for um texto literal em português (usado pelas views) e
      não houver tradução cadastrada, devolve o próprio texto — é assim
      que o idioma "pt" funciona sem precisar duplicar cada string.
    - Se o valor encontrado for uma string e houver kwargs, aplica
      .format(**kwargs) nela (usado por "data.formato").
    - Se o valor encontrado for uma lista (ex.: "data.dias"), devolve a
      lista como está.
    """
    valor = IDIOMAS.get(_IDIOMA_ATUAL, {}).get(chave, chave)
    if kwargs and isinstance(valor, str):
        return valor.format(**kwargs)
    return valor