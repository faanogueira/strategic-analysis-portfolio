import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

@st.cache_data
def carregar_dados():
    url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSQO339x3asoCz7WUA4bxRD7Oj85mJr2pv_VSyDVjUyfXpe5fTcNhaL7mqq-ZF30GBiz894cs3Kcd4Y/pub?gid=971678561&single=true&output=csv"
    df = pd.read_csv(url_csv)

    # normaliza nomes das colunas
    df.columns = [col.strip().lower() for col in df.columns]
    return df


def main():
    st.title("Dashboard de Vendas Empada")
    st.write("Painel de métricas e projeções")

    df = carregar_dados()

    # prévia para conferência
    with st.expander("Prévia dos dados (antes de qualquer tratamento)"):
        st.write("Colunas do dataframe:", list(df.columns))
        st.write("Tipos de dados:", df.dtypes)
        st.dataframe(df.head())

    # 1. detectar automaticamente as colunas principais

    # coluna de data: qualquer coluna que contenha "data" no nome
    data_cols = [c for c in df.columns if "data" in c]
    if not data_cols:
        st.error("Não encontrei nenhuma coluna de data (nome contendo 'data').")
        return
    col_data = data_cols[0]

    # coluna de valor: alguma coluna numérica
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if not num_cols:
        st.error("Não encontrei nenhuma coluna numérica para usar como valor de venda.")
        return

    preferidas_valor = ["valor", "total", "receita", "faturamento"]
    col_valor = None
    for nome in preferidas_valor:
        if nome in df.columns:
            col_valor = nome
            break
    if col_valor is None:
        col_valor = num_cols[0]

    # coluna de produto (opcional): alguma coluna de texto que não seja a data
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()
    cat_cols = [c for c in cat_cols if c != col_data]

    preferidas_prod = ["produto", "produto_nome", "item", "descricao", "sabor"]
    col_produto = None
    for nome in preferidas_prod:
        if nome in cat_cols:
            col_produto = nome
            break
    if col_produto is None and cat_cols:
        col_produto = cat_cols[0]

    st.info(
        f"Usando colunas: data = '{col_data}', valor = '{col_valor}'"
        + (f", produto = '{col_produto}'" if col_produto else " (sem coluna de produto)")
    )

    # 2. preparar dados de tempo
    df[col_data] = pd.to_datetime(df[col_data], dayfirst=True, errors="coerce")

    with st.expander("Após conversão de data"):
        st.write("Linhas antes da remoção de datas inválidas:", len(df))
        st.write("Datas válidas:", df[col_data].notna().sum())
        st.dataframe(df[[col_data]].head())

    df = df.dropna(subset=[col_data])

    if df.empty:
        st.error("Depois da conversão de datas, não sobrou nenhuma linha válida. Verifique o formato da coluna de data na planilha.")
        return

    # garante que a coluna de valor é numérica
    df[col_valor] = pd.to_numeric(df[col_valor], errors="coerce")

    if df[col_valor].notna().sum() == 0:
        st.error(f"A coluna de valor '{col_valor}' não tem números válidos. Verifique se os valores estão com vírgula ou texto na planilha.")
        return

    df = df.dropna(subset=[col_valor])

    if df.empty:
        st.error("Após remover valores não numéricos em valor, o dataframe ficou vazio.")
        return

    df["ano_mes"] = df[col_data].dt.to_period("M").dt.to_timestamp()
    df["dia"] = df[col_data].dt.date

    with st.expander("Dados após tratamento final"):
        st.write("Shape:", df.shape)
        st.dataframe(df.head())

    # 3. Vendas mensais e média
    st.subheader("Vendas mensais e média")

    mensal = (
        df.groupby("ano_mes")[col_valor]
        .sum()
        .reset_index(name="total_mensal")
    )

    if mensal.empty:
        st.warning("Não foi possível calcular vendas mensais (agrupamento retornou vazio).")
    else:
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

        # 4. Vendas mensais (total por mês)
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

    # 5. Top 10 produtos vendidos (só se tiver coluna categórica)
    st.subheader("Top 10 produtos vendidos")
    if col_produto:
        top_produtos = (
            df.groupby(col_produto)[col_valor]
            .sum()
            .nlargest(10)
            .reset_index(name="total_vendido")
        )

        if top_produtos.empty:
            st.info("Não foi possível calcular o Top 10 produtos, dados vazios após agrupamento.")
        else:
            chart_top = (
                alt.Chart(top_produtos)
                .mark_bar()
                .encode(
                    x="total_vendido:Q",
                    y=alt.Y(col_produto + ":N", sort="-x"),
                    tooltip=[col_produto + ":N", "total_vendido:Q"]
                )
            )

            st.altair_chart(chart_top, use_container_width=True)
    else:
        st.info("Não há coluna categórica para calcular o Top 10 de produtos. Gráfico omitido.")

    # 6. Vendas diárias
    st.subheader("Vendas diárias")

    diario = (
        df.groupby("dia")[col_valor]
        .sum()
        .reset_index(name="total_diario")
    )

    if diario.empty:
        st.warning("Não foi possível calcular vendas diárias (agrupamento retornou vazio).")
    else:
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

        # 6.1. Média móvel de 7 dias
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

    # 7. Média de vendas e projeções mensais
    st.subheader("Média de vendas e projeções mensais")

    if mensal.empty or len(mensal) < 2:
        st.warning("Não há dados mensais suficientes para estimar uma tendência e projeção.")
    else:
        mensal = mensal.sort_values("ano_mes").reset_index(drop=True)
        mensal["t"] = np.arange(len(mensal))

        if mensal["total_mensal"].notna().sum() < 2:
            st.warning("Não há pontos suficientes para ajustar regressão.")
        else:
            coef = np.polyfit(mensal["t"], mensal["total_mensal"], 1)
            a, b = coef

            mensal["tendencia"] = a * mensal["t"] + b

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

            media_mensal_hist = mensal["total_mensal"].mean()
            st.metric("Média mensal histórica", f"R$ {media_mensal_hist:.2f}")


if __name__ == "__main__":
    main()
