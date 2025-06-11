import csv
from collections import defaultdict

def carregar_rubricas(caminho_rubricas):
    mapa = {}
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

def processar_folha(caminho_folha, mapa_rubricas):
    totais = defaultdict(float)
    with open(caminho_folha, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            cod = row['COD'].strip()
            valor = float(row['VALOR'].replace('.', '').replace(',', '.'))
            grupo = mapa_rubricas.get(cod, 'Grupo Desconhecido')
            totais[grupo] += valor
    return totais

if __name__ == "__main__":
    rubricas = carregar_rubricas("rubricas.csv")
    totais = processar_folha("folha.csv", rubricas)

    print("Totais por grupo contábil:")
    for grupo, valor in totais.items():
        print(f"{grupo}: R$ {valor:,.2f}")
