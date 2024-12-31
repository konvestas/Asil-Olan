from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QStackedWidget
from PySide6.QtCore import Qt


class SignupPage(QWidget):
    def __init__(self, pages: QStackedWidget):
        super().__init__()
        self.pages = pages

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Create an account")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel('Already have an account? <a href="#">Log in</a>')
        subtitle.setStyleSheet("font-size: 14px; color: gray;")
        subtitle.linkActivated.connect(self.go_loginPage)
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

        # password 2 input
        self.password_confirm_input = QLineEdit(self)
        self.password_confirm_input.setEchoMode(QLineEdit.Password)
        self.password_confirm_input.setPlaceholderText("Confirm Password")
        self.password_confirm_input.setFixedWidth(300)
        self.password_confirm_input.setFixedHeight(40)
        self.password_confirm_input.setStyleSheet("font-size: 16px;"
                                                  "padding: 5px;"
                                                  "border-radius: 5px;")
        layout.addWidget(self.password_confirm_input)

        # Error message
        self.error_label = QLabel("", self)
        self.error_label.setStyleSheet("color: red; font-size: 14px;")
        layout.addWidget(self.error_label)

        # Signup button
        signup_button = QPushButton("Sign Up", self)
        signup_button.clicked.connect(self.do_signup)
        signup_button.setFixedWidth(300)
        signup_button.setFixedHeight(40)
        signup_button.setStyleSheet("background-color: #6c63ff;"
                                    "color: white;"
                                    " font-size: 14px;"
                                    " border-radius: 5px;")
        layout.addWidget(signup_button)

        self.setLayout(layout)


    def go_loginPage(self):
        self.pages.setCurrentIndex(1)

    def do_signup(self):
        username = self.username_input.text()
        password = self.password_input.text()
        password_confirm = self.password_confirm_input.text()

        if not username or not password or not password_confirm:
            self.error_label.setText("Enter all the fields")
            return

        if password != password_confirm:
            self.error_label.setText("Passwords don't match")
            return

        if check_signup(username, password):
            self.pages.setCurrentIndex(1)
        else:
            self.error_label.setText("Username exists Try again.")


def check_signup(username, password):
    import json

    users = []
    try:
        with open("users.json", "r", encoding="utf-8") as file:
            users = json.load(file)
    except FileNotFoundError:
        print(f"users.json does not exist yet. Creating a new file.")
    except json.JSONDecodeError:
        print(f"Error: users.json is empty or corrupted. Creating a new file.")

    for user in users:
        if username == user["username"]:
            print(f"Username '{username}' already exists.")
            return False

    new_user = {
        "username": username,
        "password": password,
        "type": "student",  # Default user type
        "image": ""  # Default empty image
    }
    users.append(new_user)

    try:
        with open("users.json", "w", encoding="utf-8") as file:
            json.dump(users, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving user data: {e}")
        return False
    return True