import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QFileDialog
import pandas_util
import audio_util
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QAudioRecorder, QAudioEncoderSettings, QAudioDeviceInfo
from PyQt5.QtMultimediaWidgets import QVideoWidget
import numpy as np
import soundfile as sf
import sounddevice as sd
import datetime
import matplotlib.pyplot as plt
import plot_utils
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import glob
import pandas as pd
from matplotlib.figure import Figure
from plots_pacientes import dados_recentes, tab_dados_recentes, gerar_tabela_valores_medios, dados_historicos, tab_dados_historicos, dados_todos, tab_dados_todos


class TelaInicial(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nome do Software")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.setWindowIcon(QIcon("LogotipoIF.png"))
        self.initUI()

    def initUI(self):
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("logoIFPB.png")
        logo_pixmap = logo_pixmap.scaledToWidth(300, Qt.SmoothTransformation)  # Ajuste de tamanho
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        nome_software_label = QLabel("Nome do Software", self)
        nome_software_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        texto_boas_vindas = QLabel("Texto de boas-vindas explicando o que é o software.", self)
        texto_boas_vindas.setStyleSheet("font-size: 14px;")

        matricula_label = QLabel("Número de Matrícula:", self)
        self.matricula_input = QLineEdit(self)
        enter_button = QPushButton("ENTER", self)
        enter_button.clicked.connect(self.verificar_acesso)

        layout = QVBoxLayout()
        layout.addWidget(logo_label)
        layout.addWidget(nome_software_label)
        layout.addWidget(texto_boas_vindas)
        layout.addWidget(matricula_label)
        layout.addWidget(self.matricula_input)
        layout.addWidget(enter_button)

        self.setLayout(layout)

    def verificar_acesso(self):
        matricula = self.matricula_input.text()
        if matricula:
            matricula_encontrada, nome_pessoa = pandas_util.verificar_matricula(matricula)
            if matricula_encontrada:
                self.hide()
                janela_acesso_permitido = JanelaAcessoPermitido(self, nome_pessoa)
                janela_acesso_permitido.show()
            else:
                QMessageBox.warning(self, "Matrícula não encontrada", "Matrícula não encontrada. Volte e tente novamente.")
                
class JanelaAcessoPermitido(QDialog):
    def __init__(self, tela_inicial, nome_pessoa):
        super().__init__(tela_inicial)
        self.setWindowTitle("Acesso Permitido")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.setWindowIcon(QIcon("LogotipoIF.png"))
        self.setFixedSize(tela_inicial.size())  # Define o mesmo tamanho da primeira tela
        self.nome_pessoa = nome_pessoa
        self.initUI()

    def initUI(self):
        texto_acesso_permitido = QLabel("Olá, " + self.nome_pessoa + ", vamos avaliar sua voz hoje?", self)
        texto_acesso_permitido.setStyleSheet("font-size: 18px; font-weight: bold;")

        avaliar_paciente_button = QPushButton("Avaliar Paciente", self)
        avaliar_paciente_button.clicked.connect(self.abrir_janela_avaliacao_paciente)

        avaliacao_geral_button = QPushButton("Avaliação Geral", self)
        avaliacao_geral_button.clicked.connect(self.abrir_avaliacao_geral)

        avaliacao_departamento_button = QPushButton("Avaliação por Departamento", self)
        avaliacao_departamento_button.clicked.connect(self.abrir_avaliacao_departamento)

        voltar_button = QPushButton("Voltar", self)
        voltar_button.clicked.connect(self.voltar_tela_inicial)

        layout = QVBoxLayout()
        layout.addWidget(texto_acesso_permitido)
        layout.addWidget(avaliar_paciente_button)
        layout.addWidget(avaliacao_geral_button)
        layout.addWidget(avaliacao_departamento_button)
        layout.addWidget(voltar_button)

        self.setLayout(layout)

    def voltar_tela_inicial(self):
        self.close()
        self.parent().show()

    def abrir_janela_avaliacao_paciente(self):
        self.hide()
        janela_avaliacao_paciente = JanelaAvaliacaoPaciente(self)
        janela_avaliacao_paciente.show()

    def abrir_terceira_tela(self):
        self.hide()
        janela_terceira_tela = JanelaTerceiraTela(self)
        janela_terceira_tela.show()

    def abrir_avaliacao_geral(self):
        self.hide()
        janela_avaliacao_geral = JanelaAvaliacaoGeral(self)
        janela_avaliacao_geral.show()

    def abrir_avaliacao_departamento(self):
        # Implemente a funcionalidade de avaliação por departamento
        pass



class JanelaTerceiraTela(QDialog):
    def __init__(self, tela_anterior):
        super().__init__(tela_anterior)
        self.setWindowTitle("Terceira Tela")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.setWindowIcon(QIcon("LogotipoIF.png"))
        self.setFixedSize(tela_anterior.size())  # Define o mesmo tamanho da tela anterior
        self.initUI()

    def initUI(self):
        mensagem_label = QLabel("OK", self)
        mensagem_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        layout = QVBoxLayout()
        layout.addWidget(mensagem_label)

        self.setLayout(layout)


class JanelaAvaliacaoPaciente(QDialog):
    def __init__(self, tela_anterior):
        super().__init__(tela_anterior)
        self.setWindowTitle("Avaliação de Paciente")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.setWindowIcon(QIcon("LogotipoIF.png"))
        self.setFixedSize(tela_anterior.size())  # Define o mesmo tamanho da tela anterior
        self.initUI()

    def initUI(self):
        texto_superior = QLabel("Avaliação de Paciente", self)
        texto_superior.setStyleSheet("font-size: 18px; font-weight: bold;")

        escolher_paciente_label = QLabel("Escolha um paciente:", self)
        self.paciente_combo_box = QComboBox(self)
        self.paciente_combo_box.currentIndexChanged.connect(self.selecionar_paciente)

        self.carregar_pacientes()

        dados_recentes_button = QPushButton("Dados recentes", self)
        dados_recentes_button.clicked.connect(self.abrir_dados_recentes)
        historico_button = QPushButton("Histórico", self)
        historico_button.clicked.connect(self.abrir_dados_historicos)
        voltar_button = QPushButton("Voltar", self)
        voltar_button.clicked.connect(self.voltar_tela_anterior)

        layout = QVBoxLayout()
        layout.addWidget(texto_superior)
        layout.addWidget(escolher_paciente_label)
        layout.addWidget(self.paciente_combo_box)
        layout.addWidget(dados_recentes_button)
        layout.addWidget(historico_button)
        layout.addWidget(voltar_button)

        self.setLayout(layout)

    def carregar_pacientes(self):
        try:
            dataframe_nomes = pd.read_pickle("dataframe_nomes.pkl")
            nomes_pacientes = dataframe_nomes["Nome"].tolist()
            self.paciente_combo_box.addItem("Selecione um paciente")
            self.paciente_combo_box.addItems(nomes_pacientes)
        except:
            QMessageBox.warning(self, "Erro", "Falha ao carregar os pacientes.")

    def selecionar_paciente(self, index):
        if index > 0:
            paciente_selecionado = self.paciente_combo_box.currentText()
            msg_box = QMessageBox()
            #msg_box.setWindowTitle("Paciente selecionado")
            #msg_box.setText(f"Paciente selecionado: {paciente_selecionado}")
            #msg_box.setIcon(QMessageBox.Information)
            #msg_box.setWindowIcon(QIcon("LogotipoIF.png"))  # Substitua o caminho pelo seu ícone .png
            #msg_box.exec_()
            QMessageBox.information(self, "Paciente selecionado", f"Paciente selecionado: {paciente_selecionado}")
            msg_box.setWindowIcon(QIcon("LogotipoIF.png"))

    def voltar_tela_anterior(self):
        self.close()
        self.parent().show()

    def abrir_dados_recentes(self):
        paciente_selecionado = self.paciente_combo_box.currentText()
        if paciente_selecionado:
            dataframe_pacientes = pd.read_pickle("dataframe_nomes.pkl")
            if "Matricula" in dataframe_pacientes.columns:
                paciente = dataframe_pacientes[dataframe_pacientes["Nome"] == paciente_selecionado]
                if not paciente.empty:
                    matricula = paciente["Matricula"].values[0]
                    janela_dados_recentes = JanelaDadosRecentes(self, paciente_selecionado, matricula)
                    janela_dados_recentes.show()
            else:
                QMessageBox.warning(self, "Erro", "A coluna 'Matricula' não está presente no DataFrame.")

    def abrir_dados_historicos(self):
        paciente_selecionado = self.paciente_combo_box.currentText()
        if paciente_selecionado:
            dataframe_pacientes = pd.read_pickle("dataframe_nomes.pkl")
            if "Matricula" in dataframe_pacientes.columns:
                paciente = dataframe_pacientes[dataframe_pacientes["Nome"] == paciente_selecionado]
                if not paciente.empty:
                    matricula = paciente["Matricula"].values[0]
                    janela_dados_historicos = JanelaDadosHistoricos(self, paciente_selecionado, matricula)
                    janela_dados_historicos.show()
            else:
                QMessageBox.warning(self, "Erro", "A coluna 'Matricula' não está presente no DataFrame.")


class JanelaDadosRecentes(QDialog):
    def __init__(self, tela_anterior, nome_paciente, matricula_paciente):
        super().__init__(tela_anterior)
        self.setWindowTitle("Dados Recentes")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.initUI(nome_paciente, matricula_paciente)

    def initUI(self, nome_paciente, matricula_paciente):
        texto_superior = QLabel("Dados Recentes - " + nome_paciente, self)
        texto_superior.setStyleSheet("font-size: 18px; font-weight: bold;")

        figura = dados_recentes(nome_paciente, matricula_paciente)
        figura_canvas = FigureCanvas(figura)

        texto_medio = QLabel("Valores médios das métricas", self)
        texto_medio.setStyleSheet("font-size: 16px;")

        df_tab = tab_dados_recentes(nome_paciente, matricula_paciente)
        tabela_valores_medios = gerar_tabela_valores_medios(df_tab)

        voltar_button = QPushButton("Voltar", self)
        voltar_button.clicked.connect(self.voltar_tela_avaliacao)

        layout = QVBoxLayout()
        layout.addWidget(texto_superior)
        layout.addWidget(figura_canvas)
        layout.addWidget(texto_medio)
        layout.addWidget(tabela_valores_medios)
        layout.addWidget(voltar_button)

        self.setLayout(layout)

    def voltar_tela_avaliacao(self):
        self.close()
        self.parent().show()


class JanelaDadosHistoricos(QDialog):
    def __init__(self, tela_anterior, nome_paciente, matricula_paciente):
        super().__init__(tela_anterior)
        self.setWindowTitle("Dados Históricos")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.initUI(nome_paciente, matricula_paciente)

    def initUI(self, nome_paciente, matricula_paciente):
        texto_superior = QLabel("Histórico - " + nome_paciente, self)
        texto_superior.setStyleSheet("font-size: 18px; font-weight: bold;")

        figura = dados_historicos(nome_paciente, matricula_paciente)
        figura_canvas = FigureCanvas(figura)

        texto_medio = QLabel("Valores médios das métricas", self)
        texto_medio.setStyleSheet("font-size: 16px;")

        df_tab = tab_dados_historicos(nome_paciente, matricula_paciente)
        tabela_valores_medios = gerar_tabela_valores_medios(df_tab)

        voltar_button = QPushButton("Voltar", self)
        voltar_button.clicked.connect(self.voltar_tela_avaliacao)

        layout = QVBoxLayout()
        layout.addWidget(texto_superior)
        layout.addWidget(figura_canvas)
        layout.addWidget(texto_medio)
        layout.addWidget(tabela_valores_medios)
        layout.addWidget(voltar_button)

        self.setLayout(layout)

    def voltar_tela_avaliacao(self):
        self.close()
        self.parent().show()


class JanelaAvaliacaoGeral(QDialog):
    def __init__(self, tela_anterior):
        super().__init__(tela_anterior)
        self.setWindowTitle("Avaliação Geral")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.initUI()

    def initUI(self):
        texto_superior = QLabel("Avaliação Geral - Departamentos", self)
        texto_superior.setStyleSheet("font-size: 18px; font-weight: bold;")

        figura = dados_todos()
        figura_canvas = FigureCanvas(figura)

        texto_medio = QLabel("Valores médios das métricas", self)
        texto_medio.setStyleSheet("font-size: 16px;")

        df_tab = tab_dados_todos()
        tabela_valores_medios = gerar_tabela_valores_medios(df_tab)

        voltar_button = QPushButton("Voltar", self)
        voltar_button.clicked.connect(self.voltar_tela_avaliacao)

        layout = QVBoxLayout()
        layout.addWidget(texto_superior)
        layout.addWidget(figura_canvas)
        layout.addWidget(texto_medio)
        layout.addWidget(tabela_valores_medios)
        layout.addWidget(voltar_button)

        self.setLayout(layout)

    def voltar_tela_avaliacao(self):
        self.close()
        self.parent().show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela_inicial = TelaInicial()
    tela_inicial.show()
    sys.exit(app.exec_())