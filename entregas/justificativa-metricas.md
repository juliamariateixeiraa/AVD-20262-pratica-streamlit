# Justificativa das métricas — Dashboard 2

**Pergunta do dashboard:** vale a pena investir em um filme? Quanto um filme típico fatura, quanto devolve do que custou, e como isso varia entre décadas e entre filmes bem e mal avaliados?

**Variáveis selecionadas:** `budget`, `revenue` (financeiras), `vote_average` (recepção), `decada` (agrupamento) e `avaliacao` (classe).

**Escolha de estatística:** todas as métricas usam a **mediana**, e não a média. Na EDA nenhuma variável passou no Shapiro-Wilk, e `budget`/`revenue` são muito assimétricas. Exemplo: a média do ROI é 11,1×, puxada por casos como *Paranormal Activity* (US$ 15 mil de orçamento, US$ 193 mi de receita), enquanto a mediana é 2,3×. A mediana descreve o filme típico; a média descreve um filme que não existe.

**Base de cálculo:** filmes com `budget = 0` ou `revenue = 0` (ou < US$ 1.000) foram marcados como "não informado" na EDA e ficam de fora das métricas financeiras. As métricas de ROI e de "% que se pagou" usam só os filmes com orçamento **e** receita informados (3.209 de 4.739). O tamanho da base aparece no tooltip de cada KPI.

---

## Métrica 1: Receita mediana
- **Variável:** `revenue` (receita de bilheteria, em US$ milhões)
- **O que mede:** a receita do filme típico do recorte. Metade dos filmes faturou mais que esse valor e metade faturou menos. Considera só filmes com receita informada.
- **Por que foi escolhida:** é a medida de tamanho de mercado mais direta. Diz quanto dinheiro um filme costuma movimentar, sem ser distorcida pelos poucos blockbusters bilionários (o máximo é US$ 2,8 bi, de *Avatar*).
- **Público-alvo:** produtoras, investidores e financiadores de cinema.
- **Qual decisão pode ser apoiada por essa métrica?** Dimensionar a expectativa de receita de um projeto e comparar o porte de mercado entre décadas. Ex.: a receita mediana subiu de US$ 38,6 mi nos anos 1980 para US$ 67,0 mi nos 2010s (valores nominais).
- **O que comunica ao público-alvo:** "um filme típico deste recorte fatura cerca de US$ X milhões". É um número que se entende sem conhecer a distribuição de `revenue`.

## Métrica 2: ROI mediano
- **Variável:** `revenue ÷ budget` (derivada; lida como multiplicador, ex.: 2,3×)
- **O que mede:** quantas vezes o filme típico faturou o próprio orçamento. 1× = empatou, 2× = faturou o dobro do que custou.
- **Por que foi escolhida:** receita alta sozinha não diz se o investimento valeu a pena, porque um filme de US$ 300 mi que fatura US$ 400 mi rende menos que um de US$ 10 mi que fatura US$ 50 mi. O ROI coloca filmes de portes diferentes na mesma régua. É a métrica central do dashboard e por isso é a métrica padrão do gráfico de barras.
- **Público-alvo:** investidores e produtoras.
- **Qual decisão pode ser apoiada por essa métrica?** Comparar a eficiência do investimento entre recortes. Ex.: filmes bem avaliados têm ROI mediano de 2,95×, contra 1,72× dos mal avaliados. <!-- Julia: escreva aqui a sua leitura dessa diferença. -->
- **O que comunica ao público-alvo:** "o filme típico devolveu 2,3 vezes o que custou". Leitura imediata, sem precisar conhecer as escalas de `budget` e `revenue`.

## Métrica 3: % que se pagou
- **Variável:** `revenue` e `budget` (proporção de filmes com `revenue > budget`)
- **O que mede:** a parcela dos filmes do recorte cuja bilheteria superou o orçamento de produção.
- **Por que foi escolhida:** o ROI mediano mostra o caso típico, mas não o risco. Esta métrica responde "qual a chance de não perder dinheiro?". É uma taxa de sucesso, um formato que qualquer público entende.
- **Público-alvo:** investidores (foco em risco) e produtoras.
- **Qual decisão pode ser apoiada por essa métrica?** Avaliar o risco de um tipo de projeto. Ex.: 82% dos filmes bem avaliados se pagaram, contra 67% dos mal avaliados.
- **O que comunica ao público-alvo:** "3 em cada 4 filmes se pagaram". **Ressalva** (explicitada no tooltip): o orçamento do TMDB não inclui marketing e distribuição, e a bilheteria não vai inteira para a produtora. Então "se pagou" aqui é um limite otimista, não lucro real.

## Métrica 4: Nota mediana
- **Variável:** `vote_average` (nota média do público no TMDB, de 0 a 10)
- **O que mede:** a recepção do filme típico do recorte pelo público.
- **Por que foi escolhida:** fecha a leitura financeira com a dimensão de qualidade. Junto com o filtro de classe, permite ver se recortes que rendem mais também são mais bem recebidos. Também conecta o Dashboard 2 à classe `avaliacao` usada no Dashboard 1 (corte na mediana de `vote_average`).
- **Público-alvo:** produtoras (reputação do catálogo) e investidores.
- **Qual decisão pode ser apoiada por essa métrica?** Equilibrar retorno e reputação. Ex.: as décadas antigas têm nota mediana maior (7,0 antes de 1970, 6,1 nos 2010s).
- **O que comunica ao público-alvo:** "o filme típico deste recorte recebe nota X de 10 do público".

---

## Widgets que controlam o dashboard
- **Décadas (pills, múltipla escolha):** define o recorte de tempo. Permite, por exemplo, olhar só o cinema recente (2000s + 2010s), que é o mais comparável ao mercado atual.
- **Classe (segmented control: Todos / Bem avaliado / Mal avaliado):** isola filmes bem ou mal avaliados para comparar o retorno de cada grupo.
- **Métrica no gráfico (segmented control):** escolhe qual dos 4 KPIs o gráfico de barras mostra por década.

Os widgets do Dashboard 2 ficam dentro da aba. A sidebar controla só o Dashboard 1, para que os sliders de intervalo do Dashboard 1 não alterem os KPIs sem o usuário perceber.

## Visual: barras por década
A variável agrupada é `decada`: 6 grupos com ordem natural, o que deixa a evolução no tempo fácil de ler. Cada barra mostra a métrica escolhida naquela década, com o valor escrito na barra. A **linha tracejada** marca o valor do recorte inteiro, para comparar cada década com o todo.

## Limitações que o público deve conhecer
- **Valores nominais:** os valores não foram corrigidos pela inflação. Comparar receita entre décadas mostra tendência, não poder de compra.
- **Poucos filmes nas décadas antigas:** há 143 filmes antes de 1970 e 109 nos anos 1970, contra 2.034 nos 2000s. As métricas dessas décadas são calculadas sobre amostras pequenas. O tooltip das barras mostra quantos filmes há em cada década. <!-- Julia: se quiser, escreva aqui a sua leitura de por que essas décadas aparecem com ROI e nota mais altos. -->
