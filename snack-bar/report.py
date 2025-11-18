import streamlit as st
import pandas as pd
import io

# 1. Importação do CSV hospedado no Google Sheets
@st.cache_data
def carregar_dados():
    url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSQO339x3asoCz7WUA4bxRD7Oj85mJr2pv_VSyDVjUyfXpe5fTcNhaL7mqq-ZF30GBiz894cs3Kcd4Y/pub?gid=971678561&single=true&output=csv"
    df = pd.read_csv(url_csv)
    return df

def main():
    st.title("Dashboard de Vendas Empada")
    st.write("Painel de métricas, filtros e exportação de dados")

    # 2. Carregar dados
    df = carregar_dados()

    st.subheader("Prévia dos dados")
    st.dataframe(df)

    # 3. Filtros
    st.subheader("Filtros")
    col1, col2 = st.columns(2)

    produto = col1.selectbox("Selecione o produto", ["Todos"] + sorted(df["produto"].unique()))
    meio_pg = col2.selectbox("Meio de pagamento", ["Todos"] + sorted(df["meio_pagamento"].unique()))

    df_filtrado = df.copy()

    if produto != "Todos":
        df_filtrado = df_filtrado[df_filtrado["produto"] == produto]

    if meio_pg != "Todos":
        df_filtrado = df_filtrado[df_filtrado["meio_pagamento"] == meio_pg]

    st.subheader("Dados filtrados")
    st.dataframe(df_filtrado)

    # 4. Estatísticas simples
    st.subheader("Estatísticas")
    total_vendido = df_filtrado["valor"].sum()
    qtd_itens = len(df_filtrado)

    st.metric("Valor total filtrado", f"R$ {total_vendido:.2f}")
    st.metric("Quantidade de itens", qtd_itens)

    # 5. Gráfico
    st.subheader("Vendas por produto")
    graf = df.groupby("produto")["valor"].sum()
    st.bar_chart(graf)

    # 6. Exportar os dados filtrados
    st.subheader("Exportar dados filtrados")

    def gerar_csv(df_export):
        buffer = io.StringIO()
        df_export.to_csv(buffer, index=False, sep=";")
        return buffer.getvalue()

    nome_arquivo = "dados_filtrados.csv"
    csv_export = gerar_csv(df_filtrado)

    st.download_button(
        label="Baixar CSV",
        data=csv_export,
        file_name=nome_arquivo,
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
