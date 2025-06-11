import streamlit as st

def substituir_codigos_por_valores(texto_com_codigos, dados_string):
    """
    Substitui códigos numéricos em um dado texto pelas suas descrições
    e valores correspondentes a partir de uma string de dados fornecida.

    Args:
        texto_com_codigos (str): O texto de entrada contendo os códigos a serem substituídos.
        dados_string (str): Uma string multi-linha onde cada linha contém
                            informações no formato 'COD;TIPO;DES;VALOR'.

    Returns:
        str: O texto com os códigos substituídos pelas suas descrições e valores.
             Retorna uma mensagem de erro se o formato dos dados estiver incorreto.
    """
    # Cria um dicionário para armazenar o mapeamento de código para descrição e valor
    mapa_codigos = {}
    
    # Divide a string de dados em linhas individuais
    linhas = dados_string.strip().split('\n')

    # Ignora a linha do cabeçalho se ela existir
    if linhas and linhas[0].startswith('COD;TIPO;DES;VALOR'):
        linhas = linhas[1:]

    for linha in linhas:
        parts = linha.split(';')
        if len(parts) == 4:
            codigo = parts[0].strip()
            descricao = parts[2].strip()
            valor = parts[3].strip() # Mantém o valor como string para substituição direta
            
            # Armazena a descrição e o valor combinados
            mapa_codigos[codigo] = f"{descricao} ({valor})"
        else:
            # Em Streamlit, é melhor usar st.warning ou st.error para mensagens de erro
            st.warning(f"Aviso: Ignorando linha de dados malformada: {linha}")
            continue

    # Itera sobre o mapa_codigos e substitui as ocorrências no texto
    # Ordenamos as chaves (códigos) pelo seu comprimento em ordem decrescente.
    # Isso é crucial para garantir que códigos mais longos (ex: '1049') sejam
    # substituídos antes de códigos mais curtos que podem ser seus prefixos (ex: '1').
    codigos_ordenados = sorted(mapa_codigos.keys(), key=len, reverse=True)

    texto_substituido = texto_com_codigos
    for codigo in codigos_ordenados:
        # Usamos uma substituição simples de string. Para cenários mais complexos
        # (por exemplo, garantir que é uma palavra inteira, não parte de outro número),
        # expressões regulares podem ser necessárias.
        texto_substituido = texto_substituido.replace(codigo, mapa_codigos[codigo])
            
    return texto_substituido

# --- Seus Dados Originais de Folha de Pagamento ---
# Estes são os dados que você forneceu inicialmente para mapeamento.
# Eles podem ser mantidos aqui ou lidos de um arquivo em uma aplicação mais complexa.
dados_folha_pagamento = """COD;TIPO;DES;VALOR
1;P;Horas Normais;175.851,23
3;P;Horas DSR;165,60
7;P;Horas Férias;17.484,95
9;P;Horas Atestado;902,03
14;P;Comissões;38.808,67
16;P;Aviso Prévio Ind.;3.356,25
17;P;Saldo de Salários;323,23
23;P;Horas Férias Prop. Resc.;2.279,08
26;P;Horas Extras 50%;16.840,54
33;P;Horas Extras 100%;5.270,03
43;P;Ad. 1/3 s/ Férias;7.976,41
45;P;Ad. 1/3 s/ Férias Prop. Resc.;1.027,92
51;P;13º Salário Prop. Resc.;800,22
52;P;13º Salário Ind. Resc.;266,74
63;P;Ad. Insalubridade;3.256,96
64;P;Ad. Insalubridade s/ Férias;321,04
70;P;Ad. Periculosidade s/ Férias;1.532,41
154;P;Biênio;425,31
169;P;Pró-Labore;9.952,55
185;P;Reflexo DSR;15.577,18
374;P;Diferença Horas Férias;401,56
375;P;Diferença Ad. 1/3 s/ Férias;133,86
398;P;Média H. E. s/ 13º Salário Prop. Re;61,37
399;P;Média H. E. s/ 13º Salário Ind. Res;20,46
400;P;Média H. E. s/ Férias;2.608,91
401;P;Média H. E. s/ Férias Prop. Resc.;187,54
404;P;Média H. E. s/ Aviso Prévio Ind.;353,68
407;P;Média Val. Variáveis s/ 13º Salário;180,76
408;P;Média Val. Variáveis s/ 13º Salário I;60,25
409;P;Média Val. Variáveis s/ Férias;1.670.46
410;P;Média Val. Variáveis s/ Férias Prop;392,13
413;P;Média Val. Variáveis s/ Aviso Prévi;515,23
420;P;Média Adicionais s/ 13º Salário Pro;68,05
421;P;Média Adicionais s/ 13º Salário Ind.;22,68
422;P;Média Adicionais s/ Férias;311,47
423;P;Média Adicionais s/ Férias Prop. R;225,00
426;P;Média Adicionais s/ Aviso Prévio In;424,28
523;P;Ad. Noturno s/ 13º Salário Ind. Res;25,89
633;P;Horas Férias Prop. Ind. Resc.;266,74
637;P;Média Val. Variáveis s/ Férias Prop;42,01
638;P;Média Adicionais s/ Férias Prop. In;32,14
651;P;Média H. E. s/ Férias Prop. Ind. Re;26,76
652;P;Ad. 1/3 s/ Férias Ind. Resc.;122,55
1025;P;Adicional Noturno 20%;1.012,67
1995;P;Ajuda de Custo;19.343,10
1996;P;Premiação;34.575,95
124;V;Salário Família;587,16
170;V;Saldo Negativo Folha;63,29
54;D;Desc. Adto de Férias;27.924,58
71;D;Pensão Alimentícia;536,69
76;D;INSS s/ 13º Salário Resc.;112,98
77;D;Horas Faltas Injustificadas;241,23
91;D;Desc. Assistência Odontológica De;91,64
104;D;INSS;23.400,44
105;D;INSS s/ Férias;2.939,26
108;D;IRRF;5.259,59
110;D;IRRF s/ Férias;1.041,81
182;D;Líquido Rescisão;10.471,79
380;D;INSS s/ Diferença de Férias;61,68
544;D;Desc. Saldo Neg. Folha Anterior;204,35
1049;D;Vale Transporte;828,89
1254;D;Desconto Alimentação;4.452.00
1981;D;Desc.Adiant.Salarial;6.682,63
2000;D;Auxílio-Educação;599,70
"""

# --- Configuração da Aplicação Streamlit ---
st.set_page_config(layout="centered", page_title="Substituidor de Códigos")

st.title("📝 Ferramenta de Substituição de Códigos")

st.write("Insira o texto que contém os códigos que deseja substituir. Os códigos serão substituídos pelas descrições e valores correspondentes da sua lista de dados.")

# Área de entrada para o texto com códigos
texto_de_entrada = st.text_area(
    "Cole o seu texto aqui:",
    height=300,
    value="""
400019;200102;400016;200038;400007;400018;40019201;400005;400191;400021;400013;400013;400006;100043;200038;200056;400019;400007;400180;400177;200034;200027;100042;200031;400181;
DESP. SALARIOS ; DESP. FÉRIAS ; HORAS EXTRAS ; SALA FAMILIA ;AVISO PRVIO IND; AD. INSALUBRIDADE ; AD. PERICUL. ; AD. NOTURNO ; BIENIO ; PRO LABORE ; GRATIFICAÇÃO ; PREMIOS ; AJUDA DE CUSTO ; DESC. ADTO FÉRIAS ; INSS ; IRRF ; DESC. SALARIOS ;AVISO PRVIO IND; ALIMENTAÇÃO ; PLANO SAUDE ; PENSÃO ALIM. ; DESC. ADTO 13° ; DESC. ADTO SAL ; LIQ. RESCIS. ; VT ;
1;7;26;124;16;63;;1.025;154;169;;1.996;1.995;54;76;108;77;;4.452;91;71;;1.981;182;1.049; TOTAL DESC. 
3;17;33;;51;64;;;;;;;;;104;110;2.000;;;;;;;;;
9;23;;;52;70;;;;;;;;;105;;544;;;;;;;;;
14;43;;;398;;;;;;;;;;380;;;;;;;;;;;
185;45;;;399;;;;;;;;;;;;;;;;;;;;;
170;374;;;401;;;;;;;;;;;;;;;;;;;;;
;375;;;404;;;;;;;;;;;;;;;;;;;;;
;400;;;407;;;;;;;;;;;;;;;;;;;;;
;409;;;408;;;;;;;;;;;;;;;;;;;;;
;410;;;413;;;;;;;;;;;;;;;;;;;;;
;422;;;420;;;;;;;;;;;;;;;;;;;;;
;423;;;421;;;;;;;;;;;;;;;;;;;;;
;633;;;426;;;;;;;;;;;;;;;;;;;;;
;637;;;523;;;;;;;;;;;;;;;;;;;;;
;638;;;;;;;;;;;;;;;;;;;;;;;;
;651;;;;;;;;;;;;;;;;;;;;;;;;
;652;;;;;;;;;;;;;;;;;;;;;;;;
"""
)

if st.button("Substituir Códigos"):
    if texto_de_entrada:
        texto_resultante = substituir_codigos_por_valores(texto_de_entrada, dados_folha_pagamento)
        st.subheader("Texto com Códigos Substituídos:")
        st.code(texto_resultante, language='text')
    else:
        st.warning("Por favor, insira algum texto para realizar a substituição.")

st.markdown("---")
st.markdown("### ℹ️ Como Funciona?")
st.write("Este aplicativo usa uma lista predefinida de códigos de folha de pagamento para substituir os códigos numéricos no seu texto pelas suas descrições e valores correspondentes. Por exemplo, '1' torna-se 'Horas Normais (175.851,23)'.")
st.write("Os códigos que não estão na lista predefinida permanecerão inalterados.")
