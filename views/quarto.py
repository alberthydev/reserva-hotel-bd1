from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QListWidget, QLabel, QMessageBox, QComboBox
from db import conectar

class AbaQuarto(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        form = QFormLayout()

        self.inputValor = QLineEdit()
        form.addRow("Valor do Quarto:", self.inputValor)

        self.comboStatus = QComboBox()
        self.comboStatus.addItems(['limpo', 'sujo', 'em limpeza'])
        form.addRow("Status Limpeza:", self.comboStatus)

        self.btnSalvar = QPushButton("Salvar Quarto")
        self.btnSalvar.clicked.connect(self.salvar)

        self.layout.addLayout(form)
        self.layout.addWidget(self.btnSalvar)

        self.lista = QListWidget()
        self.layout.addWidget(QLabel("Quartos cadastrados:"))
        self.layout.addWidget(self.lista)

        self.setLayout(self.layout)
        self.carregar()

    def carregar(self):
        self.lista.clear()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT numQuarto, vlrQuarto, statusLimpeza FROM quarto")
            for num, vlr, status in cursor.fetchall():
                self.lista.addItem(f"Quarto {num} - R$ {vlr} - Status: {status}")
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def salvar(self):
        valor = self.inputValor.text().strip()
        status = self.comboStatus.currentText()
        try:
            valor_float = float(valor)
        except:
            QMessageBox.warning(self, "Aviso", "Informe um valor numérico para o quarto")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO quarto (vlrQuarto, statusLimpeza) VALUES (%s, %s)", (valor_float, status))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sucesso", "Quarto salvo")
            self.inputValor.clear()
            self.carregar()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
