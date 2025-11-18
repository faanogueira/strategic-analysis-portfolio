import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


@st.cache_data
def carregar_dados():
    url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSQO339x3asoCz7WUA4bxRD7Oj85mJr2pv_VSyDVjUyfXpe5fTcNhaL7mqq-ZF30GBiz894cs3Kcd4Y/pub?gid=971678561&single=true&output=csv"
    df = pd.read_csv(url_csv)
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def main():

    st.title("Dashboard de Vendas Empada")
    st.write("Painel de métricas e projeções, sem remover nenhuma linha do dataset")

    df = carregar_dados()

    with st.expander("Prévia dos dados (brutos)"):
        st.write("Colunas:", list(df.columns))
        st.write("Tipos:", df.dtypes)
        st.dataframe(df.head())


    # -------------------------------------------------------------------------
    # 1 – Detectar automaticamente colunas
    # -------------------------------------------------------------------------
    data_cols = [c for c in df.columns if "data" in c]

    if not data_cols:
        st.error("Nenhuma coluna contendo 'data' encontrada.")
        return

    col_data = data_cols[0]

    # valor será a primeira coluna numérica ou a coluna chamada 'valor'
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    col_valor = None

    if "valor" in df.columns:
        col_valor = "valor"
    elif numeric_cols:
        col_valor = numeric_cols[0]
    else:
        st.error("Nenhuma coluna numérica encontrada para usar como valor.")
        return

    # produto opcional
    text_cols = df.select_dtypes(include="object").columns.tolist()
    text_cols = [c for c in text_cols if c != col_data]

    col_produto = None
    for name in ["produto", "item", "descricao", "sabor"]:
        if name in text_cols:
            col_produto = name
            break

    if not col_produto and text_cols:
        col_produto = text_cols[0]

    st.info(
        f"Detectado automaticamente: data='{col_data}', valor='{col_valor}', produto='{col_produto}'"
    )


    # -------------------------------------------------------------------------
    # 2 – Conversão de data e valor SEM DROPAR NADA
    # -------------------------------------------------------------------------

    # data
    df["_data_conv"] = pd.to_datetime(df[col_data], dayfirst=True, errors="coerce")

    with st.expander("Diagnóstico da conversão de datas"):
        st.write("Total de linhas:", len(df))
        st.write("Datas válidas:", df["_data_conv"].notna().sum())
        st.write("Exemplo após conversão:")
        st.dataframe(df[[col_data, "_data_conv"]].head())

    # valor
    df["_valor_conv"] = pd.to_numeric(df[col_valor], errors="coerce")

    with st.expander("Diagnóstico da conversão de valores"):
        st.write("Valores numéricos válidos:", df["_valor_conv"].notna().sum())
        st.dataframe(df[[col_valor, "_valor_conv"]].head())


    # Criar colunas temporais (somente para linhas válidas, mas SEM excluir)
    df["ano_mes"] = df["_data_conv"].dt.to_period("M").dt.to_timestamp()
    df["dia"] = df["_data_conv"].dt.date


    # -------------------------------------------------------------------------
    # 3 – Vendas mensais e média
    # -------------------------------------------------------------------------
    st.subheader("Vendas mensais e média")

    mensal = (
        df.groupby("ano_mes")["_valor_conv"]
        .sum(min_count=1)  # soma ignorando NaN sem apagar linhas
        .reset_index(name="total_mensal")
    )

    if mensal["total_mensal"].notna().sum() == 0:
        st.warning("Não há dados mensais suficientes para gerar o gráfico.")
    else:
        media_mensal = mensal["total_mensal"].mean()

        chart = (
            alt.Chart(mensal)
            .mark_bar()
            .encode(
                x="ano_mes:T",
                y="total_mensal:Q",
                tooltip=["ano_mes:T", "total_mensal:Q"],
            )
        )

        linha_media = (
            alt.Chart(pd.DataFrame({"media": [media_mensal]}))
            .mark_rule(color="red")
            .encode(y="media:Q")
        )

        st.altair_chart(chart + linha_media, use_container_width=True)
        st.caption(f"Média mensal: R$ {media_mensal:.2f}")


    # -------------------------------------------------------------------------
    # 4 – Vendas mensais total por mês
    # -------------------------------------------------------------------------
    st.subheader("Vendas mensais (total por mês)")
    st.altair_chart(
        chart,
        use_container_width=True
    )


    # -------------------------------------------------------------------------
    # 5 – Top 10 produtos (se existir coluna de produto)
    # -------------------------------------------------------------------------
    st.subheader("Top 10 produtos vendidos")

    if col_produto:
        top10 = (
            df.groupby(col_produto)["_valor_conv"]
            .sum(min_count=1)
            .nlargest(10)
            .reset_index(name="total_vendido")
        )

        if top10["total_vendido"].notna().sum() == 0:
            st.info("Não há dados suficientes para o Top 10.")
        else:
            chart_top = (
                alt.Chart(top10)
                .mark_bar()
                .encode(
                    x="total_vendido:Q",
                    y=alt.Y(col_produto + ":N", sort="-x"),
                    tooltip=[col_produto, "total_vendido"],
                )
            )
            st.altair_chart(chart_top, use_container_width=True)

    else:
        st.info("Nenhuma coluna de produto disponível.")


    # -------------------------------------------------------------------------
    # 6 – Vendas diárias
    # -------------------------------------------------------------------------
    st.subheader("Vendas diárias")

    diario = (
        df.groupby("dia")["_valor_conv"]
        .sum(min_count=1)
        .reset_index(name="total_diario")
    )

    if diario["total_diario"].notna().sum() == 0:
        st.warning("Não há dados diários suficientes.")
    else:
        chart_dia = (
            alt.Chart(diario)
            .mark_line(point=True)
            .encode(
                x="dia:T",
                y="total_diario:Q",
                tooltip=["dia:T", "total_diario:Q"],
            )
        )
        st.altair_chart(chart_dia, use_container_width=True)

        # média móvel sem apagar nada
        diario["mm7"] = diario["total_diario"].rolling(7, min_periods=1).mean()

        chart_mm7 = (
            alt.Chart(diario)
            .mark_line(color="orange")
            .encode(
                x="dia:T",
                y="mm7:Q",
            )
        )

        st.altair_chart(chart_dia + chart_mm7, use_container_width=True)


    # -------------------------------------------------------------------------
    # 7 – Projeção mensal (regressão linear)
    # -------------------------------------------------------------------------
    st.subheader("Projeção mensal")

    mensal_valid = mensal.dropna(subset=["total_mensal"])

    if len(mensal_valid) < 2:
        st.warning("Não há dados suficientes para regressão e projeção.")
        return

    mensal_valid = mensal_valid.sort_values("ano_mes").reset_index(drop=True)
    mensal_valid["t"] = np.arange(len(mensal_valid))

    coef = np.polyfit(mensal_valid["t"], mensal_valid["total_mensal"], 1)
    a, b = coef

    mensal_valid["tendencia"] = a * mensal_valid["t"] + b

    # projeção
    n_proj = 1
    t_proj = np.arange(len(mensal_valid), len(mensal_valid) + n_proj)

    datas_proj = pd.date_range(
        start=mensal_valid["ano_mes"].iloc[-1] + pd.offsets.MonthBegin(1),
        periods=n_proj,
        freq="MS",
    )

    proj = pd.DataFrame({
        "ano_mes": datas_proj,
        "projecao": a * t_proj + b
    })

    chart_hist = (
        alt.Chart(mensal_valid)
        .mark_bar()
        .encode(x="ano_mes:T", y="total_mensal:Q")
    )

    chart_tend = (
        alt.Chart(mensal_valid)
        .mark_line(color="orange")
        .encode(x="ano_mes:T", y="tendencia:Q")
    )

    chart_proj = (
        alt.Chart(proj)
        .mark_line(color="green")
        .encode(x="ano_mes:T", y="projecao:Q")
    )

    st.altair_chart(chart_hist + chart_tend + chart_proj, use_container_width=True)

    st.metric("Média mensal histórica", f"R$ {mensal_valid['total_mensal'].mean():.2f}")


if __name__ == "__main__":
    main()
