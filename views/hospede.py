from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QListWidget, QLabel, QMessageBox
from db import conectar

class AbaHospede(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        form = QFormLayout()

        self.inputCPF = QLineEdit()
        form.addRow("CPF do Hóspede:", self.inputCPF)

        self.inputNome = QLineEdit()
        form.addRow("Nome do Hóspede:", self.inputNome)

        self.btnSalvar = QPushButton("Salvar Hóspede")
        self.btnSalvar.clicked.connect(self.salvar)

        self.layout.addLayout(form)
        self.layout.addWidget(self.btnSalvar)

        self.lista = QListWidget()
        self.layout.addWidget(QLabel("Hóspedes cadastrados:"))
        self.layout.addWidget(self.lista)

        self.setLayout(self.layout)
        self.carregar()

    def carregar(self):
        self.lista.clear()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT cpfHospede, nomeHospede FROM hospede")
            for cpf, nome in cursor.fetchall():
                self.lista.addItem(f"{cpf} - {nome}")
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def salvar(self):
        cpf = self.inputCPF.text().strip()
        nome = self.inputNome.text().strip()
        if not cpf or not nome:
            QMessageBox.warning(self, "Aviso", "Preencha CPF e Nome")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO hospede (cpfHospede, nomeHospede) VALUES (%s, %s)", (cpf, nome))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sucesso", "Hóspede salvo")
            self.inputCPF.clear()
            self.inputNome.clear()
            self.carregar()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
