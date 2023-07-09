import pandas as pd
import numpy as numpy
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor

data1 = '17/01/2023'
data2 = '19/03/2023'
data3 = '12/05/2023'
data4 = '16/07/2023'

def dados_recentes(paciente, matricula):
    '''
    coleta dados recentes do paciente
    '''
    df1 = pd.read_pickle('dataframe_base.pkl')
    df2 = pd.read_pickle('dataframe_pacientes.pkl')

    if matricula == '20201610001':
        df_v = df2.query("classe_formal==('20201610001')")
        
    elif matricula == '20201610002':
        df_v = df2.query("classe_formal==('20201610002')")
        
    elif matricula == '20201610003':
        df_v = df2.query("classe_formal==('20201610003')")
        
    elif matricula == '20201610004':
        df_v = df2.query("classe_formal==('20201610004')")
        
    elif matricula == '20201610005':
        df_v = df2.query("classe_formal==('20201610005')")
        
    elif matricula == '20201610006':
        df_v = df2.query("classe_formal==('20201610006')")
        
    elif matricula == '20201610007':
        df_v = df2.query("classe_formal==('20201610007')")
        
    elif matricula == '20201610008':
        df_v = df2.query("classe_formal==('20201610008')")
        
    elif matricula == '20201610009':
        df_v = df2.query("classe_formal==('20201610009')")
        

    df_v2 = df_v.query("data==('16/07/2023')")
    dft = pd.concat([df_v2, df1])

    fig, axs = plt.subplots(1, 2, figsize=(10, 2.5))
    cpps_data = [dft[dft['classe_formal'] == tag]['cpps'].values for tag in dft['classe_formal'].unique()]
    slope_data = [dft[dft['classe_formal'] == tag]['slope'].values for tag in dft['classe_formal'].unique()]
    axs[0].boxplot(cpps_data, labels=dft['classe_formal'].unique())
    axs[0].set_ylabel('cpps', fontsize=10)
    axs[1].boxplot(slope_data, labels=dft['classe_formal'].unique())
    axs[1].set_ylabel('slope', fontsize=10)
    fig.tight_layout()

    return fig


def tab_dados_recentes(paciente, matricula):
    '''
    coleta dados recentes do paciente
    '''
    df1 = pd.read_pickle('dataframe_base.pkl')
    df2 = pd.read_pickle('dataframe_pacientes.pkl')

    if matricula == '20201610001':
        df_v = df2.query("classe_formal==('20201610001')")
        
    elif matricula == '20201610002':
        df_v = df2.query("classe_formal==('20201610002')")
        
    elif matricula == '20201610003':
        df_v = df2.query("classe_formal==('20201610003')")
        
    elif matricula == '20201610004':
        df_v = df2.query("classe_formal==('20201610004')")
        
    elif matricula == '20201610005':
        df_v = df2.query("classe_formal==('20201610005')")
        
    elif matricula == '20201610006':
        df_v = df2.query("classe_formal==('20201610006')")
        
    elif matricula == '20201610007':
        df_v = df2.query("classe_formal==('20201610007')")
        
    elif matricula == '20201610008':
        df_v = df2.query("classe_formal==('20201610008')")
        
    elif matricula == '20201610009':
        df_v = df2.query("classe_formal==('20201610009')")
        

    df_v2 = df_v.query("data==('16/07/2023')")
    dft = pd.concat([df_v2, df1])

    
    df_tab = dft.groupby('classe_formal')[['cpps', 'slope', 'lpc1', 'lpc2',
                                       'lpc3', 'lpc4', 'lpc5', 'lpc6', 'lpc7',
                                       'lpc8', 'lpc9', 'lpc10', 'lpc11', 'lpc12']].mean()
                        
    df_tab_vert = df_tab.transpose()


    return df_tab


def gerar_tabela_valores_medios2(df_tab):
    tabela = QTableWidget()
    tabela.setColumnCount(len(df_tab.columns))
    tabela.setRowCount(len(df_tab))

    # Definir os cabeçalhos das colunas
    colunas = df_tab.columns.tolist()
    tabela.setHorizontalHeaderLabels(colunas)

    # Preencher a tabela com os valores médios
    for i, (tag, valores) in enumerate(df_tab.iterrows()):
        for j, valor in enumerate(valores):
            valor_arredondado = round(valor, 3)  # Arredonda para 3 casas decimais
            item = QTableWidgetItem(str(valor_arredondado))
            tabela.setItem(i, j, item)
        
        # Definir a tag como o rótulo da linha
        tabela.setVerticalHeaderItem(i, QTableWidgetItem(tag))

    # Ajustar o tamanho das colunas para que elas se ajustem ao conteúdo
    tabela.resizeColumnsToContents()

    return tabela

def gerar_tabela_valores_medios3(df_tab):
    tabela = QTableWidget()
    tabela.setColumnCount(len(df_tab.columns))
    tabela.setRowCount(len(df_tab))

    # Definir o estilo da tabela
    estilo_tabela = """
        QTableWidget {
            background-color: white;
            border: 1px solid black;
        }
        QTableWidget QHeaderView {
            background-color: white;
        }
        QTableWidget::item {
            color: black;
            background-color: white;
        }
        QTableWidget::item:selected {
            background-color: green;
        }
    """
    tabela.setStyleSheet(estilo_tabela)

    # Preencher a tabela com os valores médios
    for i, (tag, valores) in enumerate(df_tab.iterrows()):
        for j, valor in enumerate(valores):
            valor_arredondado = round(valor, 3)  # Arredonda para 3 casas decimais
            item = QTableWidgetItem(str(valor_arredondado))
            if isinstance(valor, str):  # Valores textuais (tags e keys)
                item.setForeground(QColor("black"))
            else:  # Valores numéricos
                item.setForeground(QColor("green"))
            tabela.setItem(i, j, item)

        # Definir a tag como o rótulo da linha
        item_tag = QTableWidgetItem(tag)
        item_tag.setForeground(QColor("black"))
        tabela.setVerticalHeaderItem(i, item_tag)

    # Ajustar o tamanho das colunas para que elas se ajustem ao conteúdo
    tabela.resizeColumnsToContents()

    return tabela

def gerar_tabela_valores_medios(df_tab):
    tabela = QTableWidget()
    tabela.setColumnCount(len(df_tab.columns))
    tabela.setRowCount(len(df_tab))

    # Definir o estilo da tabela
    estilo_tabela = """
        QTableWidget {
            background-color: white;
            border: 1px solid black;
        }
        QTableWidget QHeaderView {
            background-color: white;
        }
        QTableWidget::item {
            color: black;
            background-color: white;
        }
        QTableWidget::item:selected {
            background-color: green;
        }
    """
    tabela.setStyleSheet(estilo_tabela)

    # Preencher a tabela com os valores médios e nomes das medidas
    medidas = list(df_tab.columns)
    for i, (tag, valores) in enumerate(df_tab.iterrows()):
        for j, valor in enumerate(valores):
            valor_arredondado = round(valor, 3)  # Arredonda para 3 casas decimais
            item = QTableWidgetItem(str(valor_arredondado))
            if isinstance(valor, str):  # Valores textuais (tags e keys)
                item.setForeground(QColor("black"))
            else:  # Valores numéricos
                item.setForeground(QColor("green"))
            tabela.setItem(i, j, item)

            # Definir o nome da medida como rótulo da coluna
            item_medida = QTableWidgetItem(medidas[j])
            item_medida.setForeground(QColor("black"))
            tabela.setHorizontalHeaderItem(j, item_medida)

        # Definir a tag como o rótulo da linha
        item_tag = QTableWidgetItem(tag)
        item_tag.setForeground(QColor("black"))
        tabela.setVerticalHeaderItem(i, item_tag)

    # Ajustar o tamanho das colunas para que elas se ajustem ao conteúdo
    tabela.resizeColumnsToContents()

    return tabela

def dados_historicos(paciente, matricula):
    '''
    coleta dados recentes do paciente
    '''
    df1 = pd.read_pickle('dataframe_base.pkl')
    df2 = pd.read_pickle('dataframe_pacientes.pkl')

    if matricula == '20201610001':
        df_v = df2.query("classe_formal==('20201610001')")
        
    elif matricula == '20201610002':
        df_v = df2.query("classe_formal==('20201610002')")
        
    elif matricula == '20201610003':
        df_v = df2.query("classe_formal==('20201610003')")
        
    elif matricula == '20201610004':
        df_v = df2.query("classe_formal==('20201610004')")
        
    elif matricula == '20201610005':
        df_v = df2.query("classe_formal==('20201610005')")
        
    elif matricula == '20201610006':
        df_v = df2.query("classe_formal==('20201610006')")
        
    elif matricula == '20201610007':
        df_v = df2.query("classe_formal==('20201610007')")
        
    elif matricula == '20201610008':
        df_v = df2.query("classe_formal==('20201610008')")
        
    elif matricula == '20201610009':
        df_v = df2.query("classe_formal==('20201610009')")
        

    df_v2 = df_v
    dft = pd.concat([df_v2, df1])

    fig, axs = plt.subplots(1, 2, figsize=(10, 2.5))
    cpps_data = [dft[dft['classe_formal'] == tag]['cpps'].values for tag in dft['classe_formal'].unique()]
    slope_data = [dft[dft['classe_formal'] == tag]['slope'].values for tag in dft['classe_formal'].unique()]
    axs[0].boxplot(cpps_data, labels=dft['classe_formal'].unique())
    axs[0].set_ylabel('cpps', fontsize=10)
    axs[1].boxplot(slope_data, labels=dft['classe_formal'].unique())
    axs[1].set_ylabel('slope', fontsize=10)
    fig.tight_layout()

    return fig

def tab_dados_historicos(paciente, matricula):
    '''
    coleta dados recentes do paciente
    '''
    df1 = pd.read_pickle('dataframe_base.pkl')
    df2 = pd.read_pickle('dataframe_pacientes.pkl')

    if matricula == '20201610001':
        df_v = df2.query("classe_formal==('20201610001')")
        
    elif matricula == '20201610002':
        df_v = df2.query("classe_formal==('20201610002')")
        
    elif matricula == '20201610003':
        df_v = df2.query("classe_formal==('20201610003')")
        
    elif matricula == '20201610004':
        df_v = df2.query("classe_formal==('20201610004')")
        
    elif matricula == '20201610005':
        df_v = df2.query("classe_formal==('20201610005')")
        
    elif matricula == '20201610006':
        df_v = df2.query("classe_formal==('20201610006')")
        
    elif matricula == '20201610007':
        df_v = df2.query("classe_formal==('20201610007')")
        
    elif matricula == '20201610008':
        df_v = df2.query("classe_formal==('20201610008')")
        
    elif matricula == '20201610009':
        df_v = df2.query("classe_formal==('20201610009')")
        

    df_v2 = df_v
    dft = pd.concat([df_v2, df1])

    
    df_tab = dft.groupby('classe_formal')[['cpps', 'slope', 'lpc1', 'lpc2',
                                       'lpc3', 'lpc4', 'lpc5', 'lpc6', 'lpc7',
                                       'lpc8', 'lpc9', 'lpc10', 'lpc11', 'lpc12']].mean()
                        
    df_tab_vert = df_tab.transpose()


    return df_tab

def dados_todos():
    '''
    coleta dados recentes do paciente
    '''
    df1 = pd.read_pickle('dataframe_todos.pkl')  

    dft = df1

    fig, axs = plt.subplots(2, 1, figsize=(10, 3))
    cpps_data = [dft[dft['departamento'] == tag]['cpps'].values for tag in dft['departamento'].unique()]
    slope_data = [dft[dft['departamento'] == tag]['slope'].values for tag in dft['departamento'].unique()]
    axs[0].boxplot(cpps_data, labels=dft['departamento'].unique())
    axs[0].set_ylabel('cpps', fontsize=10)
    axs[1].boxplot(slope_data, labels=dft['departamento'].unique())
    axs[1].set_ylabel('slope', fontsize=10)
    fig.tight_layout()

    return fig

def tab_dados_todos():
    '''
    coleta dados recentes do paciente
    '''
    df1 = pd.read_pickle('dataframe_todos.pkl')     

    dft = df1

    df_tab = dft.groupby('departamento')[['cpps', 'slope', 'lpc1', 'lpc2',
                                       'lpc3', 'lpc4', 'lpc5', 'lpc6', 'lpc7',
                                       'lpc8', 'lpc9', 'lpc10', 'lpc11', 'lpc12']].mean()
                        

    return df_tab


def dados_depto(departamento):
    '''
    coleta dados recentes do paciente
    '''
    df1 = pd.read_pickle('dataframe_todos.pkl') 

    if departamento == 'Engenharia Elétrica':
        dft = df1.query("departamento==('SDL', 'PTL', 'eng_eletrica')")
    elif departamento == 'Engenharia Mecânica':
        dft = df1.query("departamento==('SDL', 'PTL', 'eng_mecanica')")
    elif departamento == 'Engenharia Civil':
        dft = df1.query("departamento==('SDL', 'PTL', 'eng_civil')")


    fig, axs = plt.subplots(2, 1, figsize=(10, 3))
    cpps_data = [dft[dft['departamento'] == tag]['cpps'].values for tag in dft['departamento'].unique()]
    slope_data = [dft[dft['departamento'] == tag]['slope'].values for tag in dft['departamento'].unique()]
    axs[0].boxplot(cpps_data, labels=dft['departamento'].unique())
    axs[0].set_ylabel('cpps', fontsize=10)
    axs[1].boxplot(slope_data, labels=dft['departamento'].unique())
    axs[1].set_ylabel('slope', fontsize=10)
    fig.tight_layout()

    return fig


def tab_dados_depto(departamento):
    '''
    coleta dados recentes do paciente
    '''
    df1 = pd.read_pickle('dataframe_todos.pkl')     

    if departamento == 'Engenharia Elétrica':
        dft = df1.query("departamento==('SDL', 'PTL', 'eng_eletrica')")
    elif departamento == 'Engenharia Mecânica':
        dft = df1.query("departamento==('SDL', 'PTL', 'eng_mecanica')")
    elif departamento == 'Engenharia Civil':
        dft = df1.query("departamento==('SDL', 'PTL', 'eng_civil')")

    df_tab = dft.groupby('departamento')[['cpps', 'slope', 'lpc1', 'lpc2',
                                       'lpc3', 'lpc4', 'lpc5', 'lpc6', 'lpc7',
                                       'lpc8', 'lpc9', 'lpc10', 'lpc11', 'lpc12']].mean()
                        

    return df_tab