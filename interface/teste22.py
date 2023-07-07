import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
import pandas_util
import audio_util
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog
import numpy as np
import soundfile as sf
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtMultimedia import QAudioRecorder, QAudioEncoderSettings, QAudioDeviceInfo, QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
import os
import sounddevice as sd



class TelaInicial(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nome do Software")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.initUI()

    def initUI(self):
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("LogotipoIF.png")
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
                janela_acesso_permitido = JanelaAcessoPermitido(self, nome_pessoa, matricula)
                janela_acesso_permitido.show()
            else:
                QMessageBox.warning(self, "Matrícula não encontrada", "Matrícula não encontrada. Volte e tente novamente.")
                
class JanelaAcessoPermitido(QDialog):
    def __init__(self, tela_inicial, nome_pessoa, numero_matricula):
        super().__init__(tela_inicial)
        self.setWindowTitle("Acesso Permitido")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.setFixedSize(tela_inicial.size())  # Define o mesmo tamanho da primeira tela
        self.nome_pessoa = nome_pessoa
        self.numero_matricula = numero_matricula
        self.initUI()

    def initUI(self):
        texto_acesso_permitido = QLabel("Olá, " + self.nome_pessoa + ",\n vamos avaliar sua voz hoje?", self)
        texto_acesso_permitido.setStyleSheet("font-size: 18px; font-weight: bold;")

        voltar_button = QPushButton("Voltar", self)
        voltar_button.clicked.connect(self.voltar_tela_inicial)

        em_frente_button = QPushButton("Vamos em frente!", self)
        em_frente_button.clicked.connect(self.abrir_terceira_tela)

        layout = QVBoxLayout()
        layout.addWidget(texto_acesso_permitido)
        layout.addWidget(em_frente_button)
        layout.addWidget(voltar_button)

        self.setLayout(layout)

    def voltar_tela_inicial(self):
        self.close()
        self.parent().show()

    def abrir_terceira_tela(self):
        self.hide()
        janela_terceira_tela = JanelaTerceiraTela(self, self.numero_matricula)
        janela_terceira_tela.show()


class JanelaTerceiraTela(QDialog):
    def __init__(self, tela_anterior, numero_matricula):
        super().__init__(tela_anterior)

        self.tela_anterior = tela_anterior
        self.numero_matricula = numero_matricula

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.init_ui()

    def init_ui(self):
        gravar_button = QPushButton("Gravar", self)
        parar_button = QPushButton("Parar", self)
        ouvir_button = QPushButton("Ouvir", self)
        pausar_button = QPushButton("Pausar", self)
        gravar_novamente_button = QPushButton("Gravar Novamente", self)
        ok_button = QPushButton("OK", self)

        self.layout.addWidget(gravar_button)
        self.layout.addWidget(parar_button)
        self.layout.addWidget(ouvir_button)
        self.layout.addWidget(pausar_button)
        self.layout.addWidget(gravar_novamente_button)
        self.layout.addWidget(ok_button)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela_inicial = TelaInicial()
    tela_inicial.show()
    sys.exit(app.exec_())