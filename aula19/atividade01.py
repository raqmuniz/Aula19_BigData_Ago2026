import pandas as pd
import numpy as np

try:
    print('Obtendo dados...')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

#delimitando os dados
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding = 'iso-8859-1')

    df_estelionato = df_ocorrencias[['mes_ano', 'estelionato']]
    print(df_estelionato.head(30))

#preparando os dados
#Totalizando os casos de estelionato por cidade (Var Qualitativa 'munic' e Var Quant 'estelionato')
    
    df_estelionato = df_estelionato.groupby('mes_ano', as_index=False)['estelionato'].sum()

# Ordenando os dados
    df_estelionato = df_estelionato.sort_values(
        by='estelionato',
        ascending=False
    )

    print(df_estelionato.head(10))

except Exception as e:
    print(f'Erro ao obter os dados - {e}')

#Calculando as medidas de tendência central
try:
    print(f'\nObtendo informações a cerca dos casos de estelionato...')
    array_estelionato = np.array(df_estelionato['estelionato'])

    media_estelionato = np.mean(array_estelionato)
    mediana_estelionato = np.median(array_estelionato)
    distancia = abs(
        (media_estelionato - mediana_estelionato) / mediana_estelionato * 100
    )

    print('\nMedidas de Tendência Central')
    print(f'Média: {media_estelionato}')
    print(f'Mediana: {mediana_estelionato}')
    print(f'Distância Média - Mediana: {distancia:.2f}%')


except Exception as e:
    print(f'Obtendo Medidas - {e}')

# Calculando os quartis
try:
    print(f'\nSeparando os quartis...')
    q1 = np.quantile(array_estelionato, .25)
    q2 = np.quantile(array_estelionato, .50)
    q3 = np.quantile(array_estelionato, .75)

    print('\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # Períodos c/ menos ocorrências de roubos
    df_estelionato_menores = df_estelionato[
        df_estelionato['estelionato'] < q1
    ]

    # Períodos c/ maiores ocorrências de roubos
    df_estelionato_maiores = df_estelionato[
        df_estelionato['estelionato'] > q3
    ]

    # Menores
    print('\nPeríodos com menos casos de estelionato')
    print(30*'-')
    print(df_estelionato_menores.sort_values(by='estelionato', ascending=True))
    # Exportando o dataframe
    # index=False - Não exporta os índices. Salva os dados das colunas munic e roubo_veiculo
    # sep=';' - Altera o separador de colunas para ';'
    # encoding='iso-8859-1' - Informa o encoding para salvar o csv. "Pode ser o mesmo"
    df_estelionato_menores.to_csv('menores.csv', index=False, sep=';', encoding='iso-8859-1')

    # Maiores
    print('\nPeríodos com maiores casos de estelionato')
    print(30*'-')
    print(df_estelionato_maiores.sort_values(by='estelionato', ascending=False))
    # Exportando o dataframe
    df_estelionato_maiores.to_csv('maiores.csv', index=False, sep=';', encoding='iso-8859-1')


except Exception as e:
    print(f'Erro ao analizar a distribuição {e}')


#Desde 2003 os dados de estelionato foram computados por município, no estado do Rio de Janeiro. AS medidas de média e mediana (medidas de tendência central)
#não mostraram um padrão claro, pois a distância entre essas duas medidas foi maior que 50%
# De acordo com o calculo dos quartis, 25% dos dados mostram os períodos com menores valores de estelionato, e 75% dos dados mostram os períodos com maiores valores
# De um modo geral, os valores de menores e maiores quantidades de casos de estelionato mostram uma tendência de aumento dos casos, com o passar dos anos.
    
try:
#o iqr é o intervalo interquartil (50% dos dados centrais) iqr = q3 - q1 (amplitude dos dados centrais)
    iqr = q3 - q1

    #calculando os limites
    #superior
    limite_superior = q3 + (1.5 * iqr)

    #inferior
    limite_inferior = q1 - (1.5 * iqr)

    print(f'\nLimite superior: {limite_superior}')
    print(f'\nLimite inferior: {limite_inferior}')

#filtrando os outliers menores    
    df_estelionato_outliers_menores = (
        df_estelionato[df_estelionato['estelionato'] < limite_inferior]
    )

    print('\nMunicípios com outliers inferiores')
    print(30*'-')
    if len(df_estelionato_outliers_menores) == 0:
        print('Não há outliers inferiores')
    else:
        print(df_estelionato_outliers_menores)


except Exception as e:
    print(f'Erro ao analizar a distribuição {e}')

#filtrando os outliers menores    
    df_estelionato_outliers_maiores = (
        df_estelionato[df_estelionato['estelionato'] > limite_superior]
    )
    print('\nMunicípios com outliers superiores')
    print(30*'-')

    if len(df_estelionato_outliers_maiores) == 0:
        print('Não há outliers superiores')
    else:
        print(df_estelionato_outliers_maiores)