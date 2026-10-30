# Template: rascunho de layout → esqueleto do app

> **Nota:** o prompt original usado na Aula 21 não foi salvo. Este é uma reconstrução feita na Aula 22, a partir do rascunho do layout e do esqueleto do `app.py` que foi gerado.

## Contexto

Sou aluna da disciplina de Análise e Visualização de Dados (CESAR School, 2026.2) e estou construindo um app em Streamlit a partir da EDA que fiz na Aula 11. O dataset é o **TMDB 5000 Movies** (Kaggle), já tratado e exportado em `data/clean/dataset.csv` (4.739 filmes com pelo menos um voto). O objetivo do Dashboard 1 é explorar a **correlação** e a **distribuição** das variáveis quantitativas dos filmes.

## Entrada

Rascunho do layout: `entregas/prof_rascunho_dashboard1.png` (imagem anexada).

Layout: sidebar à esquerda com os filtros (variáveis + intervalo); na área principal, um card de correlação (heatmap) à esquerda e um card de distribuição (histograma) à direita, mais largo.

Colunas do dataset:
- Quantitativas: `budget`, `revenue`, `popularity`, `runtime`, `vote_average`, `vote_count`
- Categóricas: `avaliacao` (Bem avaliado / Mal avaliado, corte na mediana de `vote_average`), `decada`, `orcamento_tier`, `idioma_grp`
- Flags: `orcamento_informado`, `receita_informada`

Perguntas que o dashboard deve responder:
- Quais variáveis quantitativas se relacionam entre si, e com que força?
- Como os valores de cada variável se distribuem, e essa distribuição muda entre filmes bem e mal avaliados?

## Restrições

- Usar Streamlit, editando só o `app.py`.
- Carregar os dados por `src/data_loader.py` (`load_data()`, com `@st.cache_data`), com caminho relativo.
- Ter pelo menos **1 seletor de variáveis** (multiselect das 6 quantitativas) e **1 slider de intervalo** por variável selecionada. `budget` e `revenue` devem aparecer em US$ milhões.
- Ter um toggle para distinguir a distribuição pela classe `avaliacao`.
- A correlação deve ser de **Spearman**, porque nenhuma variável passou no Shapiro-Wilk na EDA.
- Mostrar avisos quando não der para calcular: menos de 2 variáveis para a correlação, 0 variáveis para a distribuição.
- Ainda **não** implementar os gráficos: no lugar deles, deixar placeholders.
- Seguir a Skill oficial do Streamlit (`streamlit skills`): widgets nativos, ícones Material, sem `use_container_width`.

## Formato de saída

Código completo do `app.py` com o esqueleto: sidebar com os widgets funcionando, cabeçalho, uma linha de métricas de contexto (filmes no recorte, variáveis ativas, método de correlação) e os dois cards com placeholders e comentários `# TODO` onde os gráficos vão entrar. Incluir uma explicação breve de cada seção.
