import csv

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QStackedWidget, QLineEdit, QFileDialog, QSpacerItem,
    QSizePolicy, QScrollArea, QWidget
)
from PySide6.QtGui import QPixmap, QIcon, QPainter
from PySide6.QtCore import Qt

class BookPage(QFrame):
    def __init__(self, pages: QStackedWidget,book_name,book_book,book_type,book_description):
        super().__init__()
        self.setFixedSize(1475, 800)

        self.pages = pages

        self.book_name = book_name
        self.book_book = book_book
        self.book_type = book_type
        self.book_description = book_description


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
        label = QLabel(f'Books')
        label.setStyleSheet("font-size: 35px; font-weight: bold; color: white;")
        top_bar.addWidget(label)
        content_layout.addLayout(top_bar)

        # Gap label search bar
        spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        top_bar.addSpacerItem(spacer)

        # Search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText(f"Search...")
        search_bar.setFixedSize(200, 35)
        icon = QIcon("assets/icons/search_icon.png")
        search_bar.addAction(icon, QLineEdit.TrailingPosition)

        # Icon alignment
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
        box_right = self.create_info_bookBox(book_name,book_book,book_type,book_description)
        boxes.addWidget(box_right)

        content_layout.addLayout(boxes)


        self.setLayout(main_layout)

    def create_info_bookBox(self, book_name, book_book, book_type, book_description):
        box = QFrame()
        box.setFixedSize(1285, 701)
        box.setStyleSheet("background-color: #333333; border-radius: 8px;")

        # Main layout for the box
        layout = QVBoxLayout(box)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)


        title_label = QLabel(f"{book_name}")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
        title_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(title_label)

        # Book image
        book_image = QLabel()
        book_image.setFixedSize(200, 150)  # Rectangle Shape
        book_image.setStyleSheet("border: 2px solid #555555; background-color: #444444;border-radius: 5px;")

        book_image.setAlignment(Qt.AlignCenter)

        # Load an image (replace 'path/to/profile_pic.png' with your image path)
        pixmap = QPixmap(f"assets/kitaplar/{book_name}.png").scaled(300, 250,
                                                                                 Qt.KeepAspectRatioByExpanding,
                                                                                 Qt.SmoothTransformation)
        book_image.setPixmap(pixmap)
        layout.addWidget(book_image, alignment=Qt.AlignLeft)


        book_name_label = QLabel(f"Book Name: {book_name}")
        book_name_label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
        layout.addWidget(book_name_label)


        author_label = QLabel(f"Author: {book_book}")
        author_label.setStyleSheet("font-size: 16px; color: #CCCCCC;")
        layout.addWidget(author_label)


        type_label = QLabel(f"Type: {book_type}")
        type_label.setStyleSheet("font-size: 16px; color: #CCCCCC;")
        layout.addWidget(type_label)


        description_label = QLabel(f"Description:\n{book_description}")
        description_label.setStyleSheet("font-size: 14px; color: #BBBBBB;")
        description_label.setWordWrap(True)
        layout.addWidget(description_label)


        return box

