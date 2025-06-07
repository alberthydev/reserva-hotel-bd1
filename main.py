import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget

from views.funcionario import AbaFuncionario
from views.funcao_funcionario import AbaFuncaoFuncionario
from views.hospede import AbaHospede
from views.quarto import AbaQuarto
from views.tipo_quarto import AbaTipoQuarto
from views.quarto_tipo import AbaQuartoTipo
from views.servico import AbaServico
from views.reserva import AbaReserva

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Hotelaria - Gestão")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.tabs.addTab(AbaFuncionario(), "Funcionário")
        self.tabs.addTab(AbaFuncaoFuncionario(), "Função Funcionário")
        self.tabs.addTab(AbaHospede(), "Hóspede")
        self.tabs.addTab(AbaQuarto(), "Quarto")
        self.tabs.addTab(AbaTipoQuarto(), "Tipo Quarto")
        self.tabs.addTab(AbaQuartoTipo(), "QuartoTipo")
        self.tabs.addTab(AbaServico(), "Serviço")
        self.tabs.addTab(AbaReserva(), "Reserva")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
