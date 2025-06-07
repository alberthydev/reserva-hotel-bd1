from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QListWidget, QLabel, QMessageBox
from db import conectar

class AbaFuncionario(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        form = QFormLayout()

        self.inputNome = QLineEdit()
        form.addRow("Nome Funcionário:", self.inputNome)

        self.btnSalvar = QPushButton("Salvar Funcionário")
        self.btnSalvar.clicked.connect(self.salvar)

        self.layout.addLayout(form)
        self.layout.addWidget(self.btnSalvar)

        self.lista = QListWidget()
        self.layout.addWidget(QLabel("Funcionários cadastrados:"))
        self.layout.addWidget(self.lista)

        self.setLayout(self.layout)
        self.carregar()

    def carregar(self):
        self.lista.clear()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT codFuncionario, nomeFuncionario FROM funcionario")
            for cod, nome in cursor.fetchall():
                self.lista.addItem(f"{cod} - {nome}")
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def salvar(self):
        nome = self.inputNome.text()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO funcionario (nomeFuncionario) VALUES (%s)", (nome,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sucesso", "Funcionário salvo")
            self.inputNome.clear()
            self.carregar()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
