import math

import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="CineInsights | TMDB Analytics",
    page_icon=":material/movie:",
    layout="wide",
)

# Refinamentos pontuais: só classes geradas por key= (estáveis), sem classes internas do Streamlit
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
    [class*="st-key-placeholder"] {
        background:
            repeating-linear-gradient(135deg, rgba(120, 135, 175, 0.06) 0 12px, rgba(120, 135, 175, 0) 12px 24px),
            linear-gradient(180deg, rgba(240, 84, 90, 0.06) 0%, rgba(240, 84, 90, 0) 100%);
        border: 1px dashed rgba(240, 84, 90, 0.45);
        border-radius: 14px;
    }
    </style>
    """
)

df = load_data()

# Variáveis quantitativas do estudo (mesma lista VARS_QUANT do notebook de EDA)
VARS_QUANT = ["budget", "revenue", "popularity", "runtime", "vote_average", "vote_count"]

# budget e revenue chegam a bilhões: os sliders mostram em US$ milhões para ficarem legíveis
ESCALA = {"budget": 1_000_000, "revenue": 1_000_000}


def limites_slider(serie):
    """Mínimo, máximo e passo do slider de intervalo de uma variável."""
    # runtime é inteiro, mas vem como float por causa dos NaN (runtime == 0 tratado na EDA)
    if serie.dropna().mod(1).eq(0).all():
        return int(serie.min()), int(serie.max()), 1
    return math.floor(serie.min() * 10) / 10, math.ceil(serie.max() * 10) / 10, 0.1


def formatar_inteiro(n):
    return f"{n:,}".replace(",", ".")


# Sidebar: filtros (variáveis + intervalo)
with st.sidebar:
    st.header("Filtros", icon=":material/tune:")
    st.caption("Defina o recorte de filmes analisado nas seções ao lado.")

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
        unidade = " (US$ mi)" if var in ESCALA else ""
        intervalos[var] = st.slider(
            f"Intervalo de {var}{unidade}",
            min_value=minimo,
            max_value=maximo,
            value=(minimo, maximo),
            step=passo,
            format="%d" if passo == 1 else "%.1f",
            key=f"intervalo_{var}",
        )

# Mantém só os filmes dentro de todos os intervalos escolhidos.
# Filmes sem valor (runtime ausente) só saem quando o intervalo daquela variável é estreitado.
df_filtrado = df
for var, (inicio, fim) in intervalos.items():
    valores = df_filtrado[var] / ESCALA.get(var, 1)
    minimo, maximo, _ = limites_slider(df[var] / ESCALA.get(var, 1))
    dentro = valores.between(inicio, fim)
    if (inicio, fim) == (minimo, maximo):
        dentro |= valores.isna()
    df_filtrado = df_filtrado[dentro]

# Cabeçalho
with st.container(key="hero", gap="small"):
    st.badge("TMDB Analytics", icon=":material/movie:", color="primary")
    st.title("CineInsights")
    st.markdown("Correlação e distribuição das variáveis quantitativas do **TMDB 5000 Movies**.")

st.space("small")

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


def placeholder(chave, icone, titulo, descricao, altura=360):
    """Espaço reservado para um gráfico que ainda será implementado."""
    with st.container(
        key=f"placeholder_{chave}",
        height=altura,
        horizontal_alignment="center",
        vertical_alignment="center",
    ):
        st.markdown(f"## {icone}", text_alignment="center")
        st.markdown(f"**{titulo}**", text_alignment="center")
        st.caption(descricao, text_alignment="center")
        st.badge("Em breve", icon=":material/schedule:", color="primary")


# Dashboard 1: correlação (heatmap) à esquerda, distribuição (histograma) à direita
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
            # TODO: matriz de Spearman (df_filtrado[variaveis].corr(method="spearman")) em heatmap
            placeholder(
                "correlacao",
                ":material/grid_on:",
                "Heatmap de correlação de Spearman",
                f"{len(variaveis)} variáveis · {formatar_inteiro(len(df_filtrado))} filmes",
                altura="stretch",  # ocupa a altura que sobra no card (o da direita tem um seletor a mais)
            )

with col_distribuicao:
    with st.container(border=True, height="stretch"):
        st.subheader("Distribuição", icon=":material/bar_chart:")
        st.caption("Como os valores de uma variável se espalham entre os filmes do recorte.")

        if not variaveis:
            st.warning("Selecione pelo menos 1 variável para ver a distribuição.", icon=":material/warning:")
        else:
            var_hist = st.selectbox("Variável do histograma", options=variaveis)
            classe = "Bem avaliado × Mal avaliado" if separar_por_classe else "todos os filmes juntos"

            # TODO: histograma de var_hist; se separar_por_classe: color="avaliacao"
            placeholder(
                "distribuicao",
                ":material/bar_chart:",
                f"Histograma de {var_hist}",
                f"{classe} · {formatar_inteiro(len(df_filtrado))} filmes",
            )

st.caption("Fonte: TMDB 5000 Movie Dataset (Kaggle) · Tratamento: notebooks/eda.ipynb")

# TODO: Dashboard 2 — KPIs (Aula 22)
