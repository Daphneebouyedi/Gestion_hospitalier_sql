from PySide6.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QListWidget, QMenuBar, QScrollArea, QStackedWidget,
    QFormLayout, QMessageBox, QCheckBox, QApplication
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QColor
from viewmodel.ComptableViewModel import ComptableViewModel
import sys
import os
import webbrowser

class ComptableWindow(QMainWindow):
    def __init__(self, comptable_id):
        super().__init__()
        self.comptable_id = comptable_id
        self.view_model = ComptableViewModel(self.comptable_id)
        self.setWindowTitle("Gestion des Facturations")
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

        self.sidebar_options = ["Factures Non Payées", "Factures Payées"]

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
        self.full_sidebar_widget.currentRowChanged.connect(self.switch_facture_view)
        self.sidebar_options_stack.addWidget(self.full_sidebar_widget)

        collapsed_sidebar_widget = QListWidget()
        collapsed_options = [option for option in self.get_sidebar_options()]
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
        self.search_bar.setPlaceholderText("Search factures...")
        self.search_bar.setObjectName("searchBar")
        self.search_bar.setFixedWidth(350)
        self.search_bar.textChanged.connect(self.filter_table)
        search_user_layout.addWidget(self.search_bar, alignment=Qt.AlignRight)

        user_name = self.view_model.get_comptable_name()
        user_label = QLabel(user_name)
        user_label.setObjectName("userLabel")
        search_user_layout.addWidget(user_label, alignment=Qt.AlignRight)
        status_area.addLayout(search_user_layout)

        self.content_area_stack = QStackedWidget()
        parent_area.addWidget(self.content_area_stack)

        self.factures_non_payees_widget = self.create_factures_widget(paye=False)
        self.content_area_stack.addWidget(self.factures_non_payees_widget)

        self.factures_payees_widget = self.create_factures_widget(paye=True)
        self.content_area_stack.addWidget(self.factures_payees_widget)

        self.full_sidebar_widget.setCurrentRow(0)
        self.content_area_stack.setCurrentIndex(0)

        self.view_model.facture_retrieved.connect(self.populate_facture_table)
        self.view_model.facture_details_retrieved.connect(self.display_facture_details)
        self.view_model.facture_updated.connect(self.on_facture_updated)

        self.view_model.get_factures(est_paye=False)

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

    def switch_facture_view(self, index):
        if index == 0:
            self.content_area_stack.setCurrentWidget(self.factures_non_payees_widget)
            self.view_model.get_factures(est_paye=False)
        elif index == 1:
            self.content_area_stack.setCurrentWidget(self.factures_payees_widget)
            self.view_model.get_factures(est_paye=True)

    def create_factures_widget(self, paye=False):
        facture_widget = QWidget()
        facture_layout = QVBoxLayout(facture_widget)

        facture_table = QTableWidget(0, 6)
        facture_table.setSelectionBehavior(QTableWidget.SelectRows)
        facture_table.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Montant (€)", "Date Emission", "Date Paiement"])
        facture_table.setObjectName("factureTable")

        facture_table.cellClicked.connect(self.on_facture_clicked)
        facture_table.cellDoubleClicked.connect(self.on_facture_double_clicked)

        facture_table.setShowGrid(False)
        facture_table.setAlternatingRowColors(True)

        facture_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        facture_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        facture_layout.addWidget(facture_table)

        no_result_label = QLabel("Aucun résultat correspondant")
        no_result_label.setAlignment(Qt.AlignCenter)
        no_result_label.setObjectName("noResultLabel")
        no_result_label.setVisible(False)
        facture_layout.addWidget(no_result_label)

        facture_widget.facture_table = facture_table
        facture_widget.no_result_label = no_result_label

        return facture_widget

    def populate_facture_table(self, est_paye, factures):
        if est_paye:
            current_widget = self.factures_payees_widget
        else:
            current_widget = self.factures_non_payees_widget

        facture_table = current_widget.facture_table
        no_result_label = current_widget.no_result_label

        facture_table.setRowCount(0)

        for row_idx, facture in enumerate(factures):
            facture_table.insertRow(row_idx)
            facture_table.setItem(row_idx, 0, QTableWidgetItem(str(facture['id_Facturation'])))
            facture_table.setItem(row_idx, 1, QTableWidgetItem(facture['nom']))
            facture_table.setItem(row_idx, 2, QTableWidgetItem(facture['prenom']))
            facture_table.setItem(row_idx, 3, QTableWidgetItem(f"{facture['montant']:.2f}"))
            facture_table.setItem(row_idx, 4, QTableWidgetItem(facture['date_emission']))
            facture_table.setItem(row_idx, 5, QTableWidgetItem(facture['date_Paiement']))

            if row_idx % 2 == 0:
                for col in range(facture_table.columnCount()):
                    facture_table.item(row_idx, col).setBackground(QColor(240, 240, 240))

        if factures:
            facture_table.setVisible(True)
            no_result_label.setVisible(False)
        else:
            facture_table.setVisible(False)
            no_result_label.setVisible(True)

    def create_facture_details_widget(self, details):
        details_widget = QWidget()
        details_layout = QFormLayout()
        details_widget.setLayout(details_layout)

        id_facture_label = QLabel(str(details.get('id_Facturation', '')))
        nom_label = QLabel(details.get('nom', ''))
        prenom_label = QLabel(details.get('prenom', ''))
        montant_label = QLabel(f"{details.get('montant', 0):.2f} €")
        date_emission_label = QLabel(details.get('date_emission', ''))
        date_paiement_label = QLabel(details.get('date_Paiement', ''))
        acteur_label = QLabel(details.get('acteur', ''))
        telephone_acteur_label = QLabel(details.get('telephone_Acteur', ''))
        description_label = QLabel(details.get('description', ''))

        self.checkbox_paye = QCheckBox("Facture Payée")
        self.checkbox_paye.setChecked(details.get('est_Payee', False))
        self.checkbox_paye.stateChanged.connect(lambda state: self.on_checkbox_changed(details.get('id_Facturation'), state))

        details_layout.addRow("ID Facturation :", id_facture_label)
        details_layout.addRow("Nom :", nom_label)
        details_layout.addRow("Prénom :", prenom_label)
        details_layout.addRow("Montant :", montant_label)
        details_layout.addRow("Date Emission :", date_emission_label)
        details_layout.addRow("Date Paiement :", date_paiement_label)
        details_layout.addRow("Acteur :", acteur_label)
        details_layout.addRow("Téléphone Acteur :", telephone_acteur_label)
        details_layout.addRow("Description :", description_label)
        details_layout.addRow("", self.checkbox_paye)

        if not hasattr(self, 'details_layout'):
            self.details_layout = QVBoxLayout()
            self.details_widget_container = QWidget()
            self.details_widget_container.setLayout(self.details_layout)
            self.details_layout.setAlignment(Qt.AlignTop)
            parent_area = self.findChild(QVBoxLayout, "parentArea")
            if parent_area:
                parent_area.addWidget(self.details_widget_container)
            self.details_layout.addWidget(details_widget)
        else:
            while self.details_layout.count():
                child = self.details_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            self.details_layout.addWidget(details_widget)

    def on_facture_clicked(self, row, column):
        facture_table = self.sender()
        facture_id_item = facture_table.item(row, 0)
        if facture_id_item:
            facture_id = int(facture_id_item.text())
            self.view_model.get_facture_details(facture_id)

    def on_facture_double_clicked(self, row, column):
        facture_table = self.sender()
        facture_id_item = facture_table.item(row, 0)
        if facture_id_item:
            facture_id = int(facture_id_item.text())
            pdf_path = self.view_model.get_facture_pdf(facture_id)
            if os.path.exists(pdf_path):
                webbrowser.open(f"file://{os.path.abspath(pdf_path)}")
            else:
                QMessageBox.warning(self, "Erreur", "Le fichier PDF de la facture est introuvable.")

    def filter_table(self):
        filter_text = self.search_bar.text().lower()
        current_widget = self.content_area_stack.currentWidget()
        facture_table = current_widget.facture_table
        no_result_label = current_widget.no_result_label
        found = False
        for row in range(facture_table.rowCount()):
            match = False
            for column in range(facture_table.columnCount()):
                item = facture_table.item(row, column)
                if filter_text in item.text().lower():
                    match = True
                    break
            facture_table.setRowHidden(row, not match)
            if match:
                found = True

        facture_table.setVisible(found)
        no_result_label.setVisible(not found)

    def on_facture_details_retrieved(self, details):
        if details:
            self.create_facture_details_widget(details)
        else:
            QMessageBox.warning(self, "Détails Facture", "Détails de la facture introuvables.")

    def on_facture_updated(self, success):
        if success:
            QMessageBox.information(self, "Succès", "Statut de la facture mis à jour avec succès.")
            current_widget = self.content_area_stack.currentWidget()
            if current_widget == self.factures_payees_widget:
                paye = True
            else:
                paye = False
            self.view_model.get_factures(est_paye=paye)
        else:
            QMessageBox.critical(self, "Erreur", "Échec de la mise à jour du statut de la facture.")

    def display_facture_details(self, details):
        self.on_facture_details_retrieved(details)

    def on_checkbox_changed(self, facture_id, state):
        est_paye = (state == Qt.Checked)
        self.view_model.update_facture_status(facture_id, est_paye)

    def go_back(self):
        pass

    def show_context_menu(self, position):
        pass

    def closeEvent(self, event):
        self.view_model.disconnect_database()
        event.accept()

    def on_login_success(self, role, specific_id):
        pass

    def on_login_failure(self, message):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    comptable_id = 123
    window = ComptableWindow(comptable_id)
    window.setObjectName("mainWindow")
    window.show()
    try:
        with open("../styles/style.qss", "r") as style_file:
            app.setStyleSheet(style_file.read())
    except FileNotFoundError:
        pass
    sys.exit(app.exec())
