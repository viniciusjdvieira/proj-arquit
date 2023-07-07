import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
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
from PyQt5.QtCore import QUrl, QTimer
import os
import sounddevice as sd
import datetime
import matplotlib.pyplot as plt
import plot_utils
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from avalia_sinal import get_probs

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
        self.setWindowTitle("Gravação do áudio")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.setFixedSize(tela_anterior.size())  # Define o mesmo tamanho da primeira tela

        self.tela_anterior = tela_anterior
        self.numero_matricula = numero_matricula

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.init_ui()
        
    def init_ui(self):
        # Mensagem de instruções
        mensagem_label = QLabel("Agora vamos gravar sua voz. Clique no botão abaixo para começar a gravar e aguarde 5 segundos. Você pode ouvir o áudio.", self)
        self.layout.addWidget(mensagem_label)

        # Botões
        gravar_button = QPushButton("Gravar", self)
        gravar_button.clicked.connect(self.gravar_audio)

        ouvir_button = QPushButton("Ouvir", self)
        ouvir_button.clicked.connect(self.ouvir_audio)

        pausar_button = QPushButton("Pausar", self)
        pausar_button.clicked.connect(self.pausar_audio)

        gravar_novamente_button = QPushButton("Gravar Novamente", self)
        gravar_novamente_button.clicked.connect(self.gravar_audio)

        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.abrir_quarta_janela)

        self.layout.addWidget(gravar_button)
        self.layout.addWidget(ouvir_button)
        self.layout.addWidget(pausar_button)
        self.layout.addWidget(gravar_novamente_button)
        self.layout.addWidget(ok_button)

        # Configurações do player de áudio
        self.player = QMediaPlayer()
        self.player.setVideoOutput(QVideoWidget())

        # Variáveis para a gravação
        self.frames = []
        self.gravando = False

    def gravar_audio(self):
        if not self.gravando:
            self.gravando = True
            self.frames = []
            duration = 5  # Duração da gravação em segundos
            fs = 22050  # Taxa de amostragem em Hz
            channels = 1  # Número de canais (mono)

            def callback(indata, frames, time, status):
                self.frames.append(indata.copy())

            with sd.InputStream(callback=callback, channels=channels, samplerate=fs):
                sd.sleep(int(duration * 1000))

            

            self.parar_gravacao()

            self.show()  # Exibir a janela de gravação

    def parar_gravacao(self):
        if self.gravando:
            self.gravando = False
            frames = np.concatenate(self.frames)
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.arquivo_gravacao = f"grav_{self.numero_matricula}_{current_time}.wav"  # Nome do arquivo de gravação
            sf.write(self.arquivo_gravacao, frames, samplerate=22050)


    def gravar_novamente(self):
        # Excluir a gravação anterior, se existir
        if os.path.exists(self.arquivo_gravacao):
            os.remove(self.arquivo_gravacao)
        #os.remove(f"grav_{self.numero_matricula}.wav")
        self.gravar_audio()

    def ouvir_audio(self):
        # Reproduzir o áudio gravado
        audio_url = QUrl.fromLocalFile(self.arquivo_gravacao)
        self.player.setMedia(QMediaContent(audio_url))
        self.player.play()

    def pausar_audio(self):
        self.player.pause()

    def abrir_quarta_janela(self):
        self.hide()
        quarta_janela = JanelaQuartaTela(self, self.arquivo_gravacao)
        quarta_janela.show()

###------------------------------

class JanelaQuartaTela(QDialog):
    def __init__(self, tela_anterior, audio_filename):
        super().__init__(tela_anterior)
        self.setWindowTitle("Quarta Tela")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        #self.setFixedSize(tela_anterior.size())  # Define o mesmo tamanho da tela anterior
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.audio_filename = audio_filename
        self.initUI()

    def initUI(self):
        mensagem_label = QLabel("Sua voz foi analisada! \n Veja o sinal e seu espectrograma abaixo:", self)
        mensagem_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.layout.addWidget(mensagem_label)

        # Figura da forma de onda
        figura_forma_onda = plot_utils.plot_signal_spec(self.audio_filename)
        canvas_forma_onda = FigureCanvas(figura_forma_onda)
        self.layout.addWidget(canvas_forma_onda)

        #Outra mensagem
        path_sinal = self.audio_filename
        path_modelo = 'project_model.h5'
        sdl_p , ptl_p = get_probs(path_sinal,path_modelo)
        mensagem_label = QLabel("Sua voz foi analisada! \n Veja o sinal e seu espectrograma abaixo:", self)
        mensagem_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.layout.addWidget(mensagem_label)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela_inicial = TelaInicial()
    tela_inicial.show()
    sys.exit(app.exec_())