from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QListWidget, QLabel, QMessageBox
from db import conectar

class AbaTipoQuarto(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        form = QFormLayout()

        self.inputDescricao = QLineEdit()
        form.addRow("Descrição Tipo Quarto:", self.inputDescricao)

        self.btnSalvar = QPushButton("Salvar Tipo Quarto")
        self.btnSalvar.clicked.connect(self.salvar)

        self.layout.addLayout(form)
        self.layout.addWidget(self.btnSalvar)

        self.lista = QListWidget()
        self.layout.addWidget(QLabel("Tipos de Quartos cadastrados:"))
        self.layout.addWidget(self.lista)

        self.setLayout(self.layout)
        self.carregar()

    def carregar(self):
        self.lista.clear()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT tipoID, descricaoTipo FROM tipoQuarto")
            for id_, desc in cursor.fetchall():
                self.lista.addItem(f"{id_} - {desc}")
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def salvar(self):
        desc = self.inputDescricao.text().strip()
        if not desc:
            QMessageBox.warning(self, "Aviso", "Informe uma descrição")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tipoQuarto (descricaoTipo) VALUES (%s)", (desc,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sucesso", "Tipo Quarto salvo")
            self.inputDescricao.clear()
            self.carregar()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
