from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QListWidget, QLabel, QMessageBox, QComboBox
from db import conectar

class AbaFuncaoFuncionario(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        form = QFormLayout()

        self.comboFuncionario = QComboBox()
        form.addRow("Funcionário:", self.comboFuncionario)

        self.inputFuncao = QLineEdit()
        form.addRow("Função:", self.inputFuncao)

        self.btnSalvar = QPushButton("Salvar Função")
        self.btnSalvar.clicked.connect(self.salvar)

        self.layout.addLayout(form)
        self.layout.addWidget(self.btnSalvar)

        self.lista = QListWidget()
        self.layout.addWidget(QLabel("Funções dos Funcionários:"))
        self.layout.addWidget(self.lista)

        self.setLayout(self.layout)
        self.carregarFuncionarios()
        self.carregar()

    def carregarFuncionarios(self):
        self.comboFuncionario.clear()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT codFuncionario, nomeFuncionario FROM funcionario")
            for cod, nome in cursor.fetchall():
                self.comboFuncionario.addItem(f"{nome} ({cod})", cod)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def carregar(self):
        self.lista.clear()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ff.codFuncionario, f.nomeFuncionario, ff.funcaoFuncionario
                FROM funcaoFuncionario ff
                JOIN funcionario f ON ff.codFuncionario = f.codFuncionario
            """)
            for cod, nome, funcao in cursor.fetchall():
                self.lista.addItem(f"{cod} - {nome}: {funcao}")
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def salvar(self):
        cod = self.comboFuncionario.currentData()
        funcao = self.inputFuncao.text().strip()
        if cod is None:
            QMessageBox.warning(self, "Aviso", "Selecione um funcionário")
            return
        if not funcao:
            QMessageBox.warning(self, "Aviso", "Digite a função")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO funcaoFuncionario (codFuncionario, funcaoFuncionario) VALUES (%s, %s)", (cod, funcao))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sucesso", "Função salva")
            self.inputFuncao.clear()
            self.carregar()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
