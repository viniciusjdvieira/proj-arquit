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
from pydub import AudioSegment
from pydub.playback import play

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
        self.setWindowTitle("Terceira Tela")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.setFixedSize(tela_anterior.size())  # Define o mesmo tamanho da tela anterior
        self.numero_matricula = numero_matricula
        self.initUI()

    def initUI(self):
        self.opcao = None  # Variável para armazenar a opção selecionada

        carregar_button = QPushButton("Carregar Áudio", self)
        carregar_button.setStyleSheet("font-size: 14px;")
        carregar_button.clicked.connect(self.carregar_audio)

        gravar_button = QPushButton("Gravar Áudio", self)
        gravar_button.setStyleSheet("font-size: 14px;")
        gravar_button.clicked.connect(self.gravar_audio)

        layout = QVBoxLayout()
        layout.addWidget(carregar_button)
        layout.addWidget(gravar_button)

        self.setLayout(layout)

    def carregar_audio(self):
        self.opcao = "Carregar"
        # Abrir diálogo de seleção de arquivo
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Arquivos WAV (*.wav)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            # Obter o caminho do arquivo selecionado
            caminho_arquivo = file_dialog.selectedFiles()[0]
            audio = audio_util.carregar_audio(caminho_arquivo)

            # Carregar o áudio usando a biblioteca pydub
            audio = AudioSegment.from_file(caminho_arquivo)

            # Criar botões de ação para reproduzir, carregar novamente ou confirmar
            reproduzir_button = QPushButton("Reproduzir", self)
            reproduzir_button.setStyleSheet("font-size: 14px;")
            reproduzir_button.clicked.connect(lambda: play(audio))

            carregar_novamente_button = QPushButton("Carregar Novamente", self)
            carregar_novamente_button.setStyleSheet("font-size: 14px;")
            carregar_novamente_button.clicked.connect(self.carregar_audio)

            ok_button = QPushButton("OK", self)
            ok_button.setStyleSheet("font-size: 14px;")
            ok_button.clicked.connect(self.abrir_quarta_tela)

            layout = QVBoxLayout()
            layout.addWidget(reproduzir_button)
            layout.addWidget(carregar_novamente_button)
            layout.addWidget(ok_button)

            self.setLayout(layout)

    def gravar_audio(self):
        self.opcao = "Gravar"
        # Implemente a lógica para gravar o áudio
        # Use a função gravar_audio() do módulo audio_util

        # Exemplo de uso:
        nome_arquivo = f"grav_{self.numero_matricula}.wav"
        caminho_arquivo = audio_util.gravar_audio(nome_arquivo)

        # Criar um player de áudio para reproduzir o áudio gravado
        player = QMediaPlayer()
        player.setMedia(QMediaContent(QUrl.fromLocalFile(caminho_arquivo)))

        # Criar botões de ação para gravar novamente ou confirmar
        gravar_novamente_button = QPushButton("Gravar Novamente", self)
        gravar_novamente_button.setStyleSheet("font-size: 14px;")
        gravar_novamente_button.clicked.connect(self.gravar_audio)

        ok_button = QPushButton("OK", self)
        ok_button.setStyleSheet("font-size: 14px;")
        ok_button.clicked.connect(self.abrir_quarta_tela)

        layout = QVBoxLayout()
        layout.addWidget(gravar_novamente_button)
        layout.addWidget(ok_button)

        # Adicionar o player de áudio ao layout
        player_layout = QVBoxLayout()
        player_layout.addWidget(player)
        layout.addLayout(player_layout)

        self.setLayout(layout)

    def abrir_quarta_tela(self):
        self.hide()
        janela_quarta_tela = JanelaQuartaTela(self)
        janela_quarta_tela.show()

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