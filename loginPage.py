import csv

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QStackedWidget
from PySide6.QtCore import Qt



class LoginPage(QWidget):
    def __init__(self, pages: QStackedWidget):
        super().__init__()
        self.pages = pages


        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Log to an account")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel('Dont have a account? <a href="#">Sign up</a>')
        subtitle.setStyleSheet("font-size: 14px; color: gray;")
        subtitle.linkActivated.connect(self.go_signupPage)
        layout.addWidget(subtitle)

        # username input
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedWidth(300)
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("font-size: 16px;"
                                          "padding: 5px;"
                                          "border-radius: 5px;")
        layout.addWidget(self.username_input)

        # password input
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedWidth(300)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("font-size: 16px;"
                                          "padding: 5px;"
                                          "border-radius: 5px;")
        layout.addWidget(self.password_input)

        # Error message
        self.error_label = QLabel("", self)
        self.error_label.setStyleSheet("color: red; font-size: 14px;")
        layout.addWidget(self.error_label)

        # Signin button
        signin_button = QPushButton("Sign In", self)
        signin_button.clicked.connect(self.login)
        signin_button.setFixedWidth(300)
        signin_button.setFixedHeight(40)
        signin_button.setStyleSheet("background-color: #6c63ff;"
                                    "color: white;"
                                    " font-size: 14px;"
                                    " border-radius: 5px;")
        layout.addWidget(signin_button)

        self.setLayout(layout)


    def go_signupPage(self):
        self.pages.setCurrentIndex(0)



    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            self.error_label.setText("Enter all the fields")
            return

        if check_login(username, password):
            self.pages.setCurrentIndex(2)

        else:
            self.error_label.setText("Username or password wrong")
            print("Try again")




def check_login(username, password):
        with open("users", "r", encoding='utf-8') as user_file:
            for line in user_file:
                stored_username, stored_password  = line.strip().split(',')
                if username == stored_username and password == stored_password:
                    return True
        return False

