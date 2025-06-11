import streamlit as st
import pandas as pd
import re
from io import StringIO

# --- Função para substituição ---
def substituir_codigos_por_valores(texto_com_codigos, df_codigos):
    mapa_codigos = {
        str(row['COD']): f"{row['DES']} ({row['VALOR']})"
        for _, row in df_codigos.iterrows()
    }

    codigos_ordenados = sorted(mapa_codigos.keys(), key=len, reverse=True)

    texto_substituido = texto_com_codigos
    codigos_substituidos = []
    for codigo in codigos_ordenados:
        padrao = r'\b' + re.escape(codigo) + r'\b'
        if re.search(padrao, texto_substituido):
            codigos_substituidos.append(codigo)
            texto_substituido = re.sub(padrao, mapa_codigos[codigo], texto_substituido)

    return texto_substituido, codigos_substituidos

# --- Dados em CSV embutido ---
dados_csv = """COD;TIPO;DES;VALOR
1;P;Horas Normais;175.851,23
3;P;Horas DSR;165,60
7;P;Horas Férias;17.484,95
9;P;Horas Atestado;902,03
14;P;Comissões;38.808,67
16;P;Aviso Prévio Ind.;3.356,25
17;P;Saldo de Salários;323,23
26;P;Horas Extras 50%;16.840,54
33;P;Horas Extras 100%;5.270,03
54;D;Desc. Adto de Férias;27.924,58
63;P;Ad. Insalubridade;3.256,96
64;P;Ad. Insalubridade s/ Férias;321,04
76;D;INSS s/ 13º Salário Resc.;112,98
77;D;Horas Faltas Injustificadas;241,23
91;D;Desc. Assistência Odontológica;91,64
104;D;INSS;23.400,44
105;D;INSS s/ Férias;2.939,26
108;D;IRRF;5.259,59
110;D;IRRF s/ Férias;1.041,81
124;V;Salário Família;587,16
154;P;Biênio;425,31
169;P;Pró-Labore;9.952,55
170;V;Saldo Negativo Folha;63,29
182;D;Líquido Rescisão;10.471,79
185;P;Reflexo DSR;15.577,18
1981;D;Desc.Adiant.Salarial;6.682,63
1995;P;Ajuda de Custo;19.343,10
1996;P;Premiação;34.575,95
2000;D;Auxílio-Educação;599,70
1049;D;Vale Transporte;828,89
"""
df_codigos = pd.read_csv(StringIO(dados_csv), sep=';')

# --- Streamlit UI ---
st.set_page_config(layout="centered", page_title="Substituidor de Códigos")
st.title("🧾 Substituidor de Códigos por Descrições e Valores")

st.markdown("Insira o texto com códigos que deseja substituir. Os códigos serão substituídos pelas descrições e valores equivalentes.")

col1, col2 = st.columns(2)

with col1:
    texto_de_entrada = st.text_area("Texto com Códigos", height=300)

with col2:
    if st.button("🔄 Substituir"):
        if texto_de_entrada:
            resultado, substituidos = substituir_codigos_por_valores(texto_de_entrada, df_codigos)
            st.subheader("Resultado:")
            st.code(resultado, language='text')
            st.info(f"Códigos substituídos: {len(substituidos)}")

            st.download_button(
                label="📥 Baixar Resultado",
                data=resultado,
                file_name="resultado_substituido.txt",
                mime="text/plain"
            )
        else:
            st.warning("Por favor, insira o texto com códigos antes de continuar.")

st.markdown("---")
st.markdown("### ℹ️ Ajuda")
st.markdown("- O sistema substitui apenas os códigos presentes na tabela interna.")
st.markdown("- Códigos que não forem encontrados permanecerão inalterados.")
