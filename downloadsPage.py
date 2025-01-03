import csv
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QPushButton, QHBoxLayout, QLabel,
    QLineEdit, QWidget, QStackedWidget, QSpacerItem,
    QSizePolicy, QScrollArea
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt
from PySide6.QtCore import QTimer


class DownloadsPage(QFrame):
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

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        from sideMenu import SideMenu
        side_menu = SideMenu(self.pages)
        side_menu.setFixedWidth(150)
        main_layout.addWidget(side_menu)

        # Right content
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(10)
        self.content_layout.setContentsMargins(10, 10, 10, 0)

        right_content = QFrame()
        right_content.setLayout(self.content_layout)
        right_content.setStyleSheet("background-color: #222222;")
        main_layout.addWidget(right_content)

        # Downloads Label
        top_bar = QHBoxLayout()
        label = QLabel("Downloads")
        label.setStyleSheet("font-size: 35px; font-weight: bold; color: white;")
        top_bar.addWidget(label)
        self.content_layout.addLayout(top_bar)

        # Gap between label and search bar
        spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        top_bar.addSpacerItem(spacer)

        # Search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search...")
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
        self.content_layout.addLayout(top_bar)


        self.box_layout = QHBoxLayout()
        self.content_layout.addLayout(self.box_layout)


        self.book_box = self.create_book_box("Purchased", "users.json")
        self.book_box.setFixedSize(1285, 701)
        self.box_layout.addWidget(self.book_box)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_book_box)
        self.timer.start(3500)

        self.setLayout(main_layout)

    def refresh_book_box(self):
        self.box_layout.removeWidget(self.book_box)
        self.book_box.deleteLater()

        self.book_box = self.create_book_box("Purchased", "users.json")
        self.book_box.setFixedSize(1285, 701)

        self.box_layout.addWidget(self.book_box)

    def load_books_json(self, filename):
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

    def create_book_box(self, own_label, file_name):
        box = QFrame()
        box.setFixedSize(625, 325)
        box.setStyleSheet("background-color: #333333; border-radius: 8px;")

        # Main layout
        layout = QVBoxLayout(box)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Top Section
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

        # Container for scroll content
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

        # Book & author information
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
        info_label = QLabel(f"{data['name']} • {data['type']}", text_frame)
        info_label.setStyleSheet("font-size: 12px; color: #CCCCCC;")

        text_layout.addWidget(name_label)
        text_layout.addWidget(info_label)
        row_layout.addWidget(text_frame)

        row_layout.addStretch()
        return row_button

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

