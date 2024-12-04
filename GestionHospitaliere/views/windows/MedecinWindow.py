from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QListWidget, QMenuBar, QScrollArea, QStackedWidget, QFormLayout, QMessageBox,
    QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction
import sys
from viewmodel.MedecinViewModel import MedecinViewModel


class MedecinWindow(QMainWindow):
    def __init__(self, medecin_id):
        super().__init__()
        self.medecin_id = medecin_id
        self.view_model = MedecinViewModel(self.medecin_id)
        self.setWindowTitle("Interface Médecin")
        self.setGeometry(100, 100, 1200, 800)

        screen_geometry = self.screen().availableGeometry()
        min_width = int(screen_geometry.width() * 0.9)
        min_height = int(screen_geometry.height() * 0.2)
        self.setMinimumWidth(min_width)
        self.setMinimumHeight(min_height)

        QTimer.singleShot(0, self.center_window)

        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        file_menu = menu_bar.addMenu("Fichier")
        exit_action = QAction("Quitter", self)
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(self.close)

        edit_menu = menu_bar.addMenu("Éditer")
        settings_action = QAction("Paramètres", self)
        edit_menu.addAction(settings_action)

        help_menu = menu_bar.addMenu("Aide")
        about_action = QAction("À propos", self)
        help_menu.addAction(about_action)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        self.sidebar_options = ["Dossiers", "Tableau de bord", "Rendez-vous", "Paramètres"]

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

        back_button = QPushButton("< Retour")
        back_button.setObjectName("backButton")
        back_button.clicked.connect(self.go_back)
        status_area.addWidget(back_button, alignment=Qt.AlignLeft)

        search_user_layout = QHBoxLayout()
        search_user_layout.addStretch()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher des dossiers...")
        self.search_bar.setObjectName("searchBar")
        self.search_bar.setFixedWidth(350)
        self.search_bar.textChanged.connect(self.filter_table)
        search_user_layout.addWidget(self.search_bar, alignment=Qt.AlignRight)

        user_name = self.view_model.get_medecin_name()
        user_label = QLabel(user_name)
        user_label.setObjectName("userLabel")
        search_user_layout.addWidget(user_label, alignment=Qt.AlignRight)
        status_area.addLayout(search_user_layout)

        self.content_area_stack = QStackedWidget()
        parent_area.addWidget(self.content_area_stack)

        self.dossier_widget = self.create_dossier_widget()
        self.content_area_stack.addWidget(self.dossier_widget)

        dashboard_widget = QLabel("Contenu du tableau de bord")
        self.content_area_stack.addWidget(dashboard_widget)

        appointments_widget = QLabel("Contenu des rendez-vous")
        self.content_area_stack.addWidget(appointments_widget)

        settings_widget = QLabel("Contenu des paramètres")
        self.content_area_stack.addWidget(settings_widget)

        self.feuilles_table_widget = self.create_feuilles_table_widget()
        self.content_area_stack.addWidget(self.feuilles_table_widget)

        self.add_feuille_widget = self.create_add_feuille_widget()
        self.content_area_stack.addWidget(self.add_feuille_widget)

        self.feuille_details_widget = self.create_feuille_details_widget()
        self.content_area_stack.addWidget(self.feuille_details_widget)

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

    def create_dossier_widget(self):
        dossier_widget = QWidget()
        dossier_layout = QHBoxLayout(dossier_widget)

        dossier_scroll_area = QScrollArea()
        dossier_scroll_area.setWidgetResizable(True)
        dossier_scroll_widget = QWidget()
        dossier_table_layout = QVBoxLayout(dossier_scroll_widget)
        dossier_scroll_area.setWidget(dossier_scroll_widget)

        self.dossier_table = QTableWidget(0, 7)
        self.dossier_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.dossier_table.setHorizontalHeaderLabels(["ID Dossier", "Nom Patient", "Prénom Patient", "Groupe Sanguin", "Statut Rhésus", "Observation", "Date Ouverture"])
        self.dossier_table.setObjectName("dossierTable")

        self.dossier_table.setColumnHidden(0, True)

        self.dossier_table.cellClicked.connect(self.on_dossier_table_cell_clicked)
        self.dossier_table.cellDoubleClicked.connect(self.on_dossier_table_cell_double_clicked)

        self.dossier_table.setShowGrid(False)
        self.dossier_table.setAlternatingRowColors(True)

        self.load_dossier_data()

        self.dossier_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dossier_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        dossier_table_layout.addWidget(self.dossier_table)

        self.no_result_label = QLabel("Aucun résultat correspondant")
        self.no_result_label.setAlignment(Qt.AlignCenter)
        self.no_result_label.setObjectName("noResultLabel")
        self.no_result_label.setVisible(False)
        dossier_table_layout.addWidget(self.no_result_label)

        dossier_layout.addWidget(dossier_scroll_area)

        right_sidebar_layout = QVBoxLayout()
        right_sidebar_layout.setAlignment(Qt.AlignTop)

        self.functionality_label = QLabel("Sélectionnez un dossier pour afficher les informations")
        self.functionality_label.setObjectName("functionalityLabel")
        right_sidebar_layout.addWidget(self.functionality_label)

        right_sidebar_widget = QWidget()
        right_sidebar_widget.setLayout(right_sidebar_layout)
        right_sidebar_widget.setObjectName("rightSidebarWidget")
        right_sidebar_widget.setFixedWidth(200)

        dossier_layout.addWidget(right_sidebar_widget)

        return dossier_widget

    def on_dossier_table_cell_clicked(self, row, column):
        id_dossier_item = self.dossier_table.item(row, 0)
        if id_dossier_item is not None:
            id_dossier = int(id_dossier_item.text())
            self.update_dossier_sidebar(id_dossier)

    def on_dossier_table_cell_double_clicked(self, row, column):
        id_dossier_item = self.dossier_table.item(row, 0)
        if id_dossier_item is not None:
            id_dossier = int(id_dossier_item.text())
            self.show_feuilles_table(id_dossier)

    def update_dossier_sidebar(self, dossier_id):
        dossier_info = self.view_model.get_dossier_info(dossier_id)
        if dossier_info:
            nom = dossier_info['nom_Patient']
            prenom = dossier_info['prenom_Patient']
            age = self.view_model.calculate_age(dossier_info['date_naissance'])
            date_ouverture = dossier_info['date_Ouverture']
            heure_ouverture = date_ouverture.strftime('%H:%M:%S')
            date_ouverture_str = date_ouverture.strftime('%d/%m/%Y')
            receptionniste_nom = dossier_info['nom_Receptionniste']
            receptionniste_prenom = dossier_info['prenom_Receptionniste']

            info_text = f"""Nom Prénom: {prenom} {nom}
Âge: {age}
Date: {date_ouverture_str}
Heure: {heure_ouverture}
Réceptionniste: {receptionniste_prenom} {receptionniste_nom}"""
        else:
            info_text = "Informations du dossier non disponibles."

        self.functionality_label.setText(info_text)

    def load_dossier_data(self):
        self.dossier_data = self.view_model.get_all_dossiers()
        self.dossier_table.setRowCount(0)

        for row_idx, row_data in enumerate(self.dossier_data):
            self.dossier_table.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                background = self.view_model.get_dossier_table_background(row_idx)
                if background:
                    item.setBackground(background)
                self.dossier_table.setItem(row_idx, col_idx, item)

    def create_feuilles_table_widget(self):
        feuilles_widget = QWidget()
        feuilles_layout = QHBoxLayout(feuilles_widget)

        feuilles_scroll_area = QScrollArea()
        feuilles_scroll_area.setWidgetResizable(True)
        feuilles_scroll_widget = QWidget()
        feuilles_table_layout = QVBoxLayout(feuilles_scroll_widget)
        feuilles_scroll_area.setWidget(feuilles_scroll_widget)

        self.feuilles_table = QTableWidget(0, 6)
        self.feuilles_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.feuilles_table.setHorizontalHeaderLabels(["ID Feuille", "Date Début", "Date Fin", "Poids", "Taille", "Pathologie"])
        self.feuilles_table.setObjectName("feuillesTable")

        self.feuilles_table.setColumnHidden(0, True)

        self.feuilles_table.cellClicked.connect(self.on_feuilles_table_cell_clicked)

        self.feuilles_table.setShowGrid(False)
        self.feuilles_table.setAlternatingRowColors(True)

        self.feuilles_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.feuilles_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        feuilles_table_layout.addWidget(self.feuilles_table)

        add_feuille_button = QPushButton("Ajouter un examen")
        add_feuille_button.setObjectName("addFeuilleButton")
        add_feuille_button.setFixedWidth(150)
        add_feuille_button.clicked.connect(self.show_add_feuille_form)
        feuilles_table_layout.addWidget(add_feuille_button, alignment=Qt.AlignRight)

        feuilles_layout.addWidget(feuilles_scroll_area)

        right_sidebar_layout = QVBoxLayout()
        right_sidebar_layout.setAlignment(Qt.AlignTop)

        self.feuilles_functionality_label = QLabel()
        self.feuilles_functionality_label.setObjectName("functionalityLabel")
        right_sidebar_layout.addWidget(self.feuilles_functionality_label)

        right_sidebar_widget = QWidget()
        right_sidebar_widget.setLayout(right_sidebar_layout)
        right_sidebar_widget.setObjectName("rightSidebarWidget")
        right_sidebar_widget.setFixedWidth(200)

        feuilles_layout.addWidget(right_sidebar_widget)

        return feuilles_widget

    def show_feuilles_table(self, dossier_id):
        self.current_dossier_id = dossier_id
        self.load_feuilles_data(dossier_id)
        dossier_info = self.view_model.get_dossier_info(dossier_id)
        if dossier_info:
            nom = dossier_info['nom_Patient']
            prenom = dossier_info['prenom_Patient']
            age = self.view_model.calculate_age(dossier_info['date_naissance'])
            date_ouverture = dossier_info['date_Ouverture']
            heure_ouverture = date_ouverture.strftime('%H:%M:%S')
            date_ouverture_str = date_ouverture.strftime('%d/%m/%Y')
            receptionniste_nom = dossier_info['nom_Receptionniste']
            receptionniste_prenom = dossier_info['prenom_Receptionniste']

            info_text = f"""Nom Prénom: {prenom} {nom}
Âge: {age}
Date: {date_ouverture_str}
Heure: {heure_ouverture}
Réceptionniste: {receptionniste_prenom} {receptionniste_nom}"""
        else:
            info_text = "Informations du dossier non disponibles."

        self.feuilles_functionality_label.setText(info_text)
        self.content_area_stack.setCurrentWidget(self.feuilles_table_widget)

    def load_feuilles_data(self, dossier_id):
        self.feuilles_data = self.view_model.get_feuilles_by_dossier_id(dossier_id)
        self.feuilles_table.setRowCount(0)

        for row_idx, row_data in enumerate(self.feuilles_data):
            self.feuilles_table.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                background = self.view_model.get_feuilles_table_background(row_idx)
                if background:
                    item.setBackground(background)
                self.feuilles_table.setItem(row_idx, col_idx, item)

    def on_feuilles_table_cell_clicked(self, row, column):
        id_feuille_item = self.feuilles_table.item(row, 0)
        if id_feuille_item is not None:
            id_feuille = int(id_feuille_item.text())
            self.show_feuille_details(id_feuille)

    def show_feuille_details(self, feuille_id):
        self.current_feuille_id = feuille_id
        feuille_data = self.view_model.get_feuille_details(feuille_id)
        if feuille_data:
            self.detail_poids.setText(str(feuille_data['poids']))
            self.detail_taille.setText(str(feuille_data['Taille']))
            self.detail_pathologie.setText(feuille_data['Pathologie'])
            self.detail_date_debut.setText(str(feuille_data['date_Debut']))
            self.detail_date_fin.setText(str(feuille_data['date_Fin']) if feuille_data['date_Fin'] else '')
        self.content_area_stack.setCurrentWidget(self.feuille_details_widget)

    def create_feuille_details_widget(self):
        feuille_details_widget = QWidget()
        layout = QFormLayout()

        self.detail_poids = QLineEdit()
        self.detail_taille = QLineEdit()
        self.detail_pathologie = QLineEdit()
        self.detail_date_debut = QLineEdit()
        self.detail_date_debut.setReadOnly(True)
        self.detail_date_fin = QLineEdit()

        layout.addRow("Poids:", self.detail_poids)
        layout.addRow("Taille:", self.detail_taille)
        layout.addRow("Pathologie:", self.detail_pathologie)
        layout.addRow("Date Début:", self.detail_date_debut)
        layout.addRow("Date Fin:", self.detail_date_fin)

        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(self.save_feuille_details)
        cancel_button = QPushButton("Annuler")
        cancel_button.clicked.connect(self.cancel_feuille_details)
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        layout.addRow(buttons_layout)

        feuille_details_widget.setLayout(layout)
        return feuille_details_widget

    def save_feuille_details(self):
        poids_text = self.detail_poids.text().strip()
        taille = self.detail_taille.text().strip()
        pathologie = self.detail_pathologie.text().strip()
        date_debut_text = self.detail_date_debut.text().strip()
        date_fin_text = self.detail_date_fin.text().strip()

        if not poids_text or not taille or not pathologie:
            QMessageBox.warning(self, "Validation", "Veuillez remplir tous les champs obligatoires.")
            return

        try:
            poids = float(poids_text)
        except ValueError:
            QMessageBox.warning(self, "Validation", "Veuillez entrer un poids valide.")
            return

        feuille_data = {
            'poids': poids,
            'Taille': taille,
            'Pathologie': pathologie,
            'date_Debut': date_debut_text,
            'date_Fin': date_fin_text if date_fin_text else None
        }

        success = self.view_model.update_feuille(self.current_feuille_id, feuille_data)
        if success:
            QMessageBox.information(self, "Succès", "Les détails de la feuille ont été mis à jour avec succès.")
            self.load_feuilles_data(self.current_dossier_id)
            self.content_area_stack.setCurrentWidget(self.feuilles_table_widget)
        else:
            QMessageBox.critical(self, "Erreur", "Échec de la mise à jour de la feuille. Veuillez réessayer.")

    def cancel_feuille_details(self):
        self.content_area_stack.setCurrentWidget(self.feuilles_table_widget)

    def create_add_feuille_widget(self):
        add_feuille_widget = QWidget()
        layout = QFormLayout()

        self.feuille_poids = QLineEdit()
        self.feuille_taille = QLineEdit()
        self.feuille_pathologie = QLineEdit()

        layout.addRow("Poids:", self.feuille_poids)
        layout.addRow("Taille:", self.feuille_taille)
        layout.addRow("Pathologie:", self.feuille_pathologie)

        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(self.save_new_feuille)
        layout.addWidget(save_button)

        add_feuille_widget.setLayout(layout)
        return add_feuille_widget

    def show_add_feuille_form(self):
        self.feuille_poids.clear()
        self.feuille_taille.clear()
        self.feuille_pathologie.clear()
        self.content_area_stack.setCurrentWidget(self.add_feuille_widget)

    def save_new_feuille(self):
        poids_text = self.feuille_poids.text().strip()
        taille = self.feuille_taille.text().strip()
        pathologie = self.feuille_pathologie.text().strip()
        dossier_id = self.current_dossier_id

        if not poids_text or not taille or not pathologie:
            QMessageBox.warning(self, "Validation", "Veuillez remplir tous les champs.")
            return

        try:
            poids = float(poids_text)
        except ValueError:
            QMessageBox.warning(self, "Validation", "Veuillez entrer un poids valide.")
            return

        success = self.view_model.add_feuille(poids, taille, pathologie, dossier_id)
        if success:
            QMessageBox.information(self, "Succès", "Examen ajouté avec succès.")
            self.load_feuilles_data(dossier_id)
            self.content_area_stack.setCurrentWidget(self.feuilles_table_widget)
            self.feuille_poids.clear()
            self.feuille_taille.clear()
            self.feuille_pathologie.clear()
        else:
            QMessageBox.critical(self, "Erreur", "Échec de l'ajout de l'examen. Veuillez réessayer.")

    def filter_table(self):
        filter_text = self.search_bar.text().lower()
        current_widget = self.content_area_stack.currentWidget()
        if current_widget == self.dossier_widget:
            table = self.dossier_table
        elif current_widget == self.feuilles_table_widget:
            table = self.feuilles_table
        else:
            return

        found = False
        for row in range(table.rowCount()):
            match = False
            for column in range(table.columnCount()):
                item = table.item(row, column)
                if item and filter_text in item.text().lower():
                    match = True
                    break
            table.setRowHidden(row, not match)
            if match:
                found = True

        table.setVisible(found)
        self.no_result_label.setVisible(not found)

    def go_back(self):
        current_widget = self.content_area_stack.currentWidget()
        if current_widget == self.feuilles_table_widget:
            self.content_area_stack.setCurrentWidget(self.dossier_widget)
        elif current_widget == self.feuille_details_widget or current_widget == self.add_feuille_widget:
            self.content_area_stack.setCurrentWidget(self.feuilles_table_widget)
        else:
            self.content_area_stack.setCurrentWidget(self.dossier_widget)

    def closeEvent(self, event):
        self.view_model.disconnect_database()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    medecin_id = 1
    window = MedecinWindow(medecin_id)
    window.setObjectName("mainWindow")
    window.show()
    try:
        with open("../styles/style.qss", "r") as style_file:
            app.setStyleSheet(style_file.read())
    except FileNotFoundError:
        pass
    sys.exit(app.exec())
