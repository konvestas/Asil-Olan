from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QStackedWidget, QLineEdit, QFileDialog, QSpacerItem,
    QSizePolicy, QScrollArea, QWidget
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QTimer


class ProfilePage(QFrame):
    def __init__(self, pages: QStackedWidget):
        super().__init__()
        self.pages = pages

        self.setStyleSheet("""
                                    QWidget { background-color: #222222; color: #FFFFFF; }
                                    QLineEdit { background-color: #333333;
                                                border: 1px solid #444444;
                                                border-radius: 8px;
                                                padding: 5px;
                                                color: white; }
                                    QLabel { font-size: 14px; }
                                """)

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        from sideMenu import SideMenu
        side_menu = SideMenu(self.pages)
        side_menu.setFixedWidth(150)
        main_layout.addWidget(side_menu)

        # Right content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(10, 10, 10, 0)

        right_content = QFrame()
        right_content.setLayout(content_layout)
        right_content.setStyleSheet("background-color: #222222;")
        main_layout.addWidget(right_content)

        # Profile Label
        top_bar = QHBoxLayout()
        label = QLabel("Profile")
        label.setStyleSheet("font-size: 35px; font-weight: bold; color: white;")
        top_bar.addWidget(label)
        content_layout.addLayout(top_bar)

        # Gap label search bar
        spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        top_bar.addSpacerItem(spacer)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setFixedSize(200, 35)

        icon = QIcon("assets/icons/search_icon.png")
        self.search_bar.addAction(icon, QLineEdit.TrailingPosition)


        # Icon alignment
        self.search_bar.setStyleSheet("""
                                    QLineEdit {
                                        background-color: #333333;
                                        border: 1px solid #444444;
                                        border-radius: 8px;
                                        padding-right: 25px;
                                        color: white;
                                    }
                                """)
        top_bar.addWidget(self.search_bar, alignment=Qt.AlignLeft)
        content_layout.addLayout(top_bar)


        self.box_layout = QHBoxLayout()

        box_left = self.create_userBox()
        self.box_topRight = self.create_downloaded_box("Your downloads", "users.json")
       # self.box_bottomRight = self.create_book_box("Recommended Books", "mostViewed.json")


        right_boxes = QHBoxLayout()
        right_boxes.setSpacing(10)
        right_boxes.addWidget(self.box_topRight)
        #right_boxes.addWidget(self.box_bottomRight)

        self.box_layout.addWidget(box_left)
        self.box_layout.addLayout(right_boxes)
        content_layout.addLayout(self.box_layout)

        self.setLayout(main_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_downloads)
        self.timer.start(5000)

    def refresh_downloads(self):
        self.box_layout.removeWidget(self.box_topRight)
        self.box_topRight.deleteLater()

        self.box_topRight = self.create_downloaded_box("Your downloads", "users.json")
        self.box_topRight.setFixedSize(620, 344)
        self.box_layout.addWidget(self.box_topRight)


    def load_downloaded_books(self, filename):
        import json
        from loginPage import get_saved_user

        user = get_saved_user()
        if not user:
            print("Error: No user information found.")
            return []

        username = user.get("username")
        if not username:
            print("Error: User has no username.")
            return []

        books = []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

                for user_data in data:
                    if user_data.get("username") == username:

                        for book in user_data.get("books", []):
                            books.append({
                                "name": book.get("name", "Unknown").strip(),
                                "book": book.get("book", "Unknown").strip(),
                                "type": book.get("type", "Unknown").strip(),
                                "description": book.get("description", "").strip(),
                                "image": book.get("image", "").strip()
                            })
                        break

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON in file '{filename}'.")
        except Exception as e:
            print(f"An unexpected error occurred while reading '{filename}': {e}")

        return books

    def load_books_json(self, filename):
        import json

        books = []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                for row in data:
                    books.append({
                        "name": row.get("name", "Unknown").strip(),
                        "book": row.get("book", "Unknown").strip(),
                        "type": row.get("type", "Unknown").strip(),
                        "description": row.get("description", "").strip(),
                        "image": row.get("image", "").strip()
                    })
        except Exception as e:
            print(f"Error reading JSON file '{filename}': {e}")

        return books

    def create_userBox(self):
        box = QFrame()
        box.setFixedSize(657, 701)
        box.setStyleSheet("background-color: #333333; border-radius: 8px;")

        # Main layout for the box
        layout = QVBoxLayout(box)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        # Title Section
        title_label = QLabel("Your Details")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        #Profile pic
        self.profile_pic = QLabel()

        self.profile_pic.setFixedSize(200, 150)
        self.profile_pic.setStyleSheet("border: 2px solid #555555;background-color: #444444;border-radius: 7px;")
        self.profile_pic.setAlignment(Qt.AlignCenter)

        pixmap = self.load_user_picture()
        self.profile_pic.setPixmap(pixmap)

        layout.addWidget(self.profile_pic, alignment=Qt.AlignCenter)

        # Change image button
        changePic_button = QPushButton("Change picture")
        changePic_button.setFixedSize(150, 35)
        changePic_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                border: none;
                border-radius: 8px;
                color: #FFFFFF;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #777777;
            }
        """)
        changePic_button.clicked.connect(self.change_profile_picture)
        layout.addWidget(changePic_button, alignment=Qt.AlignCenter)

        # Form Layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        # Username Field
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-size: 14px; color: #FFFFFF;")
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter your username")
        self.username_edit.setFixedSize(200, 30)
        self.username_edit.setStyleSheet(
            "background-color: #444444; border: 1px solid #555555; border-radius: 5px; padding: 5px;")

        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_edit)
        form_layout.addLayout(username_layout)

        # Password Field
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-size: 14px; color: #FFFFFF;")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Enter your password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFixedSize(200, 30)
        self.password_edit.setStyleSheet(
            "background-color: #444444; border: 1px solid #555555; border-radius: 5px; padding: 5px;")

        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_edit)
        form_layout.addLayout(password_layout)

        layout.addLayout(form_layout)

        # Save Changes button
        save_button = QPushButton("Save Changes")
        save_button.setFixedSize(150, 35)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                border: none;
                border-radius: 8px;
                color: #FFFFFF;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #777777;
            }
        """)
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button, alignment=Qt.AlignCenter)

        return box

    def create_book_box(self, own_label, file_name):
        box = QFrame()
        box.setFixedSize(620, 344)
        box.setStyleSheet("background-color: #333333; border-radius: 8px;")

        layout = QVBoxLayout(box)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        top_layout = QHBoxLayout()

        title_label = QLabel(own_label)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        top_layout.addWidget(title_label)
        layout.addLayout(top_layout)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea { background-color: transparent; }
            QScrollBar:vertical { border: none; background: white; width: 10px;  }
            QScrollBar::handle:vertical { background: #666666; border-radius: 5px; }
            QScrollBar::handle:vertical:hover { background: #888888; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(10)

        books = self.load_books_json(file_name)
        for book in books:
            scroll_layout.addWidget(self.create_book_row(book))

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        return box

    def create_downloaded_box(self, own_label, file_name):
        box = QFrame()
        box.setFixedSize(620, 344)
        box.setStyleSheet("background-color: #333333; border-radius: 8px;")

        layout = QVBoxLayout(box)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        top_layout = QHBoxLayout()

        title_label = QLabel(own_label)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        top_layout.addWidget(title_label)
        layout.addLayout(top_layout)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea { background-color: transparent; }
            QScrollBar:vertical { border: none; background: white; width: 10px;  }
            QScrollBar::handle:vertical { background: #666666; border-radius: 5px; }
            QScrollBar::handle:vertical:hover { background: #888888; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(10)

        books = self.load_downloaded_books(file_name)
        for book in books:
            scroll_layout.addWidget(self.create_book_row(book))

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        return box

    def create_book_row(self, data):
        row_button = QPushButton()
        row_button.setFixedHeight(60)
        row_button.setStyleSheet("""
            QPushButton {
                background-color: #444444;
                border: none;
                border-radius: 10px;
                text-align: left;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """)
        row_button.clicked.connect(lambda: self.go_to_book(data))

        # Layout inside the button
        row_layout = QHBoxLayout(row_button)
        row_layout.setContentsMargins(10, 5, 10, 5)
        row_layout.setSpacing(10)

        author_pic_frame = QFrame(row_button)
        author_pic_frame.setFixedSize(50, 50)
        author_pic_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border-radius: 10px;
            }
        """)

        author_pic = QLabel(author_pic_frame)
        pixmap = QPixmap(data["image"]).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        author_pic.setPixmap(pixmap)
        author_pic.setAlignment(Qt.AlignCenter)

        row_layout.addWidget(author_pic_frame)

        # Book author information
        text_frame = QFrame(row_button)
        text_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
            }
        """)

        text_layout = QVBoxLayout(text_frame)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        name_label = QLabel(data["book"], text_frame)
        name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #FFFFFF;")
        stats_label = QLabel(f"{data['name']} • {data['type']}", text_frame)
        stats_label.setStyleSheet("font-size: 12px; color: #CCCCCC;")

        text_layout.addWidget(name_label)
        text_layout.addWidget(stats_label)
        row_layout.addWidget(text_frame)

        row_layout.addStretch()
        return row_button

    def change_profile_picture(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture", "", "Images (*.png *.jpg *.jpeg)")
        if not file_path:
            print("No profile picture selected.")
            return

        self.new_profile_picture_path = file_path

        pixmap = QPixmap(self.new_profile_picture_path).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.profile_pic.setPixmap(pixmap)

    def save_changes(self):
        import json
        from loginPage import get_saved_user

        username_entered = self.username_edit.text()
        password_entered = self.password_edit.text()

        logged_in_user = get_saved_user()

        if logged_in_user:
            logged_in_username = logged_in_user.get("username")
            logged_in_password = logged_in_user.get("password")

            if username_entered != logged_in_username or password_entered != logged_in_password:
                print("Error: Incorrect username or password.")
                return

            try:
                with open("users.json", "r", encoding="utf-8") as file:
                    data = json.load(file)

                for row in data:
                    if row["username"] == logged_in_username and row["password"] == logged_in_password:

                        row["username"] = username_entered
                        row["password"] = password_entered


                        if hasattr(self, 'new_profile_picture_path'):
                            row["image"] = self.new_profile_picture_path
                        break

                with open("users.json", "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4)

            except FileNotFoundError:
                print("Error: users.json file not found.")
        else:
            print("Error: No user is currently logged in.")

    def go_to_book(self, book_data):
        page = QFrame()
        page.setStyleSheet("background-color: #444444; border-radius: 8px;")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        from bookPage import BookPage
        book_page = BookPage(
            self.pages,
            book_data.get('name', 'No Name'),
            book_data.get('book', 'No Book'),
            book_data.get('type', 'No Type'),
            book_data.get('image', 'No image'),
            book_data.get('description', 'No description')

        )
        layout.addWidget(book_page)

        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

    def load_user_picture(self):
        import json
        from PySide6.QtGui import QPixmap
        from loginPage import get_saved_user

        logged_in_user = get_saved_user()

        if logged_in_user:
            logged_in_username = logged_in_user.get("username")
            logged_in_password = logged_in_user.get("password")
            try:
                with open("users.json","r",encoding="utf-8") as file:
                    data = json.load(file)
                    for row in data:
                        if row["username"] == logged_in_username and row["password"] == logged_in_password:
                            image_path = row["image"]
                            return QPixmap(image_path).scaled(
                                200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation
                            )
                    else:
                        print(f"User '{logged_in_username}' not found in users.json")
            except FileNotFoundError:
                print("Error: users.json file not found.")
        else:
            print("Error: No user is currently logged in.")

        return QPixmap("assets/kitaplar/photomode_13012023_190407.png").scaled(
            200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )