# Porsche Sales Intelligence

## 1. Visão geral

O projeto **Porsche Sales Intelligence** tem como objetivo transformar uma planilha de dados de vendas em uma base estruturada, padronizada e preparada para análise, utilizando um processo automatizado de **ETL (Extract, Transform, Load)** e, posteriormente, disponibilizar os dados tratados em uma **Dashboard de Business Intelligence**.

O fluxo do projeto foi desenvolvido para reduzir atividades manuais de tratamento de dados, melhorar a qualidade das informações e facilitar a análise do desempenho comercial por meio de indicadores, filtros, gráficos e insights.

O processo pode ser representado da seguinte forma:

```text
Planilha Base Porsche
        │
        ▼
      ETL
        │
        │  Schema + regras de tratamento
        ▼
Agente de Sanitização Porsche
        │
        ▼
Planilha Porsche Sanitizada
        │
        ▼
Dashboard Porsche Sales Intelligence
```

---

# 2. Objetivo do projeto

O projeto busca responder perguntas de negócio relacionadas ao comportamento das vendas de veículos Porsche, principalmente:

* Quais são os modelos de Porsche mais vendidos em cada cidade?
* Qual combinação de **Model Year + Modelo** apresenta maior volume de vendas?
* Quais cidades concentram maior quantidade de vendas?
* Qual é a receita gerada pelas vendas?
* Qual é o ticket médio dos veículos vendidos?
* Quais formas de pagamento são mais utilizadas?
* Quais modelos apresentam maior popularidade?
* Como o mix de produtos se comporta entre as diferentes cidades?
* Quais padrões podem ser identificados nos dados de vendas?

A solução combina **engenharia de dados, automação, qualidade de dados e visualização analítica**.

---

# 3. Estrutura do processo

## 3.1. Extração — Planilha Base Porsche

O primeiro estágio do projeto consiste na utilização do arquivo:

```text
Planilha base Porsche
```

Essa planilha representa a **fonte de dados original** utilizada pelo processo de ETL.

A etapa de extração tem como finalidade disponibilizar os registros para processamento automático, sem a necessidade de realizar manualmente cada tratamento diretamente no Excel.

Os dados originais podem conter inconsistências relacionadas a:

* Formatação;
* Datas;
* Nomes;
* Modelos;
* Cidades;
* Formas de pagamento;
* Valores monetários;
* Campos vazios ou inválidos;
* Padronização de texto;
* Tipos de dados.

Por esse motivo, a planilha original não deve ser utilizada diretamente como fonte final da Dashboard.

---

# 4. Schema

O arquivo:

```text
Schema
```

é utilizado como uma camada de definição das regras que orientam o processamento dos dados.

O Schema funciona como uma referência para o processo de sanitização, permitindo definir como os campos da planilha devem ser interpretados, transformados e apresentados após o tratamento.

De forma conceitual, o Schema estabelece a estrutura esperada dos dados e auxilia na definição das regras utilizadas pelo código Python responsável pelo ETL.

Entre as informações relevantes para o processamento estão campos relacionados a:

| Campo            | Descrição                 |
| ---------------- | ------------------------- |
| `sale_id`        | Identificador da venda    |
| `SaleDate`       | Data da venda             |
| `customer_name`  | Nome do cliente           |
| `PorscheModel`   | Modelo do veículo         |
| `ModelYear`      | Ano/model year do veículo |
| `SalesPrice`     | Valor da venda            |
| `VehicleMileage` | Quilometragem do veículo  |
| `PayMethod`      | Forma de pagamento        |
| `City`           | Cidade                    |
| `State`          | Estado                    |
| `salesperson`    | Vendedor                  |
| `DeliveryStatus` | Status da entrega         |

O Schema permite que o processo de transformação seja mais consistente e reproduzível.

---

# 5. Agente de Sanitização Porsche

A partir da combinação entre a planilha de origem, o Schema e as regras definidas para o tratamento dos dados, é gerado o:

```text
agente_sanitizacao_porsche
```

O agente representa a automação responsável pelo processamento da base.

Seu objetivo é executar as etapas necessárias para transformar os dados brutos em uma estrutura adequada para análise.

De maneira geral, o agente executa tarefas como:

1. Leitura da planilha de origem;
2. Identificação das colunas;
3. Validação dos dados;
4. Padronização dos campos;
5. Tratamento de valores inconsistentes;
6. Conversão dos tipos de dados;
7. Padronização de nomes e categorias;
8. Tratamento de datas inválidas;
9. Preparação dos campos para análise;
10. Geração da base sanitizada.

A utilização de Python permite que o processo seja executado de forma automatizada e repetível.

---

# 6. Transformação e sanitização dos dados

A etapa de transformação é responsável por melhorar a qualidade da base antes que os dados sejam utilizados pela Dashboard.

Um dos principais objetivos é garantir que cada coluna possua um padrão adequado para análise.

Os campos tratados recebem a nomenclatura sanitizada, como:

```text
SaleDateSanitized
PorscheModelSanitized
ModelYearSanitized
SalesPriceSanitized
VehicleMileageSanitized
PayMethodSanitized
CitySanitized
StateSanitized
DeliveryStatusSanitized
```

Essa abordagem facilita a identificação dos campos que passaram pelo processo de tratamento.

## 6.1. Tratamento de datas

Datas inválidas não devem ser artificialmente corrigidas ou inventadas.

Quando uma data não pode ser determinada com segurança, ela é mantida como:

```text
INVALID
```

Essa abordagem preserva a rastreabilidade do dado original e evita a criação de informações inexistentes.

A Dashboard, por sua vez, considera apenas datas válidas quando realiza análises temporais.

---

## 6.2. Padronização de valores

Os dados também são preparados para que possam ser agrupados corretamente.

Exemplos:

```text
PorscheModelSanitized
ModelYearSanitized
CitySanitized
PayMethodSanitized
```

Isso permite que diferentes registros sejam comparados e agrupados de maneira consistente.

---

## 6.3. Tratamento de valores financeiros

Os valores presentes em:

```text
SalesPriceSanitized
```

são utilizados para calcular indicadores financeiros, como:

* Receita total;
* Ticket médio;
* Receita por modelo;
* Receita por cidade;
* Receita por combinação de ano e modelo.

---

# 7. Planilha Porsche Sanitizada

O resultado do processo de ETL é:

```text
Planilha_Porsche_Sanitizada
```

Essa planilha representa a **base final preparada para consumo analítico**.

Ela funciona como a camada intermediária entre o processo de tratamento dos dados e a Dashboard.

A base sanitizada possui informações estruturadas que permitem realizar análises por:

* Modelo;
* Model Year;
* Cidade;
* Estado;
* Forma de pagamento;
* Data;
* Preço;
* Quilometragem;
* Status de entrega;
* Vendedor.

A Dashboard disponibilizada utiliza a base sanitizada como fonte para seus indicadores e visualizações.

---

# 8. Dashboard Porsche Sales Intelligence

A etapa final do projeto consiste na disponibilização dos dados tratados em uma Dashboard interativa:

**Porsche Sales Intelligence**

A aplicação pode ser acessada em:

[Porsche Sales Intelligence — Dashboard](https://porsche-insights-canvas.lovable.app/)

A Dashboard foi desenvolvida com foco em uma leitura executiva das vendas, permitindo analisar o desempenho por **modelo, cidade, período e método de pagamento**.

---

# 9. Filtros da Dashboard

A interface disponibiliza quatro filtros principais:

### Modelo da Porsche

Permite selecionar um modelo específico ou analisar todos os modelos disponíveis.

Exemplos:

```text
911
718
Cayenne
Macan
Taycan
Panamera
```

O filtro permite identificar o comportamento de determinado modelo dentro dos demais indicadores.

### Model Year

Permite analisar as vendas de acordo com o ano/model year do veículo.

Isso possibilita identificar quais combinações de ano e modelo apresentam maior volume.

### City

Permite selecionar uma cidade específica.

Esse filtro é importante para entender a distribuição geográfica das vendas e identificar os modelos mais relevantes em cada mercado.

### Payment Method

Permite analisar as vendas de acordo com a forma de pagamento utilizada.

A Dashboard disponibiliza, por exemplo, categorias como:

```text
Cash
Credit Card
Financing
Wire Transfer
Bank Transfer
Lease
ACH Payment
Crypto Payment
Debit Card
```

Os filtros são combináveis, permitindo análises mais específicas.

---

# 10. KPIs

A Dashboard apresenta indicadores-chave de desempenho que são recalculados conforme os filtros selecionados.

## 10.1. Unidades vendidas

Representa a quantidade de veículos existentes no recorte selecionado.

```text
Vendas = quantidade de registros filtrados
```

Esse indicador permite acompanhar o volume comercial.

---

## 10.2. Receita total

Representa a soma dos valores dos veículos vendidos no recorte analisado.

```text
Receita = Σ SalesPriceSanitized
```

Permite avaliar o impacto financeiro das vendas.

---

## 10.3. Ticket médio

Representa o valor médio dos veículos vendidos.

```text
Ticket Médio = Receita Total / Quantidade de Vendas
```

Esse indicador permite comparar não apenas volume de vendas, mas também o valor médio dos negócios.

---

## 10.4. Modelo líder

Identifica o modelo com maior quantidade de vendas dentro do recorte selecionado.

O modelo líder pode mudar conforme o usuário altera os filtros da Dashboard.

---

# 11. Principais visualizações

## 11.1. Modelos mais vendidos

Apresenta um ranking dos modelos com maior quantidade de unidades vendidas.

Essa visualização permite identificar rapidamente os veículos com maior participação no volume de vendas.

---

## 11.2. Performance por cidade

Apresenta o volume de vendas por cidade.

A visualização permite identificar mercados com maior concentração de vendas e comparar o desempenho entre localidades.

---

## 11.3. Ano × Modelo

Uma das análises mais importantes da Dashboard.

A visualização cruza:

```text
Model Year
        +
Porsche Model
```

permitindo identificar qual combinação apresenta maior quantidade de vendas.

Essa análise atende diretamente à pergunta de negócio:

> Qual ano e modelo de carro apresentou maior saída?

---

## 11.4. Métodos de pagamento

Apresenta a distribuição das vendas por forma de pagamento.

A visualização permite identificar quais modalidades são mais utilizadas pelos clientes.

---

# 12. Modelo campeão por cidade

A Dashboard também apresenta uma análise específica de liderança por cidade.

A tabela relaciona:

| Informação   | Objetivo                           |
| ------------ | ---------------------------------- |
| Cidade       | Identificar o mercado analisado    |
| Modelo líder | Identificar o Porsche mais vendido |
| Unidades     | Medir o volume                     |
| Receita      | Avaliar o impacto financeiro       |

Essa análise permite responder diretamente:

> Qual é o principal modelo de Porsche vendido em cada cidade?

A Dashboard disponibiliza exemplos de cidades como Atlanta, Las Vegas, New Orleans, Wichita, Boston, Dallas e Seattle, associando cada uma ao respectivo modelo líder no recorte analisado.

---

# 13. Insights automáticos

Além das visualizações, a solução possui uma camada de geração de insights.

Os insights são produzidos a partir do recorte atualmente selecionado e procuram destacar informações relevantes sobre:

### Popularidade

Identificação do modelo com maior volume de vendas.

### Cidade

Identificação da cidade com maior concentração de vendas e seu respectivo modelo de maior desempenho.

### Mix

Identificação da forma de pagamento dominante no conjunto filtrado.

Essa funcionalidade transforma os dados apresentados nos gráficos em informações mais fáceis de interpretar para usuários de negócio.

---

# 14. Tabela analítica

A Dashboard também apresenta uma tabela consolidada com informações como:

```text
Modelo
Cidade
Model Year
Vendas
Receita
```

Essa tabela complementa os gráficos e permite consultar os dados de maneira mais detalhada.

---

# 15. Perguntas de negócio atendidas

## Pergunta 1 — Quais são os principais modelos de carro vendidos por cidade?

A resposta pode ser obtida por meio do ranking de cidades e da análise do modelo líder por cidade.

O usuário pode selecionar uma cidade específica e verificar:

```text
Cidade
    ↓
Modelos vendidos
    ↓
Quantidade de vendas
    ↓
Modelo líder
```

---

## Pergunta 2 — Qual ano e modelo de carro mais saiu em determinado período?

A análise **Ano × Modelo** permite cruzar o Model Year com o modelo Porsche.

Quando existe uma análise temporal válida, o período pode ser utilizado para restringir o conjunto de registros e identificar a combinação com maior volume.

É importante observar que registros com datas inválidas não devem ser utilizados para construir artificialmente uma tendência temporal.

---

## Pergunta 3 — Quais são os carros mais populares em cada cidade?

A combinação dos filtros, ranking de modelos e análise de cidades permite identificar padrões locais de preferência.

Por exemplo:

```text
Cidade A → Modelo X
Cidade B → Modelo Y
Cidade C → Modelo Z
```

Essa informação pode apoiar decisões relacionadas a:

* Estoque;
* Campanhas comerciais;
* Planejamento de vendas;
* Distribuição de veículos;
* Estratégias regionais;
* Priorização de modelos.

---

# 16. Arquitetura da solução

A arquitetura lógica do projeto pode ser representada da seguinte maneira:

```text
┌───────────────────────────┐
│   Planilha Base Porsche   │
│       Dados brutos        │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│          Schema           │
│ Estrutura + regras ETL    │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Agente Sanitização Porsche│
│        Python / ETL       │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Planilha Porsche          │
│ Sanitizada                │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Porsche Sales Intelligence│
│       Dashboard           │
└───────────────────────────┘
```

---

# 17. Benefícios da solução

A solução proporciona:

* Automação do processo de ETL;
* Redução de tratamentos manuais;
* Padronização dos dados;
* Maior consistência das informações;
* Rastreabilidade dos dados inválidos;
* Reutilização do processo de sanitização;
* Preparação da base para ferramentas analíticas;
* Visualização executiva das vendas;
* Análise por modelo, cidade, ano e pagamento;
* Identificação de padrões de consumo;
* Geração automática de insights.

---

# 18. Tecnologias e conceitos utilizados

O projeto envolve conceitos e tecnologias relacionados a:

```text
Excel
Python
ETL
Data Cleaning
Data Sanitization
Schema
Business Intelligence
Data Visualization
KPIs
Data Analysis
Dashboard
Automação
```

A Dashboard utiliza uma interface web com visualizações interativas e atualização dos indicadores conforme os filtros são alterados. A implementação armazenada no projeto utiliza JavaScript e Chart.js para os gráficos.

---

# 19. Identificação dos arquivos

| Arquivo                       | Função                                                   |
| ----------------------------- | -------------------------------------------------------- |
| `Planilha base Porsche`       | Fonte original dos dados                                 |
| `Schema`                      | Define a estrutura e as regras utilizadas no tratamento  |
| `agente_sanitizacao_porsche`  | Automação responsável pelo processo de ETL e sanitização |
| `Planilha_Porsche_Sanitizada` | Base final tratada para análise                          |
| `porsche_sales_dashboard`     | Interface de visualização e análise dos dados            |

---

# 20. Fluxo operacional

Para executar o projeto de forma conceitual:

### Etapa 1 — Entrada

Disponibilizar a nova versão da:

```text
Planilha base Porsche
```

### Etapa 2 — Validação

Aplicar as regras estabelecidas pelo:

```text
Schema
```

### Etapa 3 — Processamento

Executar o:

```text
agente_sanitizacao_porsche
```

### Etapa 4 — Saída

Gerar:

```text
Planilha_Porsche_Sanitizada
```

### Etapa 5 — Análise

Disponibilizar a base sanitizada para a:

```text
Porsche Sales Intelligence
```

### Etapa 6 — Tomada de decisão

Utilizar os KPIs, gráficos, rankings e insights para identificar oportunidades comerciais.

---

# 21. Considerações sobre qualidade dos dados

A qualidade da Dashboard depende diretamente da qualidade da base sanitizada.

Por isso, recomenda-se que o processo de ETL seja executado sempre que uma nova versão da planilha de origem for disponibilizada.

Também é importante preservar os valores identificados como inválidos em vez de criar informações artificialmente.

Essa abordagem permite diferenciar:

```text
Dado válido
```

de:

```text
Dado não disponível ou inválido
```

e mantém a transparência do processo de tratamento.

---

# 22. Resultado esperado

Ao final do processo, o projeto disponibiliza uma solução completa de análise de vendas:

```text
DADOS BRUTOS
     ↓
EXTRAÇÃO
     ↓
TRANSFORMAÇÃO
     ↓
SANITIZAÇÃO
     ↓
BASE ANALÍTICA
     ↓
VISUALIZAÇÃO
     ↓
INSIGHTS
     ↓
DECISÃO
```

O resultado é uma estrutura que integra **tratamento automatizado de dados + base analítica + Business Intelligence**, permitindo transformar registros de vendas em informações úteis para análise comercial e tomada de decisão.

---

## 23. Dashboard

A versão online da Dashboard está disponível em:

[Acessar Porsche Sales Intelligence](https://porsche-insights-canvas.lovable.app/)

A interface apresenta uma abordagem executiva, com foco em desempenho de vendas, análise de mercado e identificação de padrões por modelo, cidade, período e forma de pagamento.

---

## 24. Status do projeto

**Pipeline de dados:** ETL automatizado
**Fonte:** Planilha Base Porsche
**Tratamento:** Agente de Sanitização Porsche
**Saída:** Planilha Porsche Sanitizada
**Visualização:** Porsche Sales Intelligence
**Objetivo:** Análise de desempenho e geração de insights comerciais
