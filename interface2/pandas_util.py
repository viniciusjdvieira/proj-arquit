import pandas as pd

def verificar_matricula(matricula):
    try:
        # Carregar o arquivo pickle do DataFrame
        df = pd.read_pickle('dataframe_fono.pkl')

        # Verificar se a matrícula está presente no DataFrame
        if matricula in df['Matricula'].values:
            nome_pessoa = df.loc[df['Matricula'] == matricula, 'Nome'].values[0]
            return True, nome_pessoa
        else:
            return False, None
    except FileNotFoundError:
        return False, None
