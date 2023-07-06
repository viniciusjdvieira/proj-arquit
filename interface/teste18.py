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
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import os
import soundfile as sf


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
    def __init__(self, numero_matricula):
        super().__init__()

        self.setWindowTitle("Terceira Janela")
        self.setGeometry(100, 100, 400, 300)

        self.numero_matricula = numero_matricula

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.opcao = None

        self.exibir_opcoes()

    def exibir_opcoes(self):
        opcoes_label = QLabel("Selecione uma opção:", self)
        opcoes_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        opcao1_button = QPushButton("Carregar um áudio", self)
        opcao1_button.clicked.connect(self.carregar_audio)

        opcao2_button = QPushButton("Gravar um áudio", self)
        opcao2_button.clicked.connect(self.gravar_audio)

        self.layout.addWidget(opcoes_label)
        self.layout.addWidget(opcao1_button)
        self.layout.addWidget(opcao2_button)

    def carregar_audio(self):
        self.opcao = "Carregar"

        # Abrir diálogo de seleção de arquivo
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Arquivos WAV (*.wav)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            # Obter o caminho do arquivo selecionado
            caminho_arquivo = file_dialog.selectedFiles()[0]

            self.abrir_janela_audio(caminho_arquivo)

    def gravar_audio(self):
        self.opcao = "Gravar"

        self.abrir_janela_gravacao()

    def abrir_janela_audio(self, caminho_arquivo):
        self.limpar_layout()

        # Carregar o arquivo de áudio
        audio = AudioSegment.from_file(caminho_arquivo)

        # Criar o player de áudio
        player = QSoundPlayer(audio)
        player.play()

        # Botões
        carregar_novamente_button = QPushButton("Carregar novamente", self)
        carregar_novamente_button.clicked.connect(self.carregar_audio)

        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.exibir_mensagem_ok)

        self.layout.addWidget(player)
        self.layout.addWidget(carregar_novamente_button)
        self.layout.addWidget(ok_button)

    def abrir_janela_gravacao(self):
        self.limpar_layout()

        gravar_label = QLabel("Pressione o botão 'Iniciar gravação' para gravar um áudio", self)
        gravar_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        iniciar_gravacao_button = QPushButton("Iniciar gravação", self)
        iniciar_gravacao_button.clicked.connect(self.iniciar_gravacao)

        self.layout.addWidget(gravar_label)
        self.layout.addWidget(iniciar_gravacao_button)

    
    def iniciar_gravacao(self):
        self.limpar_layout()

        # Definir o tempo de gravação em segundos
        duracao_gravacao = 5

        # Iniciar a gravação
        audio = sd.rec(int(duracao_gravacao * fs), samplerate=fs, channels=1)
        sd.wait()

        # Converter o áudio para o formato adequado
        audio = audio.flatten()

        # Salvar o áudio em um arquivo WAV
        nome_arquivo = f"grav_{self.numero_matricula}.wav"
        caminho_arquivo = os.path.join(os.path.dirname(os.path.realpath(__file__)), nome_arquivo)
        sf.write(caminho_arquivo, audio, fs)

        # Carregar o áudio gravado
        audio_gravado = AudioSegment.from_file(caminho_arquivo)

        # Criar o player de áudio
        player = QSoundPlayer(audio_gravado)
        player.play()

        # Botões
        gravar_novamente_button = QPushButton("Gravar novamente", self)
        gravar_novamente_button.clicked.connect(self.iniciar_gravacao)

        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.exibir_mensagem_ok)

        self.layout.addWidget(player)
        self.layout.addWidget(gravar_novamente_button)
        self.layout.addWidget(ok_button)

    def exibir_mensagem_ok(self):
        self.limpar_layout()

        ok_label = QLabel("OK", self)
        ok_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.layout.addWidget(ok_label)

    def limpar_layout(self):
        # Limpar o layout removendo todos os widgets
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

class QSoundPlayer(QWidget):
    def __init__(self, audio):
        super().__init__()

        self.audio = audio

        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent())

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        layout.addWidget(self.video_widget)

        self.setLayout(layout)

        self.player.setVideoOutput(self.video_widget)

        self.player.setMedia(QMediaContent())

        self.player.setMedia(QMediaContent())

        self.player.mediaChanged.connect(self.media_changed)

    def play(self):
        self.player.setMedia(QMediaContent())
        self.player.setMedia(QMediaContent())

    def media_changed(self):
        self.player.setMedia(self.audio)

        self.player.play()



class JanelaQuartaTela(QDialog):
    def __init__(self, tela_anterior):
        super().__init__(tela_anterior)
        self.setWindowTitle("Quarta Tela")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.setFixedSize(tela_anterior.size())  # Define o mesmo tamanho da tela anterior
        self.initUI()

    def initUI(self):
        mensagem_label = QLabel("OK", self)
        mensagem_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        layout = QVBoxLayout()
        layout.addWidget(mensagem_label)

        self.setLayout(layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela_inicial = TelaInicial()
    tela_inicial.show()
    sys.exit(app.exec_())