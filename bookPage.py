from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QStackedWidget, QLineEdit, QFileDialog, QSpacerItem,
    QSizePolicy, QScrollArea, QWidget
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt


class BookPage(QFrame):
    def __init__(self, pages: QStackedWidget, book_name, book_book, book_type, book_description, book_image):
        super().__init__()
        self.setFixedSize(1475, 800)

        self.pages = pages

        self.book_name = book_name
        self.book_book = book_book
        self.book_type = book_type
        self.book_description = book_description
        self.book_image = book_image

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

        # Create main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Side menu
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

        # Add book content
        boxes = QHBoxLayout()
        box_right = self.create_info_bookBox(book_name, book_book, book_type, book_description, book_image)
        boxes.addWidget(box_right)
        content_layout.addLayout(boxes)

        self.setLayout(main_layout)

    def create_info_bookBox(self, book_name, book_book, book_type, book_description, book_image):
        box = QFrame()
        box.setFixedSize(1285, 701)
        box.setStyleSheet("background-color: #333333; border-radius: 8px;")

        main_layout = QHBoxLayout(box)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(30)

        # Book image
        book_pic_layout = QVBoxLayout()
        book_pic_layout.setContentsMargins(180, 0, 0, 0)

        book_picture = QLabel()
        book_picture.setFixedSize(300, 400)
        book_picture.setStyleSheet("border: 2px solid #555555; background-color: #444444; border-radius: 5px;")
        book_picture.setAlignment(Qt.AlignCenter)

        # Handle and clean book_image
        if isinstance(book_image, set):
            book_image = next(iter(book_image), "")

        if isinstance(book_image, str):
            cleaned_image_path = book_image.strip("{} '")
            pixmap = QPixmap(cleaned_image_path)
            if pixmap.isNull():
                print(f"Image not found: {cleaned_image_path}")
                book_picture.setText("Image not found")
                book_picture.setStyleSheet("color: #FFFFFF; font-size: 14px;")
            else:
                pixmap = pixmap.scaled(300, 400, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                book_picture.setPixmap(pixmap)
        else:
            print("Invalid type for book_image. Expected string or set.")

        book_pic_layout.addWidget(book_picture, alignment=Qt.AlignLeft)
        main_layout.addLayout(book_pic_layout)

        # Right side: Details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(10)
        details_layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel(f"{book_book}")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF;")
        details_layout.addWidget(title_label)

        author_type_layout = QHBoxLayout()

        author_label = QLabel(f"Author: {book_name}")
        author_label.setStyleSheet("font-size: 16px; color: #CCCCCC; margin-right: 10px;")
        author_type_layout.addWidget(author_label)

        type_label = QLabel(f"Type: {book_type}")
        type_label.setStyleSheet("font-size: 16px; color: #CCCCCC;")
        author_type_layout.addWidget(type_label, alignment=Qt.AlignLeft)

        details_layout.addLayout(author_type_layout)

        description_label = QLabel(f"Description:\n{book_description}")
        description_label.setStyleSheet("font-size: 14px; color: #BBBBBB;")
        description_label.setWordWrap(True)
        details_layout.addWidget(description_label)

        action_button = QPushButton("Action")
        action_button.setStyleSheet("""
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
        details_layout.addWidget(action_button, alignment=Qt.AlignLeft)

        main_layout.addLayout(details_layout)
        return box