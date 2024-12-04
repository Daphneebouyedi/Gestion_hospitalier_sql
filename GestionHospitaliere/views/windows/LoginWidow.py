
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy
)
from PySide6.QtCore import QTimer, Qt
from viewmodel.LoginViewModel import LoginViewModel
from views.windows.ReceptionWindow import ReceptionWindow
from views.windows.MedecinWindow import MedecinWindow
from views.windows.ComptableWindow import ComptableWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Window")
        self.setGeometry(500, 200, 600, 400)

        self.load_stylesheet("views/styles/login_style.qss")

        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(central_layout)

        central_layout.addStretch()

        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(50, 0, 50, 0)

        self.connection_label = QLabel("CONNECTION")
        self.connection_label.setAlignment(Qt.AlignCenter)
        self.connection_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        form_layout.addWidget(self.connection_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setMinimumHeight(40)
        self.username_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setMinimumHeight(40)
        self.password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.setMinimumHeight(40)
        self.login_button.clicked.connect(self.on_login_clicked)
        form_layout.addWidget(self.login_button)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.status_label)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        form_widget.setMinimumWidth(400)

        central_layout.addWidget(form_widget, alignment=Qt.AlignHCenter)

        central_layout.addStretch()

        self.view_model = LoginViewModel()
        self.view_model.login_successful.connect(self.on_login_success)
        self.view_model.login_failed.connect(self.on_login_failure)

    def load_stylesheet(self, qss_file):
        try:
            with open(qss_file, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"{qss_file} not found. Stylesheet not applied.")

    def on_login_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.status_label.setText("Veuillez remplir tous les champs.")
            self.status_label.setStyleSheet("color: red;")
            return

        self.status_label.setText("Authentification en cours...")
        self.status_label.setStyleSheet("color: blue;")
        self.view_model.set_credentials(username, password)
        self.view_model.authenticate()

    def on_login_success(self, role, specific_id):
        self.status_label.setText("Connexion réussie !")
        self.status_label.setStyleSheet("color: green;")
        QTimer.singleShot(2000, lambda: self.open_main_app(role, specific_id))

    def on_login_failure(self, message):
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: red;")

    def open_main_app(self, role, specific_id):
        self.close()
        if role == "Medecin":
            self.main_window = MedecinWindow(specific_id)
        elif role == "Receptionniste":
            self.main_window = ReceptionWindow(specific_id)
        elif role == "Comptable":
            self.main_window = ComptableWindow(specific_id)
        else:
            self.status_label.setText("Rôle utilisateur inconnu.")
            self.status_label.setStyleSheet("color: red;")
            return

        self.main_window.show()
