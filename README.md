# 🛠️ Assistência Técnica — Sistema de Gestão para Oficinas

Sistema desktop completo para gerenciamento de ordens de serviço em oficinas de assistência técnica, desenvolvido em **Python** com arquitetura **MVC**, banco de dados **MySQL** e interface gráfica em **Tkinter**.

---

## 📌 Sobre o projeto

Oficinas de conserto de equipamentos (eletrônicos, eletrodomésticos, informática, etc.) frequentemente controlam suas ordens de serviço em cadernos, planilhas soltas ou sistemas improvisados — o que gera perda de histórico, dificuldade em calcular valores e falta de rastreabilidade sobre peças e serviços utilizados em cada atendimento.

O **Assistência Técnica** nasceu para resolver esse problema: um sistema local, simples de instalar e usar, que organiza todo o fluxo de uma ordem de serviço — da entrada do equipamento até a entrega ao cliente — mantendo o controle de peças aplicadas, serviços prestados, formas de pagamento e garantia.

---

## 🎯 Público-alvo

- Pequenas e médias oficinas de assistência técnica (eletrônicos, celulares, informática, eletrodomésticos).
- Técnicos autônomos que precisam formalizar e organizar seus atendimentos.
- Negócios que ainda controlam ordens de serviço manualmente e querem migrar para um sistema digital sem depender de soluções em nuvem pagas ou complexas.

---

## ✨ Funcionalidades

- **Cadastro de Ordens de Serviço** — vincula cliente, funcionário responsável e equipamento, registrando problema relatado, diagnóstico técnico, status do atendimento e garantia.
- **Gestão de Clientes, Funcionários e Equipamentos** — cadastro completo de quem traz o equipamento, quem realiza o conserto e o que está sendo consertado.
- **Controle de Peças utilizadas** — cada ordem de serviço permite adicionar múltiplas peças do estoque, com quantidade e valor unitário, calculando o subtotal automaticamente.
- **Controle de Serviços prestados** — vincula os serviços realizados (mão de obra, diagnóstico, limpeza, etc.) a cada ordem, com valor cobrado individualizado.
- **Cálculo automático de valores** — o sistema soma peças e serviços para compor o valor total da ordem.
- **Histórico de status** — acompanhamento da evolução da ordem (aberta → em andamento → concluída).
- **Controle de garantia** — registro de dias de garantia por ordem de serviço.

---

## 🧱 Arquitetura

O projeto segue o padrão **MVC (Model-View-Controller)**, separando claramente as responsabilidades:

```
app/
├── models/        # Entidades do domínio (Cliente, Funcionario, Equipamento, OrdemServico, Peca, Servico...)
├── dao/           # Camada de acesso a dados (DAO Pattern) — isola toda a comunicação com o MySQL
├── controllers/   # Regras de negócio e validações — ponte entre a View e o DAO
├── views/         # Interface gráfica em Tkinter
└── utils/         # Utilitários reutilizáveis (ex: conversão e validação de datas)
```

**Por que essa separação importa:**
- **Models** representam os dados puros, sem conhecer banco de dados ou interface.
- **DAOs** cuidam exclusivamente do SQL (INSERT, SELECT, UPDATE, DELETE), isolando o resto do sistema de detalhes do MySQL.
- **Controllers** validam entradas do usuário (datas, valores, campos obrigatórios) e orquestram a comunicação entre a tela e o banco.
- **Views** cuidam apenas da apresentação visual — não sabem nada sobre SQL ou regras de negócio.

Essa arquitetura facilita manutenção, testes e a compreensão do código por quem está aprendendo ou contribuindo com o projeto.

---

## 🗄️ Modelo de dados

Principais tabelas do banco de dados MySQL:

| Tabela | Descrição |
|---|---|
| `clientes` | Dados dos clientes que trazem equipamentos para conserto |
| `funcionarios` | Técnicos e colaboradores da oficina |
| `equipamentos` | Equipamentos recebidos, vinculados a um cliente |
| `ordens_servico` | Núcleo do sistema — entrada, diagnóstico, status, valores e garantia |
| `pecas` | Estoque de peças disponíveis, com preço de venda |
| `servicos` | Catálogo de serviços oferecidos, com valor padrão |
| `ordem_servico_pecas` | Peças efetivamente utilizadas em cada ordem (quantidade e valor unitário) |
| `ordem_servico_servicos` | Serviços efetivamente prestados em cada ordem (valor cobrado) |

---

## 🚀 Tecnologias utilizadas

- **Python 3** — linguagem principal do projeto
- **MySQL** — banco de dados relacional
- **Tkinter** — interface gráfica desktop
- **DAO Pattern** — abstração de acesso a dados
- **Arquitetura MVC** — organização em camadas

---

## 📦 Status do projeto

🔧 Em desenvolvimento ativo — projeto de estudo com aplicação prática, construído camada por camada (models → DAOs → controllers → views).

---

## 👤 Autor

Desenvolvido por **Theodoro** ([@Th3odor0](https://github.com/Th3odor0)), **Renato** ([renato1903-byte](https://github.com/renato1903-byte)) e **Guilherme** ([Gu1paz](https://github.com/Gu1paz)) como projeto de estudo e aplicação prática de Programação Orientada a Objetos, arquitetura MVC e integração com banco de dados em Python.
