import math

import altair as alt
import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="CineInsights | TMDB Analytics",
    page_icon=":material/movie:",
    layout="wide",
)

# [IA] Claude Code + Skill oficial do Streamlit – identidade visual: CSS do cabeçalho (Aula 21)
# Refinamento pontual: só a classe gerada por key= (estável), sem classes internas do Streamlit
st.html(
    """
    <style>
    /* Cores translúcidas: funcionam tanto no tema claro quanto no escuro */
    .st-key-hero {
        background:
            radial-gradient(120% 140% at 100% 0%, rgba(240, 84, 90, 0.20) 0%, rgba(240, 84, 90, 0) 55%),
            linear-gradient(135deg, rgba(120, 135, 175, 0.12) 0%, rgba(120, 135, 175, 0) 100%);
        border: 1px solid rgba(120, 135, 175, 0.28);
        border-radius: 18px;
        padding: 1.75rem 2rem;
    }
    </style>
    """
)

df = load_data()

# [IA] Claude Code + Skill oficial do Streamlit – esqueleto do app a partir do rascunho (Aula 21)
# Variáveis quantitativas do estudo (mesma lista VARS_QUANT do notebook de EDA)
VARS_QUANT = ["budget", "revenue", "popularity", "runtime", "vote_average", "vote_count"]

# budget e revenue chegam a bilhões: sliders e gráficos mostram em US$ milhões para ficarem legíveis
ESCALA = {"budget": 1_000_000, "revenue": 1_000_000}

# [IA] Claude Code + Skill oficial do Streamlit – constantes de classe e ordem das décadas (Aula 22)
CLASSES = ["Bem avaliado", "Mal avaliado"]
ORDEM_DECADAS = ["pre-1970", "1970s", "1980s", "1990s", "2000s", "2010s"]

# [IA] Claude Code + Skill oficial do Streamlit – identidade visual: cores dos gráficos alinhadas ao tema (Aula 22)
# Mesmas cores do .streamlit/config.toml, para os gráficos acompanharem o tema claro/escuro
TEMA_ESCURO = st.context.theme.type == "dark"
CORAL = "#F2545B" if TEMA_ESCURO else "#E5484D"  # Bem avaliado / destaque
AZUL = "#6A93DE" if TEMA_ESCURO else "#4F79C4"  # Mal avaliado
NEUTRO = "#1B2238" if TEMA_ESCURO else "#EEF0F6"  # centro da escala divergente (ρ = 0)
TEXTO = "#E9ECF5" if TEMA_ESCURO else "#0B1020"
CINZA = "#9AA3B8" if TEMA_ESCURO else "#8B93A7"  # séries secundárias (orçamento na linha do tempo)
CORES_CLASSE = alt.Scale(domain=CLASSES, range=[CORAL, AZUL])


# [IA] Claude Code + Skill oficial do Streamlit – esqueleto: limites dos sliders e formatação (Aula 21)
def limites_slider(serie):
    """Mínimo, máximo e passo do slider de intervalo de uma variável."""
    # runtime é inteiro, mas vem como float por causa dos NaN (runtime == 0 tratado na EDA)
    if serie.dropna().mod(1).eq(0).all():
        return int(serie.min()), int(serie.max()), 1
    return math.floor(serie.min() * 10) / 10, math.ceil(serie.max() * 10) / 10, 0.1


def formatar_inteiro(n):
    return f"{n:,}".replace(",", ".")


# [IA] Claude Code + Skill oficial do Streamlit – formatação de números e rótulos (Aula 22)
def formatar_decimal(x, casas=1):
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def rotulo_variavel(var):
    return f"{var} (US$ mi)" if var in ESCALA else var


# [IA] Claude Code + Skill oficial do Streamlit – cálculo da matriz de Spearman em formato longo para o Altair (Aula 22)
@st.cache_data(max_entries=50)
def matriz_spearman(dados):
    """Correlação de Spearman em formato longo (uma linha por par), pronta para o heatmap."""
    # Pares com valor ausente (budget/revenue não informados, runtime faltando) são ignorados par a par
    corr = dados.corr(method="spearman")
    longo = corr.reset_index(names="var_x").melt(id_vars="var_x", var_name="var_y", value_name="rho")
    longo["rotulo"] = longo["rho"].map(lambda r: "—" if pd.isna(r) else f"{r:.2f}")
    return longo


# [IA] Claude Code + Skill oficial do Streamlit – esqueleto: sidebar com seletor de variáveis, toggle e sliders (Aula 21)
# Sidebar: filtros do Dashboard 1 (variáveis + intervalo)
with st.sidebar:
    st.header("Filtros", icon=":material/tune:")
    st.caption("Definem o recorte de filmes da aba **Correlação e distribuição**.")

    variaveis = st.multiselect(
        "Variáveis quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT,
        help="Selecione as variáveis quantitativas que deseja analisar no dashboard.",
    )

    separar_por_classe = st.toggle(
        "Distinguir por classe",
        value=False,
        help="Separa a distribuição pela classe (avaliacao: Bem avaliado ou Mal avaliado, corte na mediana de vote_average).",
    )

    # Um slider de intervalo para cada variável selecionada
    intervalos = {}
    for var in variaveis:
        minimo, maximo, passo = limites_slider(df[var] / ESCALA.get(var, 1))
        intervalos[var] = st.slider(
            f"Intervalo de {rotulo_variavel(var)}",
            min_value=minimo,
            max_value=maximo,
            value=(minimo, maximo),
            step=passo,
            format="%d" if passo == 1 else "%.1f",
            key=f"intervalo_{var}",
        )

# [IA] Claude Code + Skill oficial do Streamlit – esqueleto: aplicação dos filtros de intervalo (Aula 21)
# Mantém só os filmes dentro de todos os intervalos escolhidos.
# Filmes sem valor (runtime, budget ou revenue ausente) só saem quando o intervalo daquela variável é estreitado.
df_filtrado = df
for var, (inicio, fim) in intervalos.items():
    valores = df_filtrado[var] / ESCALA.get(var, 1)
    minimo, maximo, _ = limites_slider(df[var] / ESCALA.get(var, 1))
    dentro = valores.between(inicio, fim)
    if (inicio, fim) == (minimo, maximo):
        dentro |= valores.isna()
    df_filtrado = df_filtrado[dentro]

# [IA] Claude Code + Skill oficial do Streamlit – esqueleto: cabeçalho (Aula 21)
# Cabeçalho
with st.container(key="hero", gap="small"):
    st.badge("TMDB Analytics", icon=":material/movie:", color="primary")
    st.title("CineInsights")
    st.markdown("Correlação, distribuição e retorno financeiro dos filmes do **TMDB 5000 Movies**.")

st.space("small")

# [IA] Claude Code + Skill oficial do Streamlit – abas separando os dois dashboards (Aula 22)
aba_d1, aba_d2 = st.tabs(
    [":material/grid_on: Correlação e distribuição", ":material/payments: Retorno do investimento"]
)

# Dashboard 1: correlação e distribuição
with aba_d1:
    # [IA] Claude Code + Skill oficial do Streamlit – esqueleto: métricas de contexto do recorte (Aula 21)
    # Contexto do recorte atual
    col_filmes, col_variaveis, col_metodo = st.columns(3, gap="medium")
    with col_filmes:
        st.metric(
            "Filmes no recorte",
            formatar_inteiro(len(df_filtrado)),
            help=f"De {formatar_inteiro(len(df))} filmes com pelo menos um voto, após o tratamento da EDA.",
            icon=":material/movie_filter:",
            border=True,
        )
    with col_variaveis:
        st.metric(
            "Variáveis ativas",
            f"{len(variaveis)} de {len(VARS_QUANT)}",
            icon=":material/tune:",
            border=True,
        )
    with col_metodo:
        st.metric(
            "Método de correlação",
            "Spearman",
            help="Nenhuma variável passou no Shapiro-Wilk na EDA, por isso a correlação é de postos (Spearman).",
            icon=":material/functions:",
            border=True,
        )

    # Correlação (heatmap) à esquerda, distribuição (histograma) à direita
    col_correlacao, col_distribuicao = st.columns([1, 1.5], gap="medium")

    with col_correlacao:
        with st.container(border=True, height="stretch"):
            st.subheader("Correlação", icon=":material/grid_on:")
            st.caption("Força da relação monotônica entre as variáveis selecionadas.")

            if len(variaveis) < 2:
                st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.", icon=":material/warning:")
            elif len(df_filtrado) < 3:
                st.warning("Poucos filmes dentro dos intervalos para calcular a correlação.", icon=":material/warning:")
            else:
                # [IA] Claude Code + Skill oficial do Streamlit – sintaxe Altair do heatmap de correlação (Aula 22)
                corr = matriz_spearman(df_filtrado[variaveis])
                base = alt.Chart(corr).encode(
                    x=alt.X("var_x:N", sort=variaveis, title=None, axis=alt.Axis(labelAngle=-35, labelOverlap=False)),
                    y=alt.Y("var_y:N", sort=variaveis, title=None, axis=alt.Axis(labelLimit=200)),
                )
                celulas = base.mark_rect(cornerRadius=4, stroke=NEUTRO, strokeWidth=2).encode(
                    color=alt.Color(
                        "rho:Q",
                        title="ρ",
                        scale=alt.Scale(domain=[-1, 0, 1], range=[AZUL, NEUTRO, CORAL]),
                        legend=alt.Legend(orient="bottom", direction="horizontal", gradientLength=220),
                    ),
                    tooltip=[
                        alt.Tooltip("var_x:N", title="Variável"),
                        alt.Tooltip("var_y:N", title="Variável"),
                        alt.Tooltip("rotulo:N", title="ρ de Spearman"),
                    ],
                )
                # Texto branco nas células escuras (|ρ| alto), cor do tema nas claras
                textos = base.mark_text(fontSize=13, fontWeight=500).encode(
                    text="rotulo:N",
                    color=alt.condition("abs(datum.rho) > 0.6", alt.value("white"), alt.value(TEXTO)),
                )
                st.altair_chart(
                    (celulas + textos).properties(height=380),
                    alt="Heatmap da correlação de Spearman entre as variáveis selecionadas",
                )
                if corr["rho"].isna().any():
                    st.caption("— : variável sem variação no recorte, correlação indefinida.")

    with col_distribuicao:
        with st.container(border=True, height="stretch"):
            st.subheader("Distribuição", icon=":material/bar_chart:")
            st.caption("Como os valores de uma variável se espalham entre os filmes do recorte.")

            if not variaveis:
                st.warning("Selecione pelo menos 1 variável para ver a distribuição.", icon=":material/warning:")
            else:
                # [IA] Claude Code + Skill oficial do Streamlit – sintaxe Altair do histograma e tratamento de casos de borda (Aula 22)
                var_hist = st.selectbox("Variável do histograma", options=variaveis)
                dados_hist = df_filtrado[[var_hist, "avaliacao"]].dropna()
                dados_hist[var_hist] = dados_hist[var_hist] / ESCALA.get(var_hist, 1)

                if dados_hist.empty:
                    st.warning("Nenhum filme com valor dessa variável no recorte.", icon=":material/warning:")
                else:
                    if separar_por_classe:
                        # Classes sobrepostas (sem empilhar) para comparar o formato das duas distribuições
                        cor = alt.Color("avaliacao:N", title="Classe", scale=CORES_CLASSE, legend=alt.Legend(orient="top"))
                        barras = alt.Chart(dados_hist).mark_bar(opacity=0.6, binSpacing=1).encode(color=cor)
                    else:
                        barras = alt.Chart(dados_hist).mark_bar(color=CORAL, binSpacing=1)

                    histograma = barras.encode(
                        x=alt.X(f"{var_hist}:Q", bin=alt.Bin(maxbins=40), title=rotulo_variavel(var_hist)),
                        y=alt.Y("count():Q", title="Filmes", stack=None),
                        tooltip=[
                            alt.Tooltip(f"{var_hist}:Q", bin=alt.Bin(maxbins=40), title=rotulo_variavel(var_hist)),
                            alt.Tooltip("count():Q", title="Filmes"),
                        ],
                    ).properties(height=380)
                    st.altair_chart(histograma, alt=f"Histograma de {var_hist}")

                    fora = len(df_filtrado) - len(dados_hist)
                    if fora:
                        st.caption(f"{formatar_inteiro(fora)} filmes do recorte sem {var_hist} informado ficam de fora.")

    st.caption("Fonte: TMDB 5000 Movie Dataset (Kaggle) · Tratamento: notebooks/eda-com-downloads.ipynb")


# [IA] Claude Code + Skill oficial do Streamlit – cálculo das métricas do Dashboard 2 (Aula 22)
# Dashboard 2: KPIs de retorno do investimento (público: produtora/investidor)
METRICAS_D2 = {
    "Receita mediana": "receita",
    "ROI mediano": "roi",
    "% que se pagou": "pagou",
    "Nota mediana": "nota",
}


@st.cache_data(max_entries=50)
def kpis(dados):
    """KPIs do Dashboard 2. As financeiras só usam filmes com budget e revenue informados."""
    fin = dados.dropna(subset=["budget", "revenue"])
    roi = fin["revenue"] / fin["budget"]
    return {
        "receita": dados["revenue"].median() / ESCALA["revenue"],
        "roi": roi.median(),
        "pagou": (roi > 1).mean() * 100 if len(fin) else float("nan"),
        "nota": dados["vote_average"].median(),
        "n_filmes": len(dados),
        "n_fin": len(fin),
    }


@st.cache_data(max_entries=50)
def kpis_por_decada(dados):
    linhas = [{"decada": d, **kpis(grupo)} for d, grupo in dados.groupby("decada")]
    return pd.DataFrame(linhas)


# [IA] Claude Code + Skill oficial do Streamlit – preparação dos dados da dispersão e da linha do tempo (Aula 23)
@st.cache_data(max_entries=50)
def filmes_com_roi(dados):
    """Um filme por linha, só os que têm orçamento e receita informados, em US$ mi."""
    fin = dados.dropna(subset=["budget", "revenue"])
    return pd.DataFrame(
        {
            "title": fin["title"],
            "ano": pd.to_datetime(fin["release_date"]).dt.year,
            "avaliacao": fin["avaliacao"],
            "budget": fin["budget"] / ESCALA["budget"],
            "revenue": fin["revenue"] / ESCALA["revenue"],
            "roi": fin["revenue"] / fin["budget"],
        }
    )


@st.cache_data(max_entries=50)
def medianas_por_lustro(dados):
    """Mediana de receita e de orçamento a cada 5 anos de lançamento, em formato longo (uma linha por lustro e série)."""
    # Lustros em vez de anos: antes de 1970 muitos anos têm 1 a 3 filmes, e um filme sozinho virava a mediana
    lustro = pd.to_datetime(dados["release_date"]).dt.year // 5 * 5
    por_lustro = dados.groupby(lustro).agg(
        receita=("revenue", "median"),
        orcamento=("budget", "median"),
        filmes=("id", "size"),
    )
    por_lustro = por_lustro.rename(columns={"receita": "Receita mediana", "orcamento": "Orçamento mediano"})
    longo = por_lustro.reset_index(names="lustro").melt(
        id_vars=["lustro", "filmes"], var_name="serie", value_name="valor"
    )
    longo["periodo"] = longo["lustro"].map(lambda a: f"{a}–{a + 4}")
    longo["valor"] = longo["valor"] / ESCALA["revenue"]
    return longo.dropna(subset=["valor"])


def valor_kpi(chave, valor):
    """Texto de exibição de cada KPI ('—' quando não há filmes para calcular)."""
    if pd.isna(valor):
        return "—"
    if chave == "receita":
        return f"US$ {formatar_decimal(valor)} mi"
    if chave == "roi":
        return f"{formatar_decimal(valor)}×"
    if chave == "pagou":
        return f"{formatar_decimal(valor, 0)}%"
    return formatar_decimal(valor)


with aba_d2:
    st.caption(
        "Para quem decide onde investir: quanto os filmes faturam, quanto devolvem do orçamento "
        "e como isso mudou ao longo das décadas."
    )

    # [IA] Claude Code + Skill oficial do Streamlit – layout dos widgets e st.metric do Dashboard 2 (Aula 22)
    # Widgets do Dashboard 2 (ficam na aba, porque a sidebar controla só o Dashboard 1)
    with st.container(horizontal=True, gap="large", vertical_alignment="bottom"):
        decadas = st.pills(
            "Décadas",
            options=ORDEM_DECADAS,
            selection_mode="multi",
            default=ORDEM_DECADAS,
            key="d2_decadas",
        )
        classe_d2 = st.segmented_control(
            "Classe",
            options=["Todos", *CLASSES],
            default="Todos",
            required=True,
            key="d2_classe",
        )

    df_d2 = df[df["decada"].isin(decadas)]
    if classe_d2 != "Todos":
        df_d2 = df_d2[df_d2["avaliacao"] == classe_d2]

    if df_d2.empty:
        st.warning("Selecione pelo menos 1 década para ver os indicadores.", icon=":material/warning:")
    else:
        geral = kpis(df_d2)
        base_fin = f"Base: {formatar_inteiro(geral['n_fin'])} filmes com orçamento e receita informados."

        col_receita, col_roi, col_pagou, col_nota = st.columns(4, gap="medium")
        with col_receita:
            st.metric(
                "Receita mediana",
                valor_kpi("receita", geral["receita"]),
                help="Metade dos filmes do recorte faturou mais do que isso na bilheteria. Considera só receitas informadas.",
                icon=":material/payments:",
                border=True,
            )
        with col_roi:
            st.metric(
                "ROI mediano",
                valor_kpi("roi", geral["roi"]),
                help=f"Receita ÷ orçamento do filme típico: 2× = faturou o dobro do que custou. {base_fin}",
                icon=":material/trending_up:",
                border=True,
            )
        with col_pagou:
            st.metric(
                "% que se pagou",
                valor_kpi("pagou", geral["pagou"]),
                help=f"Filmes cuja receita superou o orçamento (sem contar marketing e distribuição). {base_fin}",
                icon=":material/savings:",
                border=True,
            )
        with col_nota:
            st.metric(
                "Nota mediana",
                valor_kpi("nota", geral["nota"]),
                help="Mediana de vote_average (0 a 10) no recorte: a recepção do público.",
                icon=":material/star:",
                border=True,
            )

        with st.container(border=True):
            st.subheader("Por década", icon=":material/bar_chart:")
            # [IA] Claude Code + Skill oficial do Streamlit – sintaxe Altair do gráfico de barras por década (Aula 22)
            nome_metrica = st.segmented_control(
                "Métrica no gráfico",
                options=list(METRICAS_D2),
                default="ROI mediano",
                required=True,
                key="d2_metrica",
            )
            chave = METRICAS_D2[nome_metrica]

            por_decada = kpis_por_decada(df_d2).dropna(subset=[chave])
            por_decada["rotulo"] = por_decada[chave].map(lambda v: valor_kpi(chave, v))

            base = alt.Chart(por_decada).encode(
                x=alt.X("decada:N", sort=ORDEM_DECADAS, title="Década", axis=alt.Axis(labelAngle=0)),
                y=alt.Y(f"{chave}:Q", title=nome_metrica),
            )
            barras = base.mark_bar(color=CORAL, cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                tooltip=[
                    alt.Tooltip("decada:N", title="Década"),
                    alt.Tooltip("rotulo:N", title=nome_metrica),
                    alt.Tooltip("n_filmes:Q", title="Filmes"),
                    alt.Tooltip("n_fin:Q", title="Com orçamento e receita"),
                ]
            )
            # Rótulos dentro do topo da barra, para não brigar com a linha de referência
            rotulos = base.mark_text(baseline="top", dy=8, color="white", fontSize=13, fontWeight=600).encode(
                text="rotulo:N"
            )
            # Linha tracejada: valor do recorte inteiro, para comparar cada década com o todo
            referencia = (
                alt.Chart(pd.DataFrame({"valor": [geral[chave]]}))
                .mark_rule(color=AZUL, strokeDash=[6, 4], strokeWidth=2)
                .encode(y="valor:Q")
            )
            st.altair_chart(
                (barras + rotulos + referencia).properties(height=360),
                alt=f"Gráfico de barras de {nome_metrica} por década",
            )
            st.caption(f"Linha tracejada: {nome_metrica.lower()} do recorte inteiro ({valor_kpi(chave, geral[chave])}).")

        col_dispersao, col_tempo = st.columns(2, gap="medium")

        with col_dispersao:
            with st.container(border=True, height="stretch"):
                st.subheader("Orçamento × receita", icon=":material/scatter_plot:")
                st.caption("Um ponto por filme. Acima da linha tracejada, a receita superou o orçamento.")

                # [IA] Claude Code + Skill oficial do Streamlit – sintaxe Altair da dispersão orçamento × receita (Aula 23)
                filmes = filmes_com_roi(df_d2)
                if filmes.empty:
                    st.warning("Nenhum filme com orçamento e receita informados no recorte.", icon=":material/warning:")
                else:
                    escala_log = alt.Scale(type="log")
                    # Só potências de 10 no eixo: na escala log o padrão desenha uma grade densa demais
                    eixo_log = alt.Axis(values=[0.01, 0.1, 1, 10, 100, 1000], format="~g", gridOpacity=0.5)
                    pontos = (
                        alt.Chart(filmes)
                        .mark_circle(size=28, opacity=0.55)
                        .encode(
                            x=alt.X("budget:Q", title="Orçamento (US$ mi, escala log)", scale=escala_log, axis=eixo_log),
                            y=alt.Y("revenue:Q", title="Receita (US$ mi, escala log)", scale=escala_log, axis=eixo_log),
                            color=alt.Color("avaliacao:N", title="Classe", scale=CORES_CLASSE, legend=alt.Legend(orient="top")),
                            tooltip=[
                                alt.Tooltip("title:N", title="Filme"),
                                alt.Tooltip("ano:Q", title="Ano"),
                                alt.Tooltip("budget:Q", title="Orçamento (US$ mi)", format=",.1f"),
                                alt.Tooltip("revenue:Q", title="Receita (US$ mi)", format=",.1f"),
                                alt.Tooltip("roi:Q", title="ROI (×)", format=".2f"),
                            ],
                        )
                    )
                    # Linha receita = orçamento (ROI = 1×), do menor ao maior valor do recorte
                    extremos = [filmes[["budget", "revenue"]].min().min(), filmes[["budget", "revenue"]].max().max()]
                    empate = (
                        alt.Chart(pd.DataFrame({"budget": extremos, "revenue": extremos}))
                        .mark_line(color=TEXTO, strokeDash=[6, 4], strokeWidth=1.5, opacity=0.7)
                        .encode(x="budget:Q", y="revenue:Q")
                    )
                    st.altair_chart(
                        (pontos + empate).properties(height=380),
                        alt="Gráfico de dispersão do orçamento contra a receita de cada filme, em escala log",
                    )
                    st.caption(f"{formatar_inteiro(len(filmes))} filmes com orçamento e receita informados.")

        with col_tempo:
            with st.container(border=True, height="stretch"):
                st.subheader("Receita e orçamento no tempo", icon=":material/show_chart:")
                st.caption("Mediana a cada 5 anos de lançamento, em US$ milhões (valores nominais).")

                # [IA] Claude Code + Skill oficial do Streamlit – sintaxe Altair da linha de receita e orçamento por lustro (Aula 23)
                por_lustro = medianas_por_lustro(df_d2)
                if por_lustro.empty:
                    st.warning("Nenhum filme com orçamento ou receita informados no recorte.", icon=":material/warning:")
                else:
                    linhas = (
                        alt.Chart(por_lustro)
                        .mark_line(point=alt.OverlayMarkDef(size=40), strokeWidth=2.5)
                        .encode(
                            x=alt.X("lustro:Q", title="Início do lustro", axis=alt.Axis(format="d", tickMinStep=5)),
                            y=alt.Y("valor:Q", title="US$ mi"),
                            color=alt.Color(
                                "serie:N",
                                title=None,
                                scale=alt.Scale(domain=["Receita mediana", "Orçamento mediano"], range=[CORAL, CINZA]),
                                legend=alt.Legend(orient="top"),
                            ),
                            tooltip=[
                                alt.Tooltip("periodo:N", title="Período"),
                                alt.Tooltip("serie:N", title="Série"),
                                alt.Tooltip("valor:Q", title="US$ mi", format=",.1f"),
                                alt.Tooltip("filmes:Q", title="Filmes no período"),
                            ],
                        )
                    )
                    st.altair_chart(
                        linhas.properties(height=380),
                        alt="Gráfico de linhas da receita mediana e do orçamento mediano a cada 5 anos de lançamento",
                    )
                    st.caption("Cada ponto agrupa 5 anos (ex.: 1980 = 1980–1984). O tooltip mostra quantos filmes há no período.")

    st.caption("Fonte: TMDB 5000 Movie Dataset (Kaggle) · Valores nominais, sem correção pela inflação.")
