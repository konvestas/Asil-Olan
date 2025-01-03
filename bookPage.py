from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QStackedWidget, QLineEdit, QFileDialog, QSpacerItem,
    QSizePolicy, QScrollArea, QWidget
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize


class BookPage(QFrame):
    def __init__(self, pages: QStackedWidget, book_name, book_book, book_type, book_image, book_description):
        super().__init__()
        self.setFixedSize(1475, 800)

        self.pages = pages

        self.book_name = book_name
        self.book_book = book_book
        self.book_type = book_type
        self.book_image = book_image
        self.book_description = book_description


        self.setStyleSheet("""
            QWidget { background-color: #222222; color: #FFFFFF; }
            QLineEdit {
                background-color: #333333;
                border: 1px solid #444444;
                border-radius: 8px;
                padding: 5px;
                color: white;
            }
            QLabel { font-size: 14px; }
        """)

        # main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)


        from sideMenu import SideMenu
        side_menu = SideMenu(self.pages)
        side_menu.setFixedWidth(150)
        main_layout.addWidget(side_menu)

        # right content layout
        content_layout = QVBoxLayout()
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(10, 10, 10, 0)

        right_content = QFrame()
        right_content.setLayout(content_layout)
        right_content.setStyleSheet("background-color: #222222;")
        main_layout.addWidget(right_content)

        # Ulibrary
        top_bar = QHBoxLayout()
        label = QLabel('Ulibrary')
        label.setStyleSheet("font-size: 35px; font-weight: bold; color: white;")
        top_bar.addWidget(label)


        spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        top_bar.addSpacerItem(spacer)

        # Search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search...")
        search_bar.setFixedSize(200, 35)
        search_icon = QIcon("assets/icons/search_icon.png")
        search_bar.addAction(search_icon, QLineEdit.TrailingPosition)
        search_bar.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                border: 1px solid #444444;
                border-radius: 8px;
                padding-right: 25px;
                color: white;
            }
        """)
        top_bar.addWidget(search_bar, alignment=Qt.AlignLeft)
        content_layout.addLayout(top_bar)


        boxes = QHBoxLayout()
        box_right = self.create_info_bookBox(book_name, book_book, book_type, book_image, book_description)
        boxes.addWidget(box_right)
        content_layout.addLayout(boxes)

        self.setLayout(main_layout)

    def create_info_bookBox(self, book_name, book_book, book_type, book_image, book_description):
        box = QFrame()
        box.setFixedSize(1300, 701)
        box.setStyleSheet("background-color: #333333; border-radius: 8px;")


        main_layout = QHBoxLayout(box)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(0)

        # Left-side
        left_side_layout = QVBoxLayout()
        left_side_layout.setContentsMargins(0, 0, 0, 0)
        left_side_layout.setSpacing(10)


        nav_buttons_layout = QHBoxLayout()
        nav_buttons_layout.setContentsMargins(5, 0, 0, 70)
        nav_buttons_layout.setSpacing(15)


        back_button = QPushButton()
        back_button.setIcon(QIcon("assets/icons/arrow_back.png"))
        back_button.setIconSize(QSize(20, 20))
        back_button.setFixedSize(40, 40)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
        """)
        back_button.clicked.connect(lambda: self.pages.setCurrentIndex(3))
        nav_buttons_layout.addWidget(back_button)
        nav_buttons_layout.addStretch()

        left_side_layout.addLayout(nav_buttons_layout)

        # Book image layout
        book_pic_layout = QVBoxLayout()
        book_pic_layout.setContentsMargins(80, 0, 55, 120)
        book_pic_layout.setSpacing(0)

        book_picture = QLabel()
        book_picture.setFixedSize(300, 400)
        book_picture.setAlignment(Qt.AlignCenter)
        book_picture.setStyleSheet("border: 2px solid #555555; background-color: #444444; border-radius: 5px;")

        if isinstance(book_image, set):
            book_image = next(iter(book_image), "")

        if isinstance(book_image, str):
            cleaned_image_path = book_image.strip("{} '")
            pixmap = QPixmap(cleaned_image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(300, 400, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                book_picture.setPixmap(pixmap)
            else:
                print(f"Image not found: {cleaned_image_path}")
                book_picture.setText("Image not found")
                book_picture.setStyleSheet("color: #FFFFFF; font-size: 14px;")
        else:
            print("Invalid type for book_image. Expected string or set.")

        book_pic_layout.addWidget(book_picture, alignment=Qt.AlignLeft)
        left_side_layout.addLayout(book_pic_layout)

        main_layout.addLayout(left_side_layout)

        # Right-side
        details_layout = QVBoxLayout()
        details_layout.setSpacing(10)
        details_layout.setAlignment(Qt.AlignCenter)

        # Book title
        title_label = QLabel(f"{book_book}")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF;")
        title_label.setContentsMargins(0, 0, 400, 0)
        details_layout.addWidget(title_label)

        # Author type
        author_type_layout = QHBoxLayout()

        author_label = QLabel(f"Author: {book_name}")
        author_label.setStyleSheet("font-size: 16px; color: #CCCCCC; margin-right: 10px;")
        author_type_layout.addWidget(author_label)

        type_label = QLabel(f"Type: {book_type}")
        type_label.setStyleSheet("font-size: 16px; color: #CCCCCC;")
        type_label.setContentsMargins(0, 0, 400, 0)
        author_type_layout.addWidget(type_label)

        details_layout.addLayout(author_type_layout)

        # Description
        description_label = QLabel(f"Description:\n{book_description}")
        description_label.setStyleSheet("font-size: 14px; color: #BBBBBB;")
        description_label.setWordWrap(True)
        details_layout.addWidget(description_label)

        # Save button
        save_button = QPushButton("Save")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
        """)

        save_button.clicked.connect(lambda: self.save_book(book_name, book_book, book_type, book_image, book_description))
        details_layout.addWidget(save_button, alignment=Qt.AlignLeft)

        main_layout.addLayout(details_layout)
        return box

    def save_book(self, book_name, book_book, book_type, book_image, book_description):
        import json
        try:
            new_book = {
                "name": book_name,
                "book": book_book,
                "type": book_type,
                "image": book_image,
                "description": book_description
            }

            with open("users.json", "r", encoding="utf-8") as file:
                users = json.load(file)

            from loginPage import get_saved_user
            logged_in_user = get_saved_user()
            username = logged_in_user.get("username")

            if not username:
                print("Error: Logged-in username not found.")
                return

            user_found = False
            for user in users:
                if user["username"] == username:
                    user_found = True

                    if "books" not in user:
                        user["books"] = []

                    if any(book["book"] == book_book for book in user["books"]):
                        print(f"The book '{book_book}' is already saved.")
                        return

                    user["books"].append(new_book)
                    break

            if not user_found:
                print(f"Error: User '{username}' not found in users.json.")
                return

            with open("users.json", "w", encoding="utf-8") as file:
                json.dump(users, file, indent=4)

            print(f"The book '{book_book}' has been saved successfully!")

        except FileNotFoundError:
            print("Error: users.json file not found in save_book.")
        except Exception as e:
            print(f"An error occurred in save_book: {e}")

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