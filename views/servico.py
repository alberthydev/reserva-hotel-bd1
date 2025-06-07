from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem,  # Itens corretos para a tabela
    QLabel, QMessageBox, QHBoxLayout
)

from db import conectar


class AbaServico(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        form = QFormLayout()

        self.lista = QTableWidget()
        self.layout.addWidget(QLabel("Funcionario/Serviço"))
        self.layout.addWidget(self.lista)

        self.setLayout(self.layout)

        self.carregar()

    def carregar(self):
        # self.lista agora é um QTableWidget
        self.servico_selecionado = None

        try:
            # --- Configuração da Tabela ---
            self.lista.setRowCount(0)
            self.lista.setColumnCount(2)
            self.lista.setHorizontalHeaderLabels(
                ["Cód. Funcionário", "Nº Quarto"])

            self.lista.verticalHeader().setVisible(False)

            # --- Busca dos Dados ---
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT fk_funcionario_codFuncionario, fk_quarto_numQuarto FROM servico")

            resultados = cursor.fetchall()

            # --- Preenchimento da Tabela ---
            for linha, (cod_func, num_quarto) in enumerate(resultados):
                self.lista.insertRow(linha)

                # str() garante que o dado é convertido para texto antes de criar o item
                item_cod = QTableWidgetItem(str(cod_func))
                item_quarto = QTableWidgetItem(str(num_quarto))

                self.lista.setItem(linha, 0, item_cod)
                self.lista.setItem(linha, 1, item_quarto)

                # Opcional: Ajusta o tamanho das colunas para caber o conteúdo
                self.lista.resizeColumnsToContents()

        except Exception as e:
            QMessageBox.critical(
                self, "Erro", f"Erro ao carregar os serviços:\n{e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()
