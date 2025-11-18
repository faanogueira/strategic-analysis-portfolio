import streamlit as st
import pandas as pd
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

    df = carregar_dados()

    # debug inicial
    st.expander("Ver colunas e amostra dos dados").write(df.head())
    st.write("Colunas do dataframe:", list(df.columns))

    # ajuste estes nomes conforme o que aparecer
    coluna_produto = "produto"           # ex: "produto"
    coluna_meio_pg = "meio_pagamento"    # ex: "meio de pagamento"
    coluna_valor = "valor"               # ex: "valor"

    # validação de colunas
    for c in [coluna_produto, coluna_meio_pg, coluna_valor]:
        if c not in df.columns:
            st.error(f"Coluna '{c}' não encontrada. Colunas disponíveis: {list(df.columns)}")
            st.stop()

    st.subheader("Filtros")
    col1, col2 = st.columns(2)

    produtos = ["Todos"] + sorted(df[coluna_produto].dropna().unique().tolist())
    meios = ["Todos"] + sorted(df[coluna_meio_pg].dropna().unique().tolist())

    produto_sel = col1.selectbox("Selecione o produto", produtos)
    meio_sel = col2.selectbox("Meio de pagamento", meios)

    df_filtrado = df.copy()

    if produto_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado[coluna_produto] == produto_sel]

    if meio_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado[coluna_meio_pg] == meio_sel]

    st.subheader("Dados filtrados")
    st.dataframe(df_filtrado)

    st.subheader("Estatísticas")
    total_vendido = df_filtrado[coluna_valor].sum()
    qtd_itens = len(df_filtrado)

    colm1, colm2 = st.columns(2)
    colm1.metric("Valor total filtrado", f"R$ {total_vendido:.2f}")
    colm2.metric("Quantidade de itens", qtd_itens)

    st.subheader("Vendas por produto")
    vendas_por_produto = df_filtrado.groupby(coluna_produto)[coluna_valor].sum()
    st.bar_chart(vendas_por_produto)

    st.subheader("Exportar dados filtrados")

    def gerar_csv(dados):
        buffer = io.StringIO()
        dados.to_csv(buffer, index=False, sep=";")
        return buffer.getvalue()

    csv_export = gerar_csv(df_filtrado)

    st.download_button(
        label="Baixar CSV filtrado",
        data=csv_export,
        file_name="dados_filtrados.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
