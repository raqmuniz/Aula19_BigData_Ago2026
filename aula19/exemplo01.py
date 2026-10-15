import pandas as pd 
import numpy as np


# Obtendo os dados
try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    # print(df_ocorrencias)

    # delimitando os dados
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    # print(df_roubo_veiculo.head(30))
    # print(df_roubo_veiculo.tail(30))


    # ### PREPARANDO OS DADOS
    # Totalizando os roubos por cidade (Var Qualitativa 'munic' e Var Quant 'roubo_veiculo')
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()


    # Ordenando os dados
    df_roubo_veiculo = df_roubo_veiculo.sort_values(
        by='roubo_veiculo',
        ascending=False
    )

    print(df_roubo_veiculo.head(10))
    # print(df_roubo_veiculo.tail(10))

except Exception as e:
    print(f'Erro ao obter os dados - {e}')



try:
    print(f'\nObtendo informações a cerca dos roubos dos veículos...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs(
        (media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100
    )

    print('\nMedidas de Tendência Central')
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância Média - Mediana: {distancia:.2f}%')


except Exception as e:
    print(f'Obtendo Medidas - {e}')



# Calculando os quartis
try:
    print(f'\nSeparando os quartis...')
    q1 = np.quantile(array_roubo_veiculo, .25)
    q2 = np.quantile(array_roubo_veiculo, .50)
    q3 = np.quantile(array_roubo_veiculo, .75)

    print('\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # Cidades c/ menos ocorrências de roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] < q1
    ]

    # Cidades c/ maiores ocorrências de roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] > q3
    ]

    # Menores
    print('\nMunicípios com menores roubos')
    print(30*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    # Exportando o dataframe
    # index=False - Não exporta os índices. Salva os dados das colunas munic e roubo_veiculo
    # sep=';' - Altera o separador de colunas para ';'
    # encoding='iso-8859-1' - Informa o encoding para salvar o csv. "Pode ser o mesmo"
    df_roubo_veiculo_menores.to_csv('menores.csv', index=False, sep=';', encoding='iso-8859-1')

    # Maiores
    print('\nMunicípios com maiores roubos')
    print(30*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))
    # Exportando o dataframe
    df_roubo_veiculo_maiores.to_csv('maiores.csv', index=False, sep=';', encoding='iso-8859-1')


except Exception as e:
    print(f'Erro ao analizar a distribuição {e}')

#Detectando outliers
    
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
    df_roubo_veiculo_outliers_menores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    )

    print('\nMunicípios com outliers inferiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_menores) == 0:
        print('Não há outliers inferiores')
    else:
        print(df_roubo_veiculo_outliers_menores)


except Exception as e:
    print(f'Erro ao analizar a distribuição {e}')

#filtrando os outliers menores    
    df_roubo_veiculo_outliers_maiores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    )
    print('\nMunicípios com outliers superiores')
    print(30*'-')

    if len(df_roubo_veiculo_outliers_maiores) == 0:
        print('Não há outliers superiores')
    else:
        print(df_roubo_veiculo_outliers_maiores)