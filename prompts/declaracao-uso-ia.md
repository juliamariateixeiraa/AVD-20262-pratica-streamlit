# Declaração de Uso de IA

**Nome:** Julia Maria Santos Teixeira
**Data:** 30/10/2026 (Aula 22)

## Ferramenta

- **Claude Code** (modelo Claude Opus 5.5), na extensão do VS Code.
- **Skill oficial do Streamlit: SIM, utilizada.** A skill `developing-with-streamlit` foi instalada com `streamlit skills --yes` (fica em `.claude/skills/`) e orientou a IA a gerar código no padrão da biblioteca (ex.: `st.tabs`, `st.pills`, `st.segmented_control`, `st.metric`, `@st.cache_data`, testes com `AppTest`).

Os trechos de código feitos com apoio de IA estão marcados no próprio código com `# [IA] <ferramenta> – <finalidade>` em `app.py`, `src/data_loader.py`, `tests/test_app.py` e `.streamlit/config.toml`. Cada marcação indica se o trecho é da Aula 21 ou da Aula 22.


## Aula 21

- Esqueleto do `app.py` (sidebar com seletor de variáveis, toggle de classe e sliders de intervalo; cabeçalho; métricas de contexto) gerado com apoio de IA a partir do rascunho do layout.
- Identidade visual (`.streamlit/config.toml` e CSS do cabeçalho) feita com apoio de IA.

## Aula 22

Usos, dentro do que é permitido:
- **Atualização do repositório:** conferir se havia mudanças novas no repositório da professora (`git fetch upstream`). Não havia, porque o merge já tinha sido feito.
- **Sintaxe Altair:** código do heatmap de Spearman, do histograma (com separação por classe) e do gráfico de barras por década.
- **Identidade visual:** cores dos gráficos alinhadas ao tema já existente (coral = Bem avaliado, azul = Mal avaliado), nos temas claro e escuro.
- **Cálculo das métricas** do Dashboard 2 (receita mediana, ROI mediano, % que se pagou, nota mediana) e redação da `entregas/justificativa-metricas.md`.
- **Testes de borda** do Dashboard 1 e do Dashboard 2 (`tests/test_app.py`, 38 casos: 0, 1 e 2+ variáveis e combinações de widgets).
- **Rascunho do Dashboard 2:** wireframe gerado em `entregas/rascunho-dashboard2.jpg`.
- **Rascunho do Dashboard 1:** wireframe gerado em `entregas/rascunho-dashboard1.jpg`. Ele estava pendente desde a Aula 21 e foi feito na Aula 22, depois da implementação, a partir do layout já combinado (o rascunho da professora + o esqueleto da Aula 21).
- **Organização do repositório:** os notebooks foram renomeados para os papéis que o roteiro pede (`eda.ipynb` = EDA original, `eda-com-downloads.ipynb` = com download e exportação), e o notebook da professora foi recuperado em `arquivo-eda-original.ipynb`.
- **Template de prompt da Aula 21:** `prompts/layout-skeleton-prompt.md` foi reconstruído com apoio de IA, porque o prompt original não foi salvo. O arquivo tem uma nota dizendo isso.
- **Justificativa das métricas:** a IA ajudou a calcular as métricas e a redigir o texto. As frases de interpretação dos resultados foram retiradas do texto da IA e são minhas.
- **Depuração:** investigação de números divergentes no app (a causa era um servidor Streamlit antigo, ainda rodando com dados velhos em cache).

## Aula 23

- **Conferência dos requisitos:** a IA comparou o projeto com a lista de requisitos da atividade e apontou que o Dashboard 2 tinha 1 visual, e o mínimo é 3.
- **Escolha dos visuais:** a IA listou as opções possíveis com os dados, com prós e contras, **sem recomendar nenhuma**. Escolhi a dispersão orçamento × receita e a linha de receita/orçamento no tempo. Também decidi manter o histograma do Dashboard 1 com o selectbox (um de cada vez) e agrupar a linha do tempo por lustro, para evitar os picos dos anos com poucos filmes.
- **Sintaxe Altair** dos dois visuais novos, ajustes visuais (grade da escala log e rótulos dos eixos) e novos testes de borda (`tests/test_app.py`, agora com 45 casos).
- **README:** a IA escreveu as seções que descrevem o projeto (sobre o app, organização do repositório, testes e uso de IA). O resto do README é o modelo da professora.
- **Rascunho do Dashboard 2** atualizado com os dois visuais novos, e a seção "Visuais" da justificativa descrevendo o que cada gráfico mostra.

## O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:**
  - **As decisões, incluindo a escolha das métricas, foram minhas, tomadas a partir de um debate com a IA.** Em outra conversa, eu levei as minhas próprias opções e discuti com a IA:
    - o que ela achava da minha opção e se fazia sentido;
    - por que ela recomendava outra opção e não a minha;
    - as vantagens e desvantagens de cada uma, e o impacto nos testes e na leitura do dashboard.

    Em alguns pontos acabei indo com a opção que a IA recomendava, mas só depois de entender os motivos e concordar com eles. Não aceitei recomendações sem questionar. Escolhi:
    - manter a identidade visual da Aula 21;
    - usar Altair no Dashboard 1 (preferido no roteiro e obrigatório no Dashboard 2, para manter consistência);
    - heatmap de Spearman + histograma no Dashboard 1, seguindo o rascunho da Aula 21;
    - público "produtora/investidor" no Dashboard 2;
    - agrupamento por década no gráfico de barras;
    - widgets de décadas, classe e métrica do gráfico.
  - Tratar `budget`/`revenue` não informados (zeros) como ausentes no app. Isso segue as próprias marcações de "não informado" da EDA e evita um pico falso em zero no histograma e distorção na correlação.
  - Uso da mediana em todas as métricas, coerente com a EDA (nenhuma variável passou no Shapiro-Wilk).
- **Modificado:**
  - A primeira versão do heatmap escondia metade dos rótulos do eixo X e cortava `vote_average`. Os rótulos foram ajustados e a legenda foi para baixo.
  - Na primeira versão do gráfico de barras, a linha de referência cobria os valores. Os rótulos passaram para dentro do topo das barras.
  - O wireframe do Dashboard 2 tinha textos sobrepostos e foi corrigido.
  - Os números das métricas foram conferidos com um cálculo independente fora do Streamlit antes de aceitar.
- **Rejeitado:**
  - Crossfilter (clicar na barra filtra os KPIs): ficou para a Aula 23, para fechar antes as entregas obrigatórias.
  - Visual extra de dispersão no Dashboard 1 e troca do histograma por boxplot: o heatmap + histograma já responde às perguntas do rascunho com menos widgets para testar.
