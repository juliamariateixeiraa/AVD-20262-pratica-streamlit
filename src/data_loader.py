import pandas as pd
import streamlit as st


@st.cache_data(max_entries=10)
def load_data(path="data/clean/dataset.csv"):
    """Lê o dataset já tratado (exportado ao final do notebook de EDA)."""
    df = pd.read_csv(path)
    # Na EDA, budget/revenue = 0 (ou < 1000) foram marcados como "não informado" nas flags.
    # Aqui viram ausentes, para não criar um pico falso em zero nos gráficos nem distorcer a correlação.
    df.loc[~df["orcamento_informado"], "budget"] = float("nan")
    df.loc[~df["receita_informada"], "revenue"] = float("nan")
    return df
