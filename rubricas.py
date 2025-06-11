import streamlit as st
import pandas as pd

def carregar_rubricas(rubricas_texto):
    linhas = rubricas_texto.strip().split('\n')
    codigos = [c.strip() for c in linhas[0].split(';') if c.strip()]
    descricoes = [d.strip() for d in linhas[1].split(';') if d.strip()]
    grupos = {}
    for desc, linha in zip(descricoes, linhas[2:]):
        rubricas = [c.strip() for c in linha.split(';') if c.strip()]
        for cod in rubricas:
            grupos[cod] = desc
    return grupos

st.title("Classificador de Rubricas Contábeis")

folha_file = st.file_uploader("Upload Folha CSV", type=["csv"])
rubricas_file = st.file_uploader("Upload Rubricas TXT", type=["txt"])

if folha_file and rubricas_file:
    try:
        folha_df = pd.read_csv(folha_file, sep=';', encoding='latin1')
        folha_df['VALOR'] = folha_df['VALOR'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        folha_df['VALOR'] = pd.to_numeric(folha_df['VALOR'], errors='coerce')

        rubricas_texto = rubricas_file.getvalue().decode("latin1")
        grupos = carregar_rubricas(rubricas_texto)

        folha_df['COD'] = folha_df['COD'].astype(str)
        folha_df['GRUPO'] = folha_df['COD'].map(grupos).fillna('NÃO CLASSIFICADO')

        resultado = folha_df.groupby('GRUPO')['VALOR'].sum().reset_index().sort_values(by='VALOR', ascending=False)

        st.subheader("Resultado da Classificação")
        st.dataframe(resultado)
    except Exception as e:
        st.error(f"Erro ao processar os arquivos: {e}")
