import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import pandas_util

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
                janela_acesso_permitido = JanelaAcessoPermitido(self, nome_pessoa)
                janela_acesso_permitido.show()
            else:
                QMessageBox.warning(self, "Matrícula não encontrada", "Matrícula não encontrada. Volte e tente novamente.")
                

class JanelaAcessoPermitido(QDialog):
    def __init__(self, tela_inicial, nome_pessoa):
        super().__init__(tela_inicial)
        self.setWindowTitle("Acesso Permitido")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.setFixedSize(tela_inicial.size())  # Define o mesmo tamanho da primeira tela
        self.nome_pessoa = nome_pessoa
        self.initUI()

    def initUI(self):
        texto_acesso_permitido = QLabel(f"Olá, {self.nome_pessoa},\n vamos avaliar sua voz hoje?", self)
        texto_acesso_permitido.setStyleSheet("font-size: 18px; font-weight: bold;")

        voltar_button = QPushButton("Voltar", self)
        voltar_button.clicked.connect(self.voltar_tela_inicial)

        layout = QVBoxLayout()
        layout.addWidget(texto_acesso_permitido)
        layout.addWidget(voltar_button)

        self.setLayout(layout)

    def voltar_tela_inicial(self):
        self.close()
        self.parent().show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela_inicial = TelaInicial()
    tela_inicial.show()
    sys.exit(app.exec_())
