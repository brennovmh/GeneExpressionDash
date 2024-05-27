import pandas as pd
import streamlit as st
import plotly.express as px
import re

# Carregar os dados ### ALTERE AQUI OS DADOS QUANDO QUISER
df = pd.read_csv("/home/bvmh/PycharmProjects/GeneExpression/TS_RNA_tx_abundance.csv", decimal=',')

# Adicionar a logo no topo
logo_path = "/home/bvmh/PycharmProjects/GeneExpression/download.png"
st.image(logo_path, use_column_width=False)

st.title("Análise de Expressão Diferencial - Round 1")

# Adicionar campo para exploração de dados
st.sidebar.subheader("Selecione um gene")

# Corrigir o nome da variável para 'selected_gene'
selected_gene = st.sidebar.selectbox("", df['Name'].unique())

# Filtrar o DataFrame com base no gene selecionado
selected_gene_df = df[df['Name'] == selected_gene]

# Criar caixas de seleção para escolher amostras
selected_samples = st.multiselect("Escolha as amostras:", selected_gene_df.columns[1:])

# Filtrar o DataFrame com base nas amostras selecionadas
filtered_df = selected_gene_df[['Name'] + selected_samples].melt(id_vars='Name')

# Converter a coluna 'value' para string antes de substituir as vírgulas
filtered_df['value'] = filtered_df['value'].astype(str)

# Tratar valores não numéricos ou vazios antes da conversão
filtered_df['value'] = pd.to_numeric(filtered_df['value'].str.replace(',', '.'), errors='coerce')

# Remover linhas com valores nulos após a conversão
filtered_df = filtered_df.dropna()

# Plotar o gráfico de barras
fig = px.bar(
    filtered_df,
    x='variable',
    y='value',
    color='variable',
    labels={"value": "Log2-TPM", "variable": "Amostras"},
    title=f"Expressão Gênica para {selected_gene}",
)
fig.update_layout(width=900, height=550, font=dict(
        family="Arial",
        size=18,
        color="RebeccaPurple"
    ))

# Exibir o gráfico
st.plotly_chart(fig)
