"""
Aplica 3 correções em app/view/ordem_servico_view.py sem você editar à mão.

Uso (na raiz do projeto):
    python ferramentas/aplicar_patch_view.py app/view/ordem_servico_view.py

Faz um backup (.bak) antes e é seguro rodar duas vezes.
"""
import shutil
import sys

CAMINHO_PADRAO = "app/view/ordem_servico_view.py"


def main():
    caminho = sys.argv[1] if len(sys.argv) > 1 else CAMINHO_PADRAO
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        texto = arquivo.read()
    quebra = "\r\n" if "\r\n" in texto else "\n"

    imp_antigo = "from app.core.dataUltils import DataUtils"
    imp_novo = "from app.models.ordem_servico import Ordem_servico"
    status_antigo = 'STATUS_OPCOES = ["aberta", "em andamento", "concluida", "cancelada"]'
    status_novo = "STATUS_OPCOES = Ordem_servico.STATUS_PERMITIDOS"
    valor_antigo = "p.valor:.2f"
    valor_novo = "p.preco_venda:.2f"

    # (descrição, texto antigo, texto novo, marca de "já aplicado")
    correcoes = [
        ("import do model Ordem_servico", imp_antigo, imp_antigo + quebra + imp_novo, imp_novo),
        ("STATUS_OPCOES vindo do model", status_antigo, status_novo, status_novo),
        ("p.valor -> p.preco_venda (aba de peças)", valor_antigo, valor_novo, valor_novo),
    ]

    novo_texto = texto
    aplicou_algo = False
    for descricao, antigo, novo, marca in correcoes:
        if marca in novo_texto:
            print(f"[já estava]   {descricao}")
        elif novo_texto.count(antigo) == 1:
            novo_texto = novo_texto.replace(antigo, novo)
            aplicou_algo = True
            print(f"[aplicado]    {descricao}")
        else:
            print(f"[NÃO ACHEI]   {descricao} -> faça à mão (veja o guia)")

    if aplicou_algo:
        shutil.copyfile(caminho, caminho + ".bak")
        with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
            arquivo.write(novo_texto)
        print(f"\nBackup em {caminho}.bak")


if __name__ == "__main__":
    main()