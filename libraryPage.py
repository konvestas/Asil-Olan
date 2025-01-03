from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QPushButton, QHBoxLayout, QLabel,
    QLineEdit, QWidget, QStackedWidget, QSpacerItem,
    QSizePolicy, QScrollArea
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt


class LibraryPage(QFrame):
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

        # Library Label
        top_bar = QHBoxLayout()
        label = QLabel("Library")
        label.setStyleSheet("font-size: 35px; font-weight: bold; color: white;")
        top_bar.addWidget(label)
        content_layout.addLayout(top_bar)

        # Gap label search bar
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
        content_layout.addLayout(top_bar)

        # Top Boxes
        top_boxes_layout = QHBoxLayout()

        box_topleft = self.create_book_box("Top books", "topBook.json")
        box_topleft.setFixedSize(410, 701)

        box_topmiddle = self.create_book_box("Most viewed", "mostViewed.json")
        box_topmiddle.setFixedSize(410, 701)

        box_topright = self.create_book_box("Most downloaded", "mostDownloaded.json")
        box_topright.setFixedSize(410, 701)

        top_boxes_layout.addWidget(box_topleft)
        top_boxes_layout.addWidget(box_topmiddle)
        top_boxes_layout.addWidget(box_topright)
        content_layout.addLayout(top_boxes_layout)

        self.setLayout(main_layout)

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

        text_layout.addWidget(name_label)
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