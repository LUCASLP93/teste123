import streamlit as st
import pandas as pd
import csv
from collections import defaultdict
import io # Para ler dados do arquivo carregado pelo Streamlit

# --- Funções existentes do seu processador.py ---
def carregar_rubricas(caminho_rubricas):
    mapa = {}
    # Adaptação para Streamlit: caminho_rubricas pode ser um objeto BytesIO
    try:
        # Tenta ler como arquivo local
        with open(caminho_rubricas, encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                grupo = row['GRUPO'].strip()
                cods = row['CODS'].split(',')
                for cod in cods:
                    cod = cod.strip()
                    if cod:
                        mapa[cod] = grupo
        return mapa
    except FileNotFoundError:
        st.error(f"Arquivo de rubricas não encontrado em {caminho_rubricas}. Por favor, verifique o caminho.")
        return {}
    except AttributeError: # Caso seja um objeto BytesIO (upload do streamlit)
        caminho_rubricas.seek(0) # Volta para o início do arquivo
        reader = csv.DictReader(io.TextIOWrapper(caminho_rubricas, encoding='utf-8'), delimiter=';')
        for row in reader:
            grupo = row['GRUPO'].strip()
            cods = row['CODS'].split(',')
            for cod in cods:
                cod = cod.strip()
                if cod:
                    mapa[cod] = grupo
        return mapa


def processar_folha(dados_folha, mapa_rubricas):
    totais = defaultdict(float)
    # Adaptação para Streamlit: dados_folha é um DataFrame do Pandas
    for index, row in dados_folha.iterrows():
        cod = str(row['COD']).strip() # Garante que COD é string
        
        # Converte o valor, tratando a vírgula como separador decimal
        try:
            valor_str = str(row['VALOR']).replace('.', '').replace(',', '.')
            valor = float(valor_str)
        except ValueError:
            st.warning(f"Atenção: Valor inválido '{row['VALOR']}' na linha {index + 2} da folha. Ignorando esta linha.")
            continue # Pula para a próxima linha

        grupo = mapa_rubricas.get(cod, 'Grupo Desconhecido')
        totais[grupo] += valor
    return totais

# --- Interface Streamlit ---
st.set_page_config(
    page_title="Classificador de Folha de Pagamento",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Classificador de Folha de Pagamento")
st.write("Carregue seus arquivos CSV de rubricas e folha para classificar os valores por grupo contábil.")

# Seção para carregar rubricas.csv
st.header("1. Carregar Rubricas")
st.info("O arquivo `rubricas.csv` deve ter as colunas `GRUPO` e `CODS` (códigos separados por vírgula).")
uploaded_rubricas_file = st.file_uploader("Escolha o arquivo rubricas.csv", type="csv", key="rubricas")

rubricas_map = {}
if uploaded_rubricas_file is not None:
    try:
        # Use o objeto uploaded_rubricas_file diretamente na função
        rubricas_map = carregar_rubricas(uploaded_rubricas_file)
        if rubricas_map:
            st.success("Rubricas carregadas com sucesso!")
            st.dataframe(pd.DataFrame(list(rubricas_map.items()), columns=['Código', 'Grupo']))
        else:
            st.warning("Nenhuma rubrica válida encontrada no arquivo.")
    except Exception as e:
        st.error(f"Erro ao carregar rubricas: {e}")
        st.info("Certifique-se de que o CSV usa `;` como delimitador e tem as colunas `GRUPO` e `CODS`.")
else:
    st.info("Aguardando upload do arquivo `rubricas.csv`...")


# Seção para carregar folha.csv
st.header("2. Carregar Folha de Pagamento")
st.info("O arquivo `folha.csv` deve ter as colunas `COD` e `VALOR`.")
uploaded_folha_file = st.file_uploader("Escolha o arquivo folha.csv", type="csv", key="folha")

if uploaded_folha_file is not None and rubricas_map:
    try:
        # Ler o CSV com pandas, usando ';' como delimitador
        df_folha = pd.read_csv(uploaded_folha_file, delimiter=';', encoding='utf-8')
        st.success("Folha de pagamento carregada com sucesso!")
        st.subheader("Prévia da Folha Carregada:")
        st.dataframe(df_folha.head()) # Mostra as primeiras linhas do DataFrame

        # Processar a folha
        if not df_folha.empty and 'COD' in df_folha.columns and 'VALOR' in df_folha.columns:
            st.header("3. Resultados da Classificação")
            totais_por_grupo = processar_folha(df_folha, rubricas_map)

            if totais_por_grupo:
                st.subheader("Totais por Grupo Contábil:")
                df_totais = pd.DataFrame(totais_por_grupo.items(), columns=['Grupo', 'Total'])
                df_totais['Total'] = df_totais['Total'].map('R$ {:,.2f}'.format) # Formata como moeda
                st.dataframe(df_totais)

                # Opcional: Mostrar detalhes dos grupos desconhecidos
                codigos_desconhecidos = [
                    row['COD'] for index, row in df_folha.iterrows()
                    if str(row['COD']).strip() not in rubricas_map and 'COD' in df_folha.columns
                ]
                if codigos_desconhecidos:
                    st.warning("Códigos de rubrica desconhecidos encontrados na folha:")
                    st.write(list(set(codigos_desconhecidos))) # Mostra apenas códigos únicos
            else:
                st.warning("Nenhum total foi calculado. Verifique se os dados estão corretos.")
        else:
            st.error("O arquivo da folha de pagamento não contém as colunas 'COD' e/ou 'VALOR' ou está vazio.")

    except pd.errors.EmptyDataError:
        st.error("O arquivo da folha de pagamento está vazio.")
    except Exception as e:
        st.error(f"Erro ao processar folha de pagamento: {e}")
        st.info("Certifique-se de que o CSV usa `;` como delimitador e tem as colunas `COD` e `VALOR`.")
elif uploaded_folha_file is not None and not rubricas_map:
    st.warning("Carregue o arquivo de rubricas primeiro.")
elif uploaded_folha_file is None:
    st.info("Aguardando upload do arquivo `folha.csv`...")

st.markdown("---")
st.markdown("Desenvolvido com ❤️ e Streamlit.")
