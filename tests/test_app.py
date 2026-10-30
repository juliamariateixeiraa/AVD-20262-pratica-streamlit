"""Testes de borda do app (rodar da raiz do projeto: pytest tests/)."""

# [IA] Claude Code + Skill oficial do Streamlit – testes de borda com AppTest: 0, 1, 2+ variáveis e combinações de widgets (Aula 22)
import pytest
from streamlit.testing.v1 import AppTest

VARS_QUANT = ["budget", "revenue", "popularity", "runtime", "vote_average", "vote_count"]


@pytest.fixture
def at():
    return AppTest.from_file("../app.py", default_timeout=30).run()


def avisos(at):
    return [w.value for w in at.warning]


def graficos(at):
    return at.get("vega_lite_chart")


def metrica(at, rotulo):
    return next(m.value for m in at.metric if m.label == rotulo)


# Dashboard 1


def test_padrao_6_variaveis(at):
    assert not at.exception
    assert not avisos(at)
    assert len(graficos(at)) == 3  # heatmap + histograma + barras do Dashboard 2
    assert metrica(at, "Variáveis ativas") == "6 de 6"
    assert len(at.slider) == 6


def test_0_variaveis(at):
    at.multiselect[0].set_value([]).run()
    assert not at.exception
    assert any("pelo menos 2 variáveis" in a for a in avisos(at))
    assert any("pelo menos 1 variável" in a for a in avisos(at))
    assert len(at.slider) == 0
    assert len(graficos(at)) == 1  # só o Dashboard 2 continua


def test_1_variavel(at):
    at.multiselect[0].set_value(["runtime"]).run()
    assert not at.exception
    assert any("pelo menos 2 variáveis" in a for a in avisos(at))
    assert len(graficos(at)) == 2  # histograma + Dashboard 2
    assert at.selectbox[0].options == ["runtime"]


@pytest.mark.parametrize(
    "selecao",
    [["budget", "revenue"], ["popularity", "vote_count", "vote_average"], VARS_QUANT[::-1]],
)
def test_2_ou_mais_variaveis(at, selecao):
    at.multiselect[0].set_value(selecao).run()
    assert not at.exception
    assert not avisos(at)
    assert len(graficos(at)) == 3
    assert len(at.slider) == len(selecao)


@pytest.mark.parametrize("var", VARS_QUANT)
@pytest.mark.parametrize("separar", [False, True])
def test_histograma_cada_variavel_com_e_sem_classe(at, var, separar):
    at.toggle[0].set_value(separar).run()
    at.selectbox[0].set_value(var).run()
    assert not at.exception
    assert len(graficos(at)) == 3


def test_intervalo_estreito_recalcula(at):
    total = metrica(at, "Filmes no recorte")
    at.slider(key="intervalo_vote_average").set_value((7.0, 8.0)).run()
    assert not at.exception
    assert metrica(at, "Filmes no recorte") != total


def test_intervalo_sem_filmes(at):
    # Duas faixas incompatíveis: nota altíssima + quase nenhum voto
    at.slider(key="intervalo_vote_average").set_value((9.9, 10.0)).run()
    at.slider(key="intervalo_vote_count").set_value((5000, 13752)).run()
    assert not at.exception
    assert metrica(at, "Filmes no recorte") == "0"
    assert any("Poucos filmes" in a for a in avisos(at))
    assert any("Nenhum filme" in a for a in avisos(at))


def test_variavel_constante_no_recorte(at):
    # Com runtime travado num valor só, a correlação dele fica indefinida, sem quebrar
    at.multiselect[0].set_value(["runtime", "vote_average"]).run()
    at.slider(key="intervalo_runtime").set_value((100, 100)).run()
    assert not at.exception
    assert any("—" in c.value for c in at.caption)


def test_tirar_variavel_remove_slider_e_filtro(at):
    at.slider(key="intervalo_vote_average").set_value((7.0, 8.0)).run()
    filtrado = metrica(at, "Filmes no recorte")
    at.multiselect[0].set_value(["budget", "revenue"]).run()
    assert not at.exception
    assert metrica(at, "Filmes no recorte") != filtrado


# Dashboard 2


def test_dashboard2_kpis_padrao(at):
    assert metrica(at, "ROI mediano").endswith("×")
    assert metrica(at, "% que se pagou").endswith("%")
    assert metrica(at, "Receita mediana").startswith("US$")


@pytest.mark.parametrize("nome", ["Receita mediana", "ROI mediano", "% que se pagou", "Nota mediana"])
@pytest.mark.parametrize("classe", ["Todos", "Bem avaliado", "Mal avaliado"])
def test_dashboard2_metrica_e_classe(at, nome, classe):
    at.segmented_control(key="d2_classe").set_value(classe).run()
    at.segmented_control(key="d2_metrica").set_value(nome).run()
    assert not at.exception
    assert len(graficos(at)) == 3


def test_dashboard2_sem_decadas(at):
    at.pills(key="d2_decadas").set_value([]).run()
    assert not at.exception
    assert any("pelo menos 1 década" in a for a in avisos(at))


def test_dashboard2_uma_decada_muda_kpi(at):
    roi_total = metrica(at, "ROI mediano")
    at.pills(key="d2_decadas").set_value(["1970s"]).run()
    assert not at.exception
    assert metrica(at, "ROI mediano") != roi_total


def test_dashboard2_independente_da_sidebar(at):
    roi_total = metrica(at, "ROI mediano")
    at.multiselect[0].set_value([]).run()
    assert metrica(at, "ROI mediano") == roi_total
