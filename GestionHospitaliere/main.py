
from PySide6.QtWidgets import QApplication
import sys
from views.windows.LoginWidow import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("views/styles/style.qss", "r") as style_file:
            qss = style_file.read()
            app.setStyleSheet(qss)
    except FileNotFoundError:
        print("QSS file not found. The application will open without custom styles.")

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())
