from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QListWidget, QMenuBar, QScrollArea, QStackedWidget, QFormLayout, QMessageBox,
    QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction
import sys
from viewmodel.ReceptionViewModel import ReceptionViewModel


class ReceptionWindow(QMainWindow):
    def __init__(self, receptionist_id):
        super().__init__()
        self.receptionist_id = receptionist_id
        self.view_model = ReceptionViewModel(self.receptionist_id)
        self.setWindowTitle("Patient Management Interface")
        self.setGeometry(100, 100, 1200, 800)

        screen_geometry = self.screen().availableGeometry()
        min_width = int(screen_geometry.width() * 0.9)
        min_height = int(screen_geometry.height() * 0.2)
        self.setMinimumWidth(min_width)
        self.setMinimumHeight(min_height)

        QTimer.singleShot(0, self.center_window)

        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(self.close)

        edit_menu = menu_bar.addMenu("Edit")
        settings_action = QAction("Settings", self)
        edit_menu.addAction(settings_action)

        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        self.sidebar_options = ["Patients", "Dashboard", "Appointments", "Settings"]

        self.sidebar_widget = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_widget.setLayout(self.sidebar_layout)
        self.sidebar_widget.setFixedWidth(200)
        main_layout.addWidget(self.sidebar_widget)

        self.toggle_button = QPushButton("<")
        self.toggle_button.setFixedWidth(30)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.sidebar_layout.addWidget(self.toggle_button, alignment=Qt.AlignLeft)

        self.sidebar_options_stack = QStackedWidget()
        self.sidebar_layout.addWidget(self.sidebar_options_stack)

        self.full_sidebar_widget = QListWidget()
        self.full_sidebar_widget.addItems(self.get_sidebar_options())
        self.full_sidebar_widget.currentRowChanged.connect(self.switch_content_area)
        self.sidebar_options_stack.addWidget(self.full_sidebar_widget)

        collapsed_sidebar_widget = QListWidget()
        collapsed_options = [option[0] for option in self.get_sidebar_options()]
        collapsed_sidebar_widget.addItems(collapsed_options)
        self.sidebar_options_stack.addWidget(collapsed_sidebar_widget)

        parent_area = QVBoxLayout()
        parent_area.setObjectName("parentArea")
        parent_widget = QWidget()
        parent_widget.setLayout(parent_area)
        parent_widget.setObjectName("parentWidget")
        main_layout.addWidget(parent_widget)

        status_area = QHBoxLayout()
        parent_area.addLayout(status_area)

        back_button = QPushButton("< Back")
        back_button.setObjectName("backButton")
        back_button.clicked.connect(self.go_back)
        status_area.addWidget(back_button, alignment=Qt.AlignLeft)

        search_user_layout = QHBoxLayout()
        search_user_layout.addStretch()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search patients...")
        self.search_bar.setObjectName("searchBar")
        self.search_bar.setFixedWidth(350)
        self.search_bar.textChanged.connect(self.filter_table)
        search_user_layout.addWidget(self.search_bar, alignment=Qt.AlignRight)

        user_name = self.view_model.get_receptionist_name()
        user_label = QLabel(user_name)
        user_label.setObjectName("userLabel")
        search_user_layout.addWidget(user_label, alignment=Qt.AlignRight)
        status_area.addLayout(search_user_layout)

        self.content_area_stack = QStackedWidget()
        parent_area.addWidget(self.content_area_stack)

        self.patient_widget = self.create_patient_widget()
        self.content_area_stack.addWidget(self.patient_widget)

        dashboard_widget = QLabel("Dashboard Content")
        self.content_area_stack.addWidget(dashboard_widget)

        appointments_widget = QLabel("Appointments Content")
        self.content_area_stack.addWidget(appointments_widget)

        settings_widget = QLabel("Settings Content")
        self.content_area_stack.addWidget(settings_widget)

        self.add_patient_widget = self.create_add_patient_widget()
        self.content_area_stack.addWidget(self.add_patient_widget)

        self.full_sidebar_widget.setCurrentRow(0)
        self.content_area_stack.setCurrentIndex(0)

    def get_sidebar_options(self):
        return self.sidebar_options

    def toggle_sidebar(self):
        current_index = self.sidebar_options_stack.currentIndex()
        new_index, new_width, button_text = self.toggle_sidebar_logic(current_index)
        self.sidebar_options_stack.setCurrentIndex(new_index)
        self.sidebar_widget.setFixedWidth(new_width)
        self.toggle_button.setText(button_text)

    def toggle_sidebar_logic(self, current_index):
        if current_index == 0:
            return 1, 60, ">"
        else:
            return 0, 200, "<"

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def switch_content_area(self, index):
        self.content_area_stack.setCurrentIndex(index)

    def create_patient_widget(self):
        patient_widget = QWidget()
        patient_layout = QHBoxLayout(patient_widget)

        patient_scroll_area = QScrollArea()
        patient_scroll_area.setWidgetResizable(True)
        patient_scroll_widget = QWidget()
        patient_table_layout = QVBoxLayout(patient_scroll_widget)
        patient_scroll_area.setWidget(patient_scroll_widget)

        self.patient_table = QTableWidget(0, 5)
        self.patient_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.patient_table.setHorizontalHeaderLabels(["Nom", "Prénom", "Âge", "Téléphone", "Genre"])
        self.patient_table.setObjectName("patientTable")

        self.patient_table.setShowGrid(False)
        self.patient_table.setAlternatingRowColors(True)

        self.load_patient_data()

        self.patient_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.patient_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        patient_table_layout.addWidget(self.patient_table)

        self.no_result_label = QLabel("Aucun résultat correspondant")
        self.no_result_label.setAlignment(Qt.AlignCenter)
        self.no_result_label.setObjectName("noResultLabel")
        self.no_result_label.setVisible(False)
        patient_table_layout.addWidget(self.no_result_label)

        patient_layout.addWidget(patient_scroll_area)

        right_sidebar_layout = QVBoxLayout()
        right_sidebar_layout.setAlignment(Qt.AlignTop)
        functionality_label = QLabel("""FUNCTIONALITY:

* RECEPTIONIST
  - RECORDS
    - Create patient record

* DOCTOR
  - EXAMINATION
    - Create examination

* CASHIER
  - BILLING

INTERFACES
- Add""")
        functionality_label.setObjectName("functionalityLabel")
        right_sidebar_layout.addWidget(functionality_label)

        right_sidebar_widget = QWidget()
        right_sidebar_widget.setLayout(right_sidebar_layout)
        right_sidebar_widget.setObjectName("rightSidebarWidget")
        right_sidebar_widget.setFixedWidth(200)

        patient_layout.addWidget(right_sidebar_widget)

        add_patient_button = QPushButton("Add Patient")
        add_patient_button.setObjectName("addPatientButton")
        add_patient_button.setFixedWidth(150)
        add_patient_button.clicked.connect(self.show_add_patient_form)
        patient_table_layout.addWidget(add_patient_button, alignment=Qt.AlignRight)

        return patient_widget

    def create_add_patient_widget(self):
        add_patient_widget = QWidget()
        layout = QFormLayout()

        self.add_patient_nom = QLineEdit()
        self.add_patient_prenom = QLineEdit()
        self.add_patient_age = QLineEdit()
        self.add_patient_telephone = QLineEdit()
        self.add_patient_telephone2 = QLineEdit()
        self.add_patient_email = QLineEdit()
        self.add_patient_address = QLineEdit()
        self.add_patient_genre = QComboBox()
        self.add_patient_genre.addItems(["Masculin", "Féminin"])

        layout.addRow("Nom:", self.add_patient_nom)
        layout.addRow("Prénom:", self.add_patient_prenom)
        layout.addRow("Âge:", self.add_patient_age)
        layout.addRow("Téléphone:", self.add_patient_telephone)
        layout.addRow("Téléphone 2:", self.add_patient_telephone2)
        layout.addRow("Email:", self.add_patient_email)
        layout.addRow("Adresse:", self.add_patient_address)
        layout.addRow("Genre:", self.add_patient_genre)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_new_patient)
        layout.addWidget(save_button)

        add_patient_widget.setLayout(layout)
        return add_patient_widget

    def show_add_patient_form(self):
        self.content_area_stack.setCurrentWidget(self.add_patient_widget)

    def go_back(self):
        self.content_area_stack.setCurrentIndex(0)

    def filter_table(self):
        filter_text = self.search_bar.text().lower()
        found = False
        for row in range(self.patient_table.rowCount()):
            match = False
            for column in range(self.patient_table.columnCount()):
                item = self.patient_table.item(row, column)
                if item and filter_text in item.text().lower():
                    match = True
                    break
            self.patient_table.setRowHidden(row, not match)
            if match:
                found = True

        self.patient_table.setVisible(found)
        self.no_result_label.setVisible(not found)

    def save_new_patient(self):
        nom = self.add_patient_nom.text().strip()
        prenom = self.add_patient_prenom.text().strip()
        age_text = self.add_patient_age.text().strip()
        telephone = self.add_patient_telephone.text().strip()
        telephone2 = self.add_patient_telephone2.text().strip()
        email = self.add_patient_email.text().strip()
        address = self.add_patient_address.text().strip()
        genre = self.add_patient_genre.currentText().strip()

        if not nom or not prenom or not age_text or not telephone or not genre:
            QMessageBox.warning(self, "Validation", "Veuillez remplir tous les champs obligatoires.")
            return

        try:
            age = int(age_text)
            if age < 0 or age > 120:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Validation", "Veuillez entrer un âge valide.")
            return

        if genre not in ['Masculin', 'Féminin']:
            QMessageBox.warning(self, "Validation", "Le genre doit être 'Masculin' ou 'Féminin'.")
            return

        success = self.view_model.add_patient(nom, prenom, age, telephone, telephone2, email, address, genre)
        if success:
            QMessageBox.information(self, "Succès", "Patient ajouté avec succès.")
            self.load_patient_data()
            self.content_area_stack.setCurrentIndex(0)
            self.add_patient_nom.clear()
            self.add_patient_prenom.clear()
            self.add_patient_age.clear()
            self.add_patient_telephone.clear()
            self.add_patient_telephone2.clear()
            self.add_patient_email.clear()
            self.add_patient_address.clear()
            self.add_patient_genre.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Erreur", "Échec de l'ajout du patient. Veuillez réessayer.")

    def load_patient_data(self):
        self.patient_data = self.view_model.prepare_patient_data()
        self.patient_table.setRowCount(0)

        for row_idx, row_data in enumerate(self.patient_data):
            self.patient_table.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                background = self.view_model.get_patient_table_background(row_idx)
                if background:
                    item.setBackground(background)
                self.patient_table.setItem(row_idx, col_idx, item)

    def closeEvent(self, event):
        self.view_model.disconnect_database()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    receptionist_id = 419
    window = ReceptionWindow(receptionist_id)
    window.setObjectName("mainWindow")
    window.show()
    try:
        with open("../styles/style.qss", "r") as style_file:
            app.setStyleSheet(style_file.read())
    except FileNotFoundError:
        pass
    sys.exit(app.exec())
