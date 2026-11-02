# Justificativa das métricas: Dashboard 2

**Pergunta do dashboard:** vale a pena investir em um filme? Quanto um filme típico fatura, quanto ele devolve do que custou, e como isso muda entre as décadas e entre filmes bem e mal avaliados?

**Variáveis selecionadas:** `budget` e `revenue` (financeiras), `vote_average` (recepção do público), `decada` (agrupamento) e `avaliacao` (classe).

**Por que mediana:** usei a mediana em todas as métricas porque, na EDA, nenhuma variável passou no teste de Shapiro-Wilk, e `budget` e `revenue` são bem assimétricas. A média do ROI, por exemplo, dá 11,1×, puxada por casos como *Paranormal Activity* (US$ 15 mil de orçamento e US$ 193 mi de receita), enquanto a mediana dá 2,3×. Ou seja, a mediana mostra como é um filme típico, e a média acaba descrevendo um filme que não existe.

**Quais filmes entram no cálculo:** filmes com `budget` ou `revenue` igual a 0 (ou abaixo de US$ 1.000) foram marcados como "não informado" na EDA e ficam de fora das métricas financeiras. O ROI e o "% que se pagou" usam só os filmes que têm orçamento e receita informados (3.209 de 4.739). O tooltip de cada KPI mostra quantos filmes entraram na conta.

---

## Métrica 1: Receita mediana
- **Variável:** `revenue` (receita de bilheteria, em US$ milhões)
- **O que mede:** quanto fatura o filme típico do recorte. Metade dos filmes faturou mais que esse valor e a outra metade faturou menos. Só entram filmes com receita informada.
- **Por que foi escolhida:** é o jeito mais direto de ver o tamanho do mercado. Mostra quanto dinheiro um filme costuma movimentar, sem ser distorcida pelos poucos blockbusters bilionários (o maior é *Avatar*, com US$ 2,8 bi).
- **Público-alvo:** produtoras, investidores e financiadores de cinema.
- **Qual decisão pode ser apoiada por essa métrica?** Ter uma noção de quanto um projeto pode faturar e comparar o tamanho do mercado entre décadas. Por exemplo, a receita mediana subiu de US$ 38,6 mi nos anos 1980 para US$ 67,0 mi nos anos 2010 (valores nominais).
- **O que comunica ao público-alvo:** "um filme típico deste recorte fatura cerca de US$ X milhões". Dá para entender esse número sem conhecer a distribuição de `revenue`.

## Métrica 2: ROI mediano
- **Variável:** `revenue ÷ budget` (variável derivada, lida como multiplicador, ex.: 2,3×)
- **O que mede:** quantas vezes o filme típico faturou o próprio orçamento. 1× significa que empatou, e 2× que faturou o dobro do que custou.
- **Por que foi escolhida:** só a receita não diz se o investimento valeu a pena. Um filme de US$ 300 mi que fatura US$ 400 mi rende menos que um de US$ 10 mi que fatura US$ 50 mi. Com o ROI, dá para comparar filmes de tamanhos diferentes. Ela é a métrica principal do dashboard, por isso já aparece selecionada no gráfico de barras.
- **Público-alvo:** investidores e produtoras.
- **Qual decisão pode ser apoiada por essa métrica?** Comparar qual recorte dá mais retorno sobre o investimento. Os filmes bem avaliados têm ROI mediano de 2,95×, contra 1,72× dos mal avaliados, ou seja, cada real investido em um filme bem avaliado retorna, na mediana, cerca de 70% a mais. Isso sugere que a qualidade percebida pesa no retorno, e não só o tamanho do orçamento, o que pode justificar investir mais em roteiro e desenvolvimento em vez de só aumentar a verba de produção. Mas tem uma ressalva: a avaliação só existe depois do lançamento, então a métrica mostra uma associação, não uma causa, e sozinha não serve para prever o retorno de um projeto antes de ele sair. Usar a mediana também ajuda a evitar que poucos sucessos fora da curva distorçam a comparação.
- **O que comunica ao público-alvo:** "o filme típico devolveu 2,3 vezes o que custou". É fácil de entender mesmo sem conhecer as escalas de `budget` e `revenue`.

## Métrica 3: % que se pagou
- **Variável:** `revenue` e `budget` (proporção de filmes com `revenue > budget`)
- **O que mede:** a parcela dos filmes do recorte em que a bilheteria superou o orçamento de produção.
- **Por que foi escolhida:** o ROI mediano mostra o caso típico, mas não mostra o risco. Esta métrica responde à pergunta "qual a chance de não perder dinheiro?". Como é uma taxa de sucesso, qualquer público consegue entender.
- **Público-alvo:** investidores (principalmente pelo risco) e produtoras.
- **Qual decisão pode ser apoiada por essa métrica?** Avaliar o risco de um tipo de projeto. Por exemplo, 82% dos filmes bem avaliados se pagaram, contra 67% dos mal avaliados.
- **O que comunica ao público-alvo:** "3 em cada 4 filmes se pagaram". **Ressalva** (que também está no tooltip): o orçamento do TMDB não inclui marketing e distribuição, e a bilheteria não vai inteira para a produtora. Então "se pagou" aqui é uma visão otimista, não lucro real.

## Métrica 4: Nota mediana
- **Variável:** `vote_average` (nota média do público no TMDB, de 0 a 10)
- **O que mede:** como o público recebeu o filme típico do recorte.
- **Por que foi escolhida:** completa a parte financeira com a qualidade. Junto com o filtro de classe, permite ver se os recortes que rendem mais também são os mais bem recebidos. Ela também liga o Dashboard 2 à classe `avaliacao` usada no Dashboard 1 (corte na mediana de `vote_average`).
- **Público-alvo:** produtoras (reputação do catálogo) e investidores.
- **Qual decisão pode ser apoiada por essa métrica?** Equilibrar retorno e reputação. Por exemplo, as décadas antigas têm nota mediana maior (7,0 antes de 1970, contra 6,1 nos anos 2010).
- **O que comunica ao público-alvo:** "o filme típico deste recorte recebe nota X de 10 do público".

---

## Widgets que controlam o dashboard
- **Décadas (pills, múltipla escolha):** define o período analisado. Dá para olhar só o cinema mais recente (2000s + 2010s), por exemplo, que é o mais comparável ao mercado atual.
- **Classe (segmented control: Todos / Bem avaliado / Mal avaliado):** separa os filmes bem ou mal avaliados para comparar o retorno de cada grupo.
- **Métrica no gráfico (segmented control):** escolhe qual dos 4 KPIs aparece por década no gráfico de barras.

Os widgets do Dashboard 2 ficam dentro da própria aba, e a sidebar controla só o Dashboard 1. Assim, os sliders do Dashboard 1 não mudam os KPIs sem o usuário perceber.

## Visuais

Os três visuais respondem aos mesmos widgets de décadas e classe que as métricas.

### 1. Barras por década
A variável agrupada é `decada`, com 6 grupos em ordem natural, o que facilita ver a evolução no tempo. Cada barra mostra a métrica escolhida naquela década, com o valor escrito nela. A linha tracejada marca o valor do recorte inteiro, para comparar cada década com o todo.

### 2. Dispersão orçamento × receita
- **Variáveis:** `budget` (eixo X) e `revenue` (eixo Y), em US$ milhões, com cor pela classe `avaliacao`.
- **O que mostra:** cada ponto é um filme. A linha tracejada marca onde a receita é igual ao orçamento (ROI = 1×): quem está acima dela se pagou, e quem está abaixo não. É a métrica "% que se pagou" vista filme a filme.
- **Por que escala log:** orçamento e receita vão de milhares a bilhões de dólares. Em escala linear, quase todos os filmes ficariam espremidos em um canto do gráfico.
- **Filmes considerados:** só os que têm orçamento e receita informados. O tooltip mostra título, ano, valores e ROI.

### 3. Linha de receita e orçamento no tempo
- **Variáveis:** `revenue` e `budget` (medianas, em US$ milhões) por `release_date`.
- **O que mostra:** a receita mediana e o orçamento mediano ao longo do tempo, no mesmo eixo, para comparar as duas linhas.
- **Por que lustros (5 anos) e não anos:** antes de 1970, muitos anos têm só de 1 a 3 filmes, então um único filme virava a mediana do ano e criava picos que não significavam nada. Agrupando de 5 em 5 anos, cada ponto tem mais filmes. O tooltip mostra quantos.

## Limitações que o público deve conhecer
- **Valores nominais:** os valores não foram corrigidos pela inflação. Comparar a receita entre décadas mostra a tendência, não o poder de compra.
- **Poucos filmes nas décadas antigas:** são 143 filmes antes de 1970 e 109 nos anos 1970, contra 2.034 nos anos 2000. Ou seja, as métricas dessas décadas vêm de amostras pequenas, e o tooltip das barras mostra quantos filmes há em cada uma. Na minha leitura, o ROI e a nota mais altos dessas décadas são um viés de sobrevivência, e não um sinal de que os filmes antigos eram, em geral, melhores ou mais rentáveis. Os filmes antigos que chegam a um catálogo como este são justamente os que ficaram na memória: clássicos, sucessos e títulos que continuaram sendo vistos, relançados e catalogados. Já a maioria das produções medianas da época nem está na base ou não tem orçamento e bilheteria registrados. Além disso, os relançamentos podem inflar a receita acumulada, e, com tão poucos filmes, alguns de destaque já puxam a mediana para cima. Por isso, a comparação entre décadas precisa ser lida com cautela, principalmente antes de 1980.