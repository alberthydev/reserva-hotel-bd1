from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QPushButton, QListWidget, QLabel, 
    QMessageBox, QComboBox, QDateEdit
)
from PyQt5.QtCore import QDate
from db import conectar

class AbaReserva(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        form = QFormLayout()

        # Combo para escolher hóspede
        self.comboHospede = QComboBox()
        form.addRow("Hóspede:", self.comboHospede)

        # Combo para escolher quarto
        self.comboQuarto = QComboBox()
        form.addRow("Quarto:", self.comboQuarto)

        # Data entrada
        self.dateInicio = QDateEdit()
        self.dateInicio.setCalendarPopup(True)
        self.dateInicio.setDate(QDate.currentDate())
        form.addRow("Data de Entrada:", self.dateInicio)

        # Data saída
        self.dateFim = QDateEdit()
        self.dateFim.setCalendarPopup(True)
        self.dateFim.setDate(QDate.currentDate())
        form.addRow("Data de Saída:", self.dateFim)

        self.btnSalvar = QPushButton("Salvar Reserva")
        self.btnSalvar.clicked.connect(self.salvar)

        self.lista = QListWidget()

        self.layout.addLayout(form)
        self.layout.addWidget(self.btnSalvar)
        self.layout.addWidget(QLabel("Reservas cadastradas:"))
        self.layout.addWidget(self.lista)

        self.setLayout(self.layout)

        self.carregar()

    def carregar(self):
        self.lista.clear()
        self.comboHospede.clear()
        self.comboQuarto.clear()

        try:
            conn = conectar()
            cursor = conn.cursor()

            # Carregar hóspedes no combo
            cursor.execute("SELECT cpfHospede, nomeHospede FROM hospede ORDER BY nomeHospede")
            hospedes = cursor.fetchall()
            for cpf, nome in hospedes:
                self.comboHospede.addItem(nome, cpf)

            # Carregar quartos no combo
            cursor.execute("SELECT numQuarto FROM quarto ORDER BY numQuarto")
            quartos = cursor.fetchall()
            for (num,) in quartos:
                self.comboQuarto.addItem(str(num), num)

            # Carregar reservas para lista
            cursor.execute("""
                SELECT r.fk_hospede_cpfHospede, h.nomeHospede, r.fk_quarto_numQuarto, r.dtEntrada, r.dtSaida
                FROM reserva r
                JOIN hospede h ON r.fk_hospede_cpfHospede = h.cpfHospede
                ORDER BY r.dtEntrada DESC
            """)
            for cpf, nome, num, dt_entrada, dt_saida in cursor.fetchall():
                dt_saida_str = dt_saida.strftime("%Y-%m-%d") if dt_saida else "Indefinido"
                dt_entrada_str = dt_entrada.strftime("%Y-%m-%d") if dt_entrada else "Indefinido"
                self.lista.addItem(f"Reserva: {nome} (CPF: {cpf}) - Quarto {num} - De {dt_entrada_str} até {dt_saida_str}")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar dados:\n{e}")
        finally:
            cursor.close()
            conn.close()

    def salvar(self):
        cpf = self.comboHospede.currentData()
        quarto = self.comboQuarto.currentData()
        dt_entrada = self.dateInicio.date().toString("yyyy-MM-dd")
        dt_saida = self.dateFim.date().toString("yyyy-MM-dd")

        if not cpf or not quarto:
            QMessageBox.warning(self, "Aviso", "Selecione hóspede e quarto")
            return

        if self.dateFim.date() < self.dateInicio.date():
            QMessageBox.warning(self, "Aviso", "Data de saída deve ser igual ou maior que a data de entrada")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reserva (fk_hospede_cpfHospede, fk_quarto_numQuarto, dtEntrada, dtSaida)
                VALUES (%s, %s, %s, %s)
            """, (cpf, quarto, dt_entrada, dt_saida))
            conn.commit()
            QMessageBox.information(self, "Sucesso", "Reserva salva com sucesso")
            self.carregar()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar reserva:\n{e}")
        finally:
            cursor.close()
            conn.close()
