import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import io

@st.cache_data
def carregar_dados():
    url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSQO339x3asoCz7WUA4bxRD7Oj85mJr2pv_VSyDVjUyfXpe5fTcNhaL7mqq-ZF30GBiz894cs3Kcd4Y/pub?gid=971678561&single=true&output=csv"
    df = pd.read_csv(url_csv)

    # normaliza nomes das colunas
    df.columns = [col.strip().lower() for col in df.columns]
    return df


def main():
    st.title("Dashboard de Vendas Empada")
    st.write("Painel de métricas, filtros e exportação")

    # carrega dados
    df = carregar_dados()

    # debug inicial para você conferir nomes das colunas
    with st.expander("Prévia dos dados"):
        st.write("Colunas do dataframe:", list(df.columns))
        st.dataframe(df.head())

    # ajuste estes nomes conforme sua planilha
    coluna_data = "Data"          # exemplo: "data"
    coluna_valor = "valor"        # exemplo: "valor"
    coluna_produto = "produto"    # exemplo: "produto"

    # validação de colunas
    for c in [coluna_data, coluna_valor, coluna_produto]:
        if c not in df.columns:
            st.error(
                f"Coluna '{c}' não encontrada. "
                f"Ajuste os nomes em coluna_data, coluna_valor e coluna_produto. "
                f"Colunas disponíveis: {list(df.columns)}"
            )
            st.stop()

    # 1. Preparar dados de tempo
    df[coluna_data] = pd.to_datetime(df[coluna_data], dayfirst=True, errors="coerce")
    df = df.dropna(subset=[coluna_data])

    df["ano_mes"] = df[coluna_data].dt.to_period("M").dt.to_timestamp()
    df["dia"] = df[coluna_data].dt.date

    # 2. Vendas mensais e média
    st.subheader("Vendas mensais e média")

    mensal = (
        df.groupby("ano_mes")[coluna_valor]
        .sum()
        .reset_index(name="total_mensal")
    )

    media_mensal = mensal["total_mensal"].mean()

    chart_mensal_media = (
        alt.Chart(mensal)
        .mark_bar()
        .encode(
            x="ano_mes:T",
            y="total_mensal:Q",
            tooltip=["ano_mes:T", "total_mensal:Q"]
        )
    )

    linha_media = (
        alt.Chart(pd.DataFrame({"media": [media_mensal]}))
        .mark_rule(color="red")
        .encode(y="media:Q")
    )

    st.altair_chart(chart_mensal_media + linha_media, use_container_width=True)
    st.caption(f"Média mensal: R$ {media_mensal:.2f}")

    # 3. Vendas mensais (somente o total por mês)
    st.subheader("Vendas mensais (total por mês)")

    chart_mensal = (
        alt.Chart(mensal)
        .mark_bar()
        .encode(
            x="ano_mes:T",
            y="total_mensal:Q",
            tooltip=["ano_mes:T", "total_mensal:Q"]
        )
    )

    st.altair_chart(chart_mensal, use_container_width=True)

    # 4. Top 10 produtos vendidos
    st.subheader("Top 10 produtos vendidos")

    top_produtos = (
        df.groupby(coluna_produto)[coluna_valor]
        .sum()
        .nlargest(10)
        .reset_index(name="total_vendido")
    )

    chart_top = (
        alt.Chart(top_produtos)
        .mark_bar()
        .encode(
            x="total_vendido:Q",
            y=alt.Y(coluna_produto + ":N", sort="-x"),
            tooltip=[coluna_produto + ":N", "total_vendido:Q"]
        )
    )

    st.altair_chart(chart_top, use_container_width=True)

    # 5. Vendas diárias
    st.subheader("Vendas diárias")

    diario = (
        df.groupby("dia")[coluna_valor]
        .sum()
        .reset_index(name="total_diario")
    )

    chart_diario = (
        alt.Chart(diario)
        .mark_line(point=True)
        .encode(
            x="dia:T",
            y="total_diario:Q",
            tooltip=["dia:T", "total_diario:Q"]
        )
    )

    st.altair_chart(chart_diario, use_container_width=True)

    # 5.1. Vendas média móvel de sete dias
    diario["mm7"] = diario["total_diario"].rolling(window=7, min_periods=1).mean()

    chart_diario_mm = (
        alt.Chart(diario)
        .mark_line()
        .encode(
            x="dia:T",
            y="mm7:Q",
            tooltip=["dia:T", "mm7:Q"]
        )
    )

    st.altair_chart(chart_diario + chart_diario_mm, use_container_width=True)

    # 6. Média de vendas e projeções
    st.subheader("Média de vendas e projeções mensais")

    # garantir que mensal está ordenado por data
    mensal = mensal.sort_values("ano_mes").reset_index(drop=True)

    # criar índice de tempo
    mensal["t"] = np.arange(len(mensal))

    # ajustar regressão linear: total_mensal em função de t
    coef = np.polyfit(mensal["t"], mensal["total_mensal"], 1)
    a, b = coef  # total_mensal aproximado igual a a * t + b

    mensal["tendencia"] = a * mensal["t"] + b

    # criar projeções para mais três meses
    qtd_proj = 3
    t_proj = np.arange(len(mensal), len(mensal) + qtd_proj)

    ultima_data = mensal["ano_mes"].max()
    datas_proj = pd.date_range(
        start=ultima_data + pd.offsets.MonthBegin(1),
        periods=qtd_proj,
        freq="MS"
    )

    projecoes = pd.DataFrame({
        "ano_mes": datas_proj,
        "t": t_proj,
    })
    projecoes["projecao"] = a * projecoes["t"] + b

    # gráfico com histórico e projeção
    chart_hist = (
        alt.Chart(mensal)
        .mark_bar()
        .encode(
            x="ano_mes:T",
            y="total_mensal:Q",
            tooltip=["ano_mes:T", "total_mensal:Q"]
        )
    )

    linha_tendencia = (
        alt.Chart(mensal)
        .mark_line(color="orange")
        .encode(
            x="ano_mes:T",
            y="tendencia:Q"
        )
    )

    chart_proj = (
        alt.Chart(projecoes)
        .mark_line(color="green")
        .encode(
            x="ano_mes:T",
            y="projecao:Q",
            tooltip=["ano_mes:T", "projecao:Q"]
        )
    )

    st.altair_chart(chart_hist + linha_tendencia + chart_proj, use_container_width=True)

    # 6.1. Flashcard média mensal
    media_mensal_hist = mensal["total_mensal"].mean()
    st.metric("Média mensal histórica", f"R$ {media_mensal_hist:.2f}")


if __name__ == "__main__":
    main()
