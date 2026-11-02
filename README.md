# CineInsights · TMDB Analytics

App em Streamlit com dois dashboards construídos a partir da minha EDA do **TMDB 5000 Movie Dataset** (Kaggle). Projeto da prática de Streamlit (Aulas 21 a 23) da disciplina Análise e Visualização de Dados, CESAR School, 2026.2.

**Autora:** Julia Maria Santos Teixeira

**Link do app (Aula 23):** _(preencher após o deploy)_

## Sobre o app

O app tem duas abas.

### Dashboard 1: Correlação e distribuição
Um laboratório para explorar as 6 variáveis quantitativas dos filmes: `budget`, `revenue`, `popularity`, `runtime`, `vote_average` e `vote_count`.
- **Sidebar:** seletor das variáveis, um slider de intervalo para cada variável selecionada e um toggle para separar os filmes por classe (Bem avaliado ou Mal avaliado).
- **Heatmap de correlação de Spearman** entre as variáveis selecionadas. É Spearman porque nenhuma variável passou no Shapiro-Wilk na EDA.
- **Histograma** da variável escolhida, com as classes sobrepostas quando o toggle está ligado.

### Dashboard 2: Retorno do investimento
KPIs para um público de **produtoras e investidores** de cinema, respondendo à pergunta "vale a pena investir em um filme?".
- **Widgets:** filtro de décadas, filtro de classe e seletor da métrica mostrada no gráfico de barras.
- **4 métricas:** receita mediana, ROI mediano (receita ÷ orçamento), % de filmes que se pagaram e nota mediana.
- **3 visuais:** barras da métrica por década, dispersão orçamento × receita (escala log) e linha da receita e do orçamento medianos a cada 5 anos.

A justificativa de cada métrica está em [entregas/justificativa-metricas.md](entregas/justificativa-metricas.md).

## Organização do repositório

| Caminho | Conteúdo |
| --- | --- |
| `app.py` | O app (as duas abas) |
| `src/data_loader.py` | Leitura do dataset tratado, com cache |
| `data/clean/dataset.csv` | Dataset tratado, exportado pela EDA (4.739 filmes com pelo menos um voto) |
| `notebooks/eda.ipynb` | Minha EDA original (Aula 11) |
| `notebooks/eda-com-downloads.ipynb` | A EDA com o download pelo Kaggle e a exportação para `data/clean/` |
| `notebooks/arquivo-eda-original.ipynb` | Notebook de EDA da professora, mantido para consulta |
| `entregas/` | Rascunhos dos dois dashboards e justificativa das métricas |
| `prompts/` | Template de prompt e Declaração de Uso de IA |
| `tests/test_app.py` | Testes de borda do app com `AppTest` |
| `.streamlit/config.toml` | Identidade visual (tema claro e escuro) |

## Testes

Os testes simulam o uso do app sem abrir o navegador: 0, 1 e 2 ou mais variáveis selecionadas, intervalos que zeram o recorte, e as combinações de widgets dos dois dashboards. O `pytest` não está no `requirements.txt` porque o deploy não precisa dele. Com o venv ativo, rode na raiz do projeto:

```bash
python -m pip install pytest
python -m pytest tests/
```

## Uso de IA

O uso de IA está declarado em [prompts/declaracao-uso-ia.md](prompts/declaracao-uso-ia.md), e os trechos de código feitos com apoio de IA estão marcados com `# [IA]`.

## Setup

Requer **Python 3.11 a 3.15**. Confira a sua versão antes de começar:

| Sistema | Verificar versão |
| --- | --- |
| macOS / Linux | `python3 --version` |
| Windows | `py --version` |

### 1. Criar e ativar o ambiente virtual

O nome do comando do Python muda por sistema (em muitas máquinas `python` nem existe). Use a linha do seu sistema:

| Sistema | Criar | Ativar |
| --- | --- | --- |
| macOS / Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |
| Windows (PowerShell) | `py -m venv .venv` | `.venv\Scripts\Activate.ps1` |
| Windows (cmd) | `py -m venv .venv` | `.venv\Scripts\activate.bat` |

Se você tem várias versões instaladas, escolha uma compatível, por exemplo `python3.12 -m venv .venv` (macOS/Linux) ou `py -3.12 -m venv .venv` (Windows).

Com o ambiente ativo, o terminal mostra `(.venv)` no início da linha. **A partir daqui os comandos são iguais em todos os sistemas**, porque dentro do venv `python` e `pip` sempre existem.

### 2. Instalar, configurar a IA e rodar

```bash
python -m pip install -r requirements.txt

# Skills de IA do Streamlit (ver seção "IA neste projeto")
streamlit skills --yes

streamlit run app.py
```

### Problemas comuns

- **`python: command not found` / `python` não é reconhecido:** use `python3` (macOS/Linux) ou `py` (Windows) só para criar o venv; depois de ativado, `python` funciona.
- **Linux (Debian/Ubuntu): `ensurepip is not available` ou `No module named venv`:** instale `sudo apt install python3-venv` (ou `python3.X-venv` para a sua versão).
- **Windows: "a execução de scripts foi desabilitada" ao ativar no PowerShell:** rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, ou use o cmd.
- **Python fora de 3.11–3.15:** instale uma versão compatível em [python.org](https://www.python.org/downloads/) e crie o venv com ela, como no exemplo acima.
- **Apareceu `ModuleNotFoundError` ou `streamlit: command not found`:** o venv provavelmente não está ativo. Ative de novo e confira o `(.venv)` no prompt.
- **Erro de certificado no `pip install` (macOS, Python do python.org):** rode `Install Certificates.command`, na pasta Python 3.X em Aplicativos.
- **`DatasetNotFoundError` ao baixar o dataset no notebook (macOS, Python do python.org):** é o mesmo problema de certificado SSL (o `pandas` não consegue ler o CSV da UCI). Rode `Install Certificates.command` e reinicie o kernel. O notebook `eda-com-downloads.ipynb` já define `SSL_CERT_FILE` com o `certifi` como contorno.

## Estrutura de dados: `data/raw` vs `data/clean`

- `data/raw/`: o dataset **bruto**, como foi baixado. Nunca é editado à mão.
- `data/clean/`: o dataset **já tratado**, exportado na última célula do notebook de EDA (ex.: `df.to_csv("data/clean/dataset.csv", index=False)`). O `app.py` lê **somente** desta pasta, via `src/data_loader.py`.

### O que vai para o Git

| Pasta | Versionada? | Por quê |
| --- | --- | --- |
| `data/raw/` | **Não** (só o `.gitkeep`) | O bruto pode ser grande ou ter dados sensíveis, e o app não o usa. |
| `data/clean/` | **Sim** | O Streamlit Community Cloud faz deploy a partir do GitHub e só enxerga o que está no repositório. Sem o CSV tratado no repo, o app funciona na sua máquina e **quebra no deploy**. |

### Antes de dar `git push` com o dado tratado

- **O dado é público ou pode ser compartilhado?** Se não for claramente público, use um **repositório privado** (o Community Cloud permite conectar repositórios privados ao autorizar o GitHub; confirme na hora do deploy). Nesse caso, dê acesso de leitura ao professor (como colaborador ou pela organização).
- **Dado sensível** (nomes, CPF, e-mail, telefone, localização exata etc.): remova ou anonimize na EDA, antes de exportar para `data/clean/`. Isso vale mesmo em repositório privado.
- **Tamanho:** o GitHub rejeita arquivos acima de **100 MB**. Se o CSV tratado for grande, reduza colunas e linhas na EDA ou exporte em Parquet (`df.to_parquet(...)`, exige `pyarrow`).
- **Lembre de commitar o arquivo:** confira com `git status` que `data/clean/dataset.csv` aparece como novo arquivo.

## Passo a passo

O passo a passo detalhado de cada aula (Aulas 21, 22 e 23), com pré-requisitos e objetivos, está em [ROTEIRO.md](ROTEIRO.md). Comece por ele depois do Setup.

## IA neste projeto

Este projeto usa o **streamlit skills**: um conjunto de instruções (arquivos `SKILL.md`) que a ferramenta de IA lê para escrever código Streamlit seguindo boas práticas (estrutura de layout, cache, widgets, etc.).

**Como instalar:** depois do `pip install -r requirements.txt`, rode na raiz do projeto:

```bash
streamlit skills        # interativo
streamlit skills --yes  # sem confirmações
```

O comando cria *symlinks* para as skills que acompanham a sua instalação do Streamlit, então elas se atualizam sozinhas quando você atualiza o pacote. (A opção `--global` instala para todos os projetos, em vez de só este.)

**Onde fica instalado:**

- `.claude/skills/`: lido pelo Claude Code.
- `.agents/skills/`: lido pelo Gemini CLI, que já encontra essa pasta sozinho.

Essas pastas **não são versionadas** (ver `.gitignore`): os symlinks apontam para o seu ambiente virtual e não funcionam em outra máquina. Cada pessoa roda `streamlit skills` no próprio clone.

**Se você usa outra ferramenta** (ChatGPT, Copilot Chat, etc.): abra o `SKILL.md` correspondente em `.agents/skills/` e cole o conteúdo manualmente no início do chat, antes do seu pedido.

O uso de IA deve ser declarado conforme a seção abaixo.

## Pasta `prompts/`

A pasta [prompts/](prompts) guarda só o que é sobre **uso de IA**: o template de prompt para transformar o rascunho de layout em esqueleto de código e a **Declaração de Uso de IA** exigida pelo Plano de Ensino. Veja [prompts/README.md](prompts/README.md).

## Pasta `entregas/`

A pasta [entregas/](entregas) guarda os artefatos de entrega que não são sobre IA: os rascunhos de layout de cada dashboard (`.jpg` ou `.png`) e a justificativa das métricas do Dashboard 2. Veja [entregas/README.md](entregas/README.md) para o detalhe de cada arquivo e o checklist por aula. Não coloque esses arquivos no `.gitignore`.
