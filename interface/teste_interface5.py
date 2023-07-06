import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class TelaInicial(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nome do Software")
        self.setStyleSheet("background-color: darkgreen; color: white;")
        self.initUI()

    def initUI(self):
        logo_label = QLabel(self)
        logo_label.setPixmap(QPixmap("LogotipoIF.png"))
        logo_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        nome_software_label = QLabel("Nome do Software", self)
        nome_software_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        texto_boas_vindas = QLabel("Texto de boas-vindas explicando o que é o software.", self)
        texto_boas_vindas.setStyleSheet("font-size: 14px;")

        matricula_label = QLabel("Número de Matrícula:", self)
        self.matricula_input = QLineEdit(self)
        enter_button = QPushButton("ENTER", self)
        enter_button.clicked.connect(self.mostrar_janela_acesso_permitido)

        layout = QVBoxLayout()
        layout.addWidget(logo_label)
        layout.addWidget(nome_software_label)
        layout.addWidget(texto_boas_vindas)
        layout.addWidget(matricula_label)
        layout.addWidget(self.matricula_input)
        layout.addWidget(enter_button)

        self.setLayout(layout)

    def mostrar_janela_acesso_permitido(self):
        matricula = self.matricula_input.text()
        if matricula:
            janela_acesso_permitido = QDialog(self)
            janela_acesso_permitido.setWindowTitle("Acesso Permitido")
            janela_acesso_permitido.setStyleSheet("background-color: darkgreen; color: white;")
            texto_acesso_permitido = QLabel("Acesso permitido", janela_acesso_permitido)
            texto_acesso_permitido.setStyleSheet("font-size: 18px; font-weight: bold;")
            janela_acesso_permitido.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela_inicial = TelaInicial()
    tela_inicial.show()
    sys.exit(app.exec_())
