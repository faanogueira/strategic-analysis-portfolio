import streamlit as st
import pandas as pd
import time

url_csv = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSQO339x3asoCz7WUA4bxRD7Oj85mJr2pv_VSyDVjUyfXpe5fTcNhaL7mqq-ZF30GBiz894cs3Kcd4Y/pub?gid=971678561&single=true&output=csv'
df = pd.read_csv(url_csv)
df.head()

def main():
    st.title("Métricas Empada")
    st.write("Acompanhe os resultados em tempo real")
    
    st. header("Input de Texto")
    input_text = st.text_area("Digite seu texto aqui:", height=150)
    if input_text:
        st.write("Você digitou: ", input_text)
    
    st.header("Seleção")
    setected_option = st.selectbox("Escolha uma opção:", ["Opção 1", "Opção 2", "Opção 3"])
    if setected_option:
        st.write("Você selecionou: ", setected_option)
    
    st.header("Slider")
    slider_value = st.slider("Selecione um valor:", 0, 100, 50)
    st.write("Valor selecionado: ", slider_value)
    
    st.header("Checkbox")
    checkbox_value = st.checkbox("Marque para confirmar")
    st.write("Checkbox está: ", checkbox_value)
    
    st.header(Botão)
    if st.button("Clique aqui"):
        st.write("Botão clicado!")
    
    st.header("Loading")
    with st.spinner("Carregando..."):
        time.sleep(3)
    st.success("Carregamento concluído!")
    
    st.header("Upload de Arquivo")
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["pdf", "csv", "xlsx"])
    if uploaded_file:
        st.write("Arquivo carregado: ", uploaded_file.name)
    
    st.header("Gráfico")
    data = {
        'Categoria': ['A', 'B', 'C', 'D'],
        'Valores': [23, 45, 12, 36]
    }
    st.line_chart(data={'Categoria': data['Categoria'], 'Valores': data['Valores']})
        
    if st.button("Start Progress"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        for percent_complete in range(101):
            time.sleep(0.05)  # Simulate a task taking time
            progress_bar.progress(percent_complete)
            status_text.text(f"Progress: {percent_complete}%")

        status_text.text("Task Completed!")