import sys
from datetime import date, datetime
from PyQt5.QtWidgets import (QApplication, QDialog, QMessageBox, QTableWidget,
                             QTableWidgetItem, QHeaderView, QComboBox)
from PyQt5.QtCore import QDate

from interface import Ui_Dialog
from db import conectar


class HotelReservationSystem(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Configuração inicial
        self.setWindowTitle("Sistema de Reserva de Hotel")
        self.db = conectar()
        if not self.db:
            QMessageBox.critical(
                self, "Erro", "Não foi possível conectar ao banco de dados")
            sys.exit(1)

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """Configura os sinais e slots da interface"""
        # Aba Funcionário
        self.saveEmployeeBtn.clicked.connect(self.add_employee)
        self.delEmployeeBtn.clicked.connect(self.delete_employee)
        self.saveServiceBtn.clicked.connect(self.assign_service)
        self.delServiceBtn.clicked.connect(self.delete_service)

        # Aba Quarto
        self.saveRoomBtn.clicked.connect(self.add_room)
        self.clearRoomBtn.clicked.connect(self.clear_room)
        self.delRoomBtn.clicked.connect(self.delete_room)

        # Aba Hóspede
        self.saveHostBtn.clicked.connect(self.add_guest)
        self.delHostBtn.clicked.connect(self.delete_guest)

        # Aba Reserva
        self.saveBookBtn.clicked.connect(self.add_reservation)
        self.delBookBtn.clicked.connect(self.delete_reservation)

        # Configura tabelas
        self.setup_tables()

    def setup_tables(self):
        """Configura as tabelas"""
        # Tabela de Funcionários
        self.employeeTableInput.setColumnCount(2)
        self.employeeTableInput.setHorizontalHeaderLabels(["ID", "Nome"])
        self.employeeTableInput.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.employeeTableInput.verticalHeader().setVisible(False)

        # Tabela de Funções
        self.funcTableInput.setColumnCount(3)
        self.funcTableInput.setHorizontalHeaderLabels(
            ["Funcionário", "Função", "Quarto"])
        self.funcTableInput.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.funcTableInput.verticalHeader().setVisible(False)

        # Tabela de Quartos
        self.roomTable.setColumnCount(3)
        self.roomTable.setHorizontalHeaderLabels(
            ["Número", "Valor", "Status Limpeza"])
        self.roomTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.roomTable.verticalHeader().setVisible(False)

        # Tabela de Hóspedes
        self.hostTable.setColumnCount(2)
        self.hostTable.setHorizontalHeaderLabels(["CPF", "Nome"])
        self.hostTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hostTable.verticalHeader().setVisible(False)

        # Tabela de Reservas
        self.bookTable.setColumnCount(6)
        self.bookTable.setHorizontalHeaderLabels(
            ["Hóspede", "Quarto", "Entrada", "Saída", "Pagamento", "Data da Reserva"])
        self.bookTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.bookTable.verticalHeader().setVisible(False)

    def execute_query(self, query, params=None, fetch=False):
        """Executa uma query no banco de dados"""
        cursor = self.db.cursor()
        try:
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            self.db.commit()
            return True
        except Exception as e:
            print(f"Erro na query: {e}")
            return False
        finally:
            cursor.close()

    def load_data(self):
        """Carrega dados iniciais"""
        self.load_employees()
        self.load_service()
        self.load_rooms()
        self.load_guests()
        self.load_reservations()
        self.update_comboboxes()

    def update_comboboxes(self):
        """Atualiza os comboboxes"""
        # Combobox de funcionários
        self.empCombo.clear()
        employees = self.execute_query(
            "SELECT codFuncionario, nomeFuncionario FROM funcionario", fetch=True)
        for emp in employees:
            self.empCombo.addItem(emp[1], emp[0])

        # Combox de Funções
        self.funcCombo.clear()
        services = [
            "Limpeza",
            "Manutenção",
            "Reposição de Frigobar",
            "Serviço de Quarto",
            "Recolher Louça"
        ]
        for service in services:
            self.funcCombo.addItem(service)
        if services:
            self.funcCombo.setCurrentIndex(0)

        # Combobox de Quartos para Serviço
        self.roomFuncCombo.clear()
        rooms = self.execute_query(
            "SELECT numQuarto FROM quarto", fetch=True
        )
        for room in rooms:
            self.roomFuncCombo.addItem(str(room[0]), room[0])
        self.roomFuncCombo.setCurrentIndex(0)

        # Combobox de hóspedes
        self.hostCombo.clear()
        guests = self.execute_query(
            "SELECT cpfHospede, nomeHospede FROM hospede", fetch=True)
        for guest in guests:
            self.hostCombo.addItem(guest[1], guest[0])

        # Combobox de quartos
        self.roomCombo.clear()
        rooms = self.execute_query("SELECT numQuarto FROM quarto", fetch=True)
        for room in rooms:
            self.roomCombo.addItem(str(room[0]), room[0])

        # Combox de Pagamento
        self.paymentCombo.clear()
        payments = [
            "Pix",
            "Crédito",
            "Débito",
            "Dinheiro",
        ]
        for payment in payments:
            self.paymentCombo.addItem(payment)
        if payments:
            self.paymentCombo.setCurrentIndex(0)

    def load_employees(self):
        """Carrega dados dos funcionários"""
        self.employeeTableInput.setRowCount(0)
        employees = self.execute_query("SELECT * FROM funcionario", fetch=True)
        for row, emp in enumerate(employees):
            self.employeeTableInput.insertRow(row)
            self.employeeTableInput.setItem(
                row, 0, QTableWidgetItem(str(emp[0])))
            self.employeeTableInput.setItem(row, 1, QTableWidgetItem(emp[1]))

    def load_service(self):
        """Carrega os serviços, mostrando funcionário, a tarefa específica e o quarto."""
        self.funcTableInput.setRowCount(0)

        # A query agora pega a descrição da tarefa diretamente da tabela 'servico'
        query = """
            SELECT
                f.nomeFuncionario,
                s.descricaoServico,
                s.fk_quarto_numQuarto
            FROM
                servico AS s
            JOIN
                funcionario AS f ON s.fk_funcionario_codFuncionario = f.codFuncionario
            ORDER BY
                f.nomeFuncionario
        """

        functions = self.execute_query(query, fetch=True)

        if not functions:
            return

        # O laço continua o mesmo, preenchendo as 3 colunas
        for row, func_data in enumerate(functions):
            self.funcTableInput.insertRow(row)
            self.funcTableInput.setItem(row, 0, QTableWidgetItem(func_data[0]))
            self.funcTableInput.setItem(row, 1, QTableWidgetItem(func_data[1]))
            self.funcTableInput.setItem(
                row, 2, QTableWidgetItem(str(func_data[2])))

    def load_rooms(self):
        """Carrega dados dos quartos"""
        self.roomTable.setRowCount(0)
        rooms = self.execute_query("SELECT * FROM quarto", fetch=True)
        for row, room in enumerate(rooms):
            self.roomTable.insertRow(row)
            self.roomTable.setItem(row, 0, QTableWidgetItem(str(room[0])))
            self.roomTable.setItem(row, 1, QTableWidgetItem(str(room[1])))
            self.roomTable.setItem(
                row, 2, QTableWidgetItem(room[2] if room[2] else ""))

    def load_guests(self):
        """Carrega dados dos hóspedes"""
        self.hostTable.setRowCount(0)
        guests = self.execute_query("SELECT * FROM hospede", fetch=True)
        for row, guest in enumerate(guests):
            self.hostTable.insertRow(row)
            self.hostTable.setItem(row, 0, QTableWidgetItem(guest[0]))
            self.hostTable.setItem(row, 1, QTableWidgetItem(guest[1]))

    def load_reservations(self):
        """Carrega dados das reservas, incluindo a data de criação."""
        self.bookTable.setRowCount(0)

        # 1. SQL MODIFICADO: Adicionamos 'r.dataCriacao' e ordenamos por ela.
        reservations = self.execute_query("""
            SELECT h.nomeHospede, r.fk_quarto_numQuarto, r.dtEntrada, r.dtSaida, r.formaPagamento, r.dataCriacao
            FROM reserva r
            JOIN hospede h ON r.fk_hospede_cpfHospede = h.cpfHospede
            ORDER BY r.dataCriacao DESC
        """, fetch=True)

        if not reservations:
            return  # Sai da função se não houver reservas

        for row, res in enumerate(reservations):
            self.bookTable.insertRow(row)

            # 2. LAÇO MODIFICADO: Agora percorre as 6 colunas
            for col in range(6):
                value = res[col]
                formatted_value = ""

                # 3. FORMATAÇÃO INTELIGENTE: Formata datas e horários de forma amigável
                if isinstance(value, datetime):  # Para a coluna 'dataCriacao'
                    formatted_value = value.strftime("%d/%m/%Y %H:%M")
                elif isinstance(value, date):  # Para 'dtEntrada' e 'dtSaida'
                    formatted_value = value.strftime("%d/%m/%Y")
                # Para outros valores (nome, quarto, etc.)
                elif value is not None:
                    formatted_value = str(value)
                # Se value for None, formatted_value continuará ""

                self.bookTable.setItem(
                    row, col, QTableWidgetItem(formatted_value))

    # Métodos CRUD para Funcionários

    def add_employee(self):
        """Adiciona um novo funcionário"""
        name = self.nmFuncInput.text().strip()
        if not name:
            QMessageBox.warning(self, "Aviso", "Informe o nome do funcionário")
            return

        if self.execute_query("INSERT INTO funcionario (nomeFuncionario) VALUES (%s)", (name,)):
            self.nmFuncInput.clear()
            self.load_employees()
            self.update_comboboxes()
            QMessageBox.information(self, "Sucesso", "Funcionário adicionado")
        else:
            QMessageBox.critical(
                self, "Erro", "Falha ao adicionar funcionário")

    def delete_employee(self):
        """Remove um funcionário"""
        selected = self.employeeTableInput.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Aviso", "Selecione um funcionário")
            return

        emp_id = self.employeeTableInput.item(selected, 0).text()

        reply = QMessageBox.question(self, "Confirmar",
                                     "Tem certeza que deseja remover este funcionário?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.execute_query("DELETE FROM funcionario WHERE codFuncionario = %s", (emp_id,)):
                self.load_employees()
                self.update_comboboxes()
            else:
                QMessageBox.critical(
                    self, "Erro", "Falha ao remover funcionário")

    # Métodos CRUD para Funções
    def assign_service(self):
        """Atribui um serviço para um funcionário em um quarto específico."""

        # 1. Obter os dados dos seus ComboBoxes
        #    Use os nomes corretos dos seus widgets aqui
        employee_id = self.empCombo.currentData()
        room_number = self.roomFuncCombo.currentData()
        # Pega o texto da função para usar na mensagem
        function_name = self.funcCombo.currentText()

        # 2. Validações para garantir que o usuário selecionou tudo
        if not employee_id:
            QMessageBox.warning(self, "Aviso", "Selecione um funcionário.")
            return
        if not room_number:
            QMessageBox.warning(self, "Aviso", "Selecione um quarto.")
            return

        # 3. Tenta inserir a nova atribuição na tabela 'servico'
        try:
            query = "INSERT INTO servico (fk_funcionario_codFuncionario, fk_quarto_numQuarto, descricaoServico) VALUES (%s, %s, %s)"
            params = (employee_id, room_number, function_name)

            if self.execute_query(query, params):
                QMessageBox.information(self, "Sucesso",
                                        f"Serviço de '{function_name}' atribuído ao quarto {room_number} com sucesso!")

                # Recarrega a tabela principal que agora lê os dados da tabela 'servico'
                self.load_service()
            else:
                # Caso execute_query retorne False por algum motivo não excepcional
                raise Exception("A query de inserção falhou.")

        except Exception as e:
            # Trata erros comuns, como tentar adicionar a mesma atribuição duas vezes (chave duplicada)
            if 'Duplicate entry' in str(e):
                QMessageBox.critical(
                    self, "Erro", "Este funcionário já está atribuído a um serviço neste quarto.")
            else:
                QMessageBox.critical(
                    self, "Erro de Banco de Dados", f"Falha ao atribuir o serviço.\n\nErro: {e}")

    def delete_service(self):
        """Remove uma atribuição de serviço específica."""
        selected = self.funcTableInput.currentRow()
        if selected == -1:
            QMessageBox.warning(
                self, "Aviso", "Selecione um serviço para remover.")
            return

        # 1. Pegamos os 3 dados da linha selecionada
        emp_name = self.funcTableInput.item(selected, 0).text()
        service_description = self.funcTableInput.item(selected, 1).text()
        room_number = self.funcTableInput.item(selected, 2).text()

        # 2. Pede uma confirmação mais clara ao usuário
        reply = QMessageBox.question(self, "Confirmar Exclusão",
                                     f"Tem certeza que deseja remover o serviço '{
                                         service_description}' do quarto {room_number} "
                                     f"atribuído a {emp_name}?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                # 3. Usa o nome para buscar o ID do funcionário
                result = self.execute_query(
                    "SELECT codFuncionario FROM funcionario WHERE nomeFuncionario = %s LIMIT 1",
                    (emp_name,),
                    fetch=True
                )

                if not result:
                    QMessageBox.critical(
                        self, "Erro", f"Não foi possível encontrar o ID para o funcionário {emp_name}.")
                    return

                emp_id = result[0][0]

                # 4. Executa o DELETE na tabela 'servico' usando a chave primária completa
                delete_success = self.execute_query(
                    "DELETE FROM servico WHERE fk_funcionario_codFuncionario = %s AND fk_quarto_numQuarto = %s AND descricaoServico = %s",
                    (emp_id, room_number, service_description)
                )

                if delete_success:
                    QMessageBox.information(
                        self, "Sucesso", "Serviço removido com sucesso!")
                    self.load_service()  # Atualiza a tabela na UI
                else:
                    raise Exception("A query de exclusão falhou.")

            except Exception as e:
                QMessageBox.critical(self, "Erro de Banco de Dados",
                                     f"Falha ao remover o serviço.\n\nErro: {e}")

    # Métodos CRUD para Quartos
    def add_room(self):
        """Adiciona um novo quarto"""
        try:
            value = float(self.vlrRoom.text())
        except ValueError:
            QMessageBox.warning(self, "Aviso", "Informe um valor válido")
            return

        if self.execute_query("INSERT INTO quarto (vlrQuarto) VALUES (%s)", (value,)):
            self.vlrRoom.clear()
            self.load_rooms()
            self.update_comboboxes()
            QMessageBox.information(self, "Sucesso", "Quarto adicionado")
        else:
            QMessageBox.critical(self, "Erro", "Falha ao adicionar quarto")

    def clear_room(self):
        """
        Altera o status de um quarto selecionado para 'Limpo'.
        Esta função deve ser conectada ao sinal 'clicked' do seu botão 'Limpar Quarto'.
        """
        # 1. Identificar a linha selecionada na tabela de quartos
        #    Substitua 'self.suaTabelaDeQuartos' pelo nome real do seu QTableWidget de quartos
        quartos = self.roomTable
        selected_row = quartos.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
                self, "Aviso", "Por favor, selecione um quarto na tabela para limpar.")
            return

        # 2. Obter os dados do quarto a partir da linha selecionada
        #    Ajuste os índices das colunas (0, 2) conforme a sua tabela
        room_number = quartos.item(selected_row, 0).text()
        current_status = quartos.item(selected_row, 2).text()

        # 3. Validação: Verificar se o quarto já não está limpo
        if current_status == 'Limpo':
            QMessageBox.information(self, "Informação", f"O quarto {
                                    room_number} já está limpo.")
            return

        # 4. Pedir confirmação ao usuário
        reply = QMessageBox.question(self, "Confirmar Limpeza",
                                     f"Deseja marcar o quarto {
                                         room_number} como 'Limpo'?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 5. Executar o comando UPDATE no banco de dados
            try:
                query = "UPDATE quarto SET statusLimpeza = 'Limpo' WHERE numQuarto = %s"

                if self.execute_query(query, (room_number,)):
                    QMessageBox.information(self, "Sucesso", f"O quarto {
                                            room_number} foi limpo com sucesso!")

                    # 6. Atualizar a tabela de quartos na UI para refletir a mudança
                    #    Substitua 'self.load_rooms' pelo nome real da sua função que carrega os quartos
                    self.load_rooms()
                else:
                    raise Exception(
                        "A query foi executada mas não retornou sucesso.")

            except Exception as e:
                QMessageBox.critical(self, "Erro de Banco de Dados",
                                     f"Não foi possível atualizar o status do quarto.\n\nErro: {e}")

    def delete_room(self):
        """Remove um quarto"""
        selected = self.roomTable.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Aviso", "Selecione um quarto")
            return

        room_num = self.roomTable.item(selected, 0).text()

        reply = QMessageBox.question(self, "Confirmar",
                                     "Tem certeza que deseja remover este quarto?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.execute_query("DELETE FROM quarto WHERE numQuarto = %s", (room_num,)):
                self.load_rooms()
                self.update_comboboxes()
            else:
                QMessageBox.critical(self, "Erro", "Falha ao remover quarto")

    # Métodos CRUD para Hóspedes
    def add_guest(self):
        """Adiciona um novo hóspede"""
        cpf = self.cpfInput.text().strip()
        name = self.nameInput.text().strip()

        if not cpf:
            QMessageBox.warning(self, "Aviso", "Informe o CPF")
            return
        if not name:
            QMessageBox.warning(self, "Aviso", "Informe o nome")
            return

        if self.execute_query("INSERT INTO hospede (cpfHospede, nomeHospede) VALUES (%s, %s)",
                              (cpf, name)):
            self.cpfInput.clear()
            self.nameInput.clear()
            self.load_guests()
            self.update_comboboxes()
            QMessageBox.information(self, "Sucesso", "Hóspede adicionado")
        else:
            QMessageBox.critical(self, "Erro", "Falha ao adicionar hóspede")

    def delete_guest(self):
        """Remove um hóspede"""
        selected = self.hostTable.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Aviso", "Selecione um hóspede")
            return

        cpf = self.hostTable.item(selected, 0).text()

        reply = QMessageBox.question(self, "Confirmar",
                                     "Tem certeza que deseja remover este hóspede?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.execute_query("DELETE FROM hospede WHERE cpfHospede = %s", (cpf,)):
                self.load_guests()
                self.update_comboboxes()
            else:
                QMessageBox.critical(self, "Erro", "Falha ao remover hóspede")

    # Métodos CRUD para Reservas
    def is_room_available(self, room_number, check_in_date, check_out_date):
        """Verifica se um quarto não tem reservas conflitantes."""
        query = """
            SELECT COUNT(*) FROM reserva
            WHERE fk_quarto_numQuarto = %s AND dtEntrada < %s AND dtSaida > %s
        """
        result = self.execute_query(
            query, (room_number, check_out_date, check_in_date), fetch=True
        )
        return result and result[0][0] == 0

    def get_room_status(self, room_number):
        """Busca o status de limpeza de um quarto."""
        query = "SELECT statusLimpeza FROM quarto WHERE numQuarto = %s"
        result = self.execute_query(query, (room_number,), fetch=True)
        return result[0][0] if result else None

    def add_reservation(self):
        """Adiciona uma nova reserva com validações completas."""
        guest_cpf = self.hostCombo.currentData()
        room_number = self.roomCombo.currentData()
        check_in_str = self.dtEnter.text().strip()
        check_out_str = self.dtOut.text().strip()
        payment_method = self.paymentCombo.currentText()

        # 1. Validações de preenchimento da UI
        if not all([guest_cpf, room_number, check_in_str]):
            QMessageBox.warning(
                self, "Aviso", "Hóspede, quarto e data de entrada são obrigatórios.")
            return

        # 2. Validação e conversão das datas
        try:
            check_in_obj = datetime.strptime(check_in_str, "%d/%m/%Y")
            check_out_obj = datetime.strptime(
                check_out_str, "%d/%m/%Y") if check_out_str else None

            if check_out_obj and check_in_obj >= check_out_obj:
                QMessageBox.warning(
                    self, "Data Inválida", "A data de saída deve ser posterior à de entrada.")
                return

        except ValueError:
            QMessageBox.warning(self, "Formato Inválido",
                                "Informe datas no formato DD/MM/AAAA.")
            return

        # 3. VALIDAÇÃO DO STATUS DO QUARTO (NOVO!)
        room_status = self.get_room_status(room_number)
        if room_status != 'Limpo':
            QMessageBox.warning(self, "Quarto Indisponível",
                                f"Não é possível reservar este quarto. Status atual: {room_status}.")
            return

        # 4. VALIDAÇÃO DE CONFLITO DE DATAS
        if check_out_obj:  # Só checa conflito se houver data de saída
            # Converte datas para o formato do banco (YYYY-MM-DD)
            check_in_db = check_in_obj.strftime("%Y-%m-%d")
            check_out_db = check_out_obj.strftime("%Y-%m-%d")

            if not self.is_room_available(room_number, check_in_db, check_out_db):
                QMessageBox.warning(
                    self, "Conflito de Datas", "O quarto já está reservado para este período.")
                return
        else:  # Se não há data de saída, apenas formata a de entrada
            check_in_db = check_in_obj.strftime("%Y-%m-%d")
            check_out_db = None

        # 5. Se todas as validações passaram, executa o INSERT
        try:
            query = """
                INSERT INTO reserva (fk_hospede_cpfHospede, fk_quarto_numQuarto, dtEntrada, dtSaida, formaPagamento, dataCriacao)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """
            params = (guest_cpf, room_number, check_in_db,
                      check_out_db, payment_method)

            if self.execute_query(query, params):
                self.dtEnter.clear()
                self.dtOut.clear()
                self.load_reservations()
                QMessageBox.information(
                    self, "Sucesso", "Reserva adicionada com sucesso!")
            else:
                raise Exception("A query de inserção falhou.")

        except Exception as e:
            QMessageBox.critical(
                self, "Erro", f"Falha ao adicionar reserva no banco de dados.\n\nErro: {e}")

    def delete_reservation(self):
        """Remove uma reserva e atualiza as tabelas de reservas e quartos."""
        selected = self.bookTable.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Aviso", "Selecione uma reserva")
            return

        guest_name = self.bookTable.item(selected, 0).text()
        room_number = self.bookTable.item(selected, 1).text()
        # Pega a data no formato da tabela (DD/MM/AAAA)
        check_in_str = self.bookTable.item(selected, 2).text()

        reply = QMessageBox.question(self, "Confirmar",
                                     f"Tem certeza que deseja remover a reserva do quarto {
                                         room_number} para {guest_name}?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                # Primeiro obtemos o CPF do hóspede
                result = self.execute_query("SELECT cpfHospede FROM hospede WHERE nomeHospede = %s LIMIT 1",
                                            (guest_name,), fetch=True)

                if not result:
                    QMessageBox.critical(
                        self, "Erro", "CPF do hóspede não encontrado.")
                    return

                cpf = result[0][0]

                # CORREÇÃO DA DATA: Converte a data para o formato do banco
                check_in_obj = datetime.strptime(check_in_str, "%d/%m/%Y")
                check_in_db = check_in_obj.strftime("%Y-%m-%d")

                # Executa a query de exclusão com a data no formato correto
                success = self.execute_query("""
                    DELETE FROM reserva 
                    WHERE fk_hospede_cpfHospede = %s 
                    AND fk_quarto_numQuarto = %s 
                    AND dtEntrada = %s
                    """, (cpf, int(room_number), check_in_db))

                if success:
                    QMessageBox.information(self, "Sucesso",
                                            f"Reserva removida. O quarto {room_number} foi marcado como sujo.")
                    self.load_reservations()
                    self.load_rooms()
                else:
                    raise Exception("A query de exclusão falhou.")

            except Exception as e:
                QMessageBox.critical(
                    self, "Erro", f"Falha ao remover reserva no banco de dados.\n\nErro: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HotelReservationSystem()
    window.show()
    sys.exit(app.exec_())
