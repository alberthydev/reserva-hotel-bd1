from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QPushButton, QListWidget, QLabel, QMessageBox, QComboBox
from db import conectar

class AbaQuartoTipo(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        form = QFormLayout()

        self.comboQuarto = QComboBox()
        form.addRow("Quarto:", self.comboQuarto)

        self.comboTipo = QComboBox()
        form.addRow("Tipo Quarto:", self.comboTipo)

        self.btnSalvar = QPushButton("Associar Quarto-Tipo")
        self.btnSalvar.clicked.connect(self.salvar)

        self.layout.addLayout(form)
        self.layout.addWidget(self.btnSalvar)

        self.lista = QListWidget()
        self.layout.addWidget(QLabel("Associações Quarto-Tipo:"))
        self.layout.addWidget(self.lista)

        self.setLayout(self.layout)
        self.carregarQuartos()
        self.carregarTipos()
        self.carregar()

    def carregarQuartos(self):
        self.comboQuarto.clear()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT numQuarto FROM quarto")
            for (num,) in cursor.fetchall():
                self.comboQuarto.addItem(str(num), num)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def carregarTipos(self):
        self.comboTipo.clear()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT tipoID, descricaoTipo FROM tipoQuarto")
            for tipoID, desc in cursor.fetchall():
                self.comboTipo.addItem(desc, tipoID)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def carregar(self):
        self.lista.clear()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT qt.numQuarto, t.descricaoTipo
                FROM quartoTipo qt
                JOIN tipoQuarto t ON qt.tipoID = t.tipoID
            """)
            for num, desc in cursor.fetchall():
                self.lista.addItem(f"Quarto {num} - Tipo: {desc}")
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def salvar(self):
        quarto = self.comboQuarto.currentData()
        tipo = self.comboTipo.currentData()
        if quarto is None or tipo is None:
            QMessageBox.warning(self, "Aviso", "Selecione quarto e tipo")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO quartoTipo (numQuarto, tipoID) VALUES (%s, %s)", (quarto, tipo))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sucesso", "Associação salva")
            self.carregar()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
