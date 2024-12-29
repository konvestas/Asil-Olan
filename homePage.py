import csv

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QPushButton, QHBoxLayout, QLabel,
    QLineEdit, QWidget, QListWidget, QStackedWidget, QSpacerItem,
    QSizePolicy,QScrollArea
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt

class HomePage(QFrame):
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
        content_layout.setContentsMargins(10, 10, 10, 20)

        right_content = QFrame()
        right_content.setLayout(content_layout)
        right_content.setStyleSheet("background-color: #222222;")
        main_layout.addWidget(right_content)

        # Discover Label
        top_bar = QHBoxLayout()
        label = QLabel("Discover")
        label.setStyleSheet("font-size: 35px; font-weight: bold; color: white;")
        top_bar.addWidget(label)
        content_layout.addLayout(top_bar)

        # Gap between  label and search bar
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

        box_topleft = QFrame()
        box_topleft.setFixedSize(620, 325)
        box_topleft.setStyleSheet("background-color: #333333; border-radius: 8px;")

        # Box Top Right with Podcasters Layout
        box_topright = self.create_book_box("Top rated books", "mostDownloadedBooks")

        top_boxes_layout.addWidget(box_topleft)
        top_boxes_layout.addWidget(box_topright)
        content_layout.addLayout(top_boxes_layout)


        # Bottom Boxes
        bottom_boxes_layout = QHBoxLayout()
        box_botleft = self.create_book_box("New books", "topBooks")
        box_botright = self.create_book_box("Our recommedations", "mostViewedBooks")
        bottom_boxes_layout.addWidget(box_botleft)
        bottom_boxes_layout.addWidget(box_botright)
        content_layout.addLayout(bottom_boxes_layout)

        self.setLayout(main_layout)

    def navigate_library(self):
        self.pages.setCurrentIndex(3)

    def load_books_from_csv(self, filename):
        author = []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    author.append({
                        "name": row["name"],
                        "book": row["book"],
                        "type": row["type"],
                        "description": row["description"],
                        "image": row["image"]
                    })
        except Exception as e:
            print(f"Error reading CSV file: {e}")
        return author

    def create_book_box(self, own_label, file_name):
        box = QFrame()
        box.setFixedSize(625, 325)
        box.setStyleSheet("background-color: #333333; border-radius: 8px;")

        # Main layout for the box
        layout = QVBoxLayout(box)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Top Section
        top_layout = QHBoxLayout()
        title_label = QLabel(own_label)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        top_layout.addWidget(title_label)
        layout.addLayout(top_layout)

        seeMore_btn = QPushButton("See more")
        seeMore_btn.setFixedSize(100, 30)
        seeMore_btn.setStyleSheet("""
                QPushButton {
                    background-color: #555555;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #777777;
                }
            """)
        seeMore_btn.clicked.connect(lambda: self.navigate_library())
        top_layout.addStretch()
        top_layout.addWidget(seeMore_btn)
        layout.addLayout(top_layout)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea { background-color: transparent; }
            QScrollBar:vertical { border: none; background: #444444; width: 10px;  }
            QScrollBar::handle:vertical { background: #666666; border-radius: 5px; }
            QScrollBar::handle:vertical:hover { background: #888888; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        # Container for scroll content
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(10)

        # create row
        authors = self.load_books_from_csv(file_name)
        for author in authors:
            scroll_layout.addWidget(self.create_book_row(author))

        scroll_layout.addStretch()

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        return box

    def create_book_row(self, data):
        row = QFrame()
        row.setFixedHeight(60)
        row.setStyleSheet("background-color: #444444; border-radius: 10px;")

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(10, 5, 10, 5)
        row_layout.setSpacing(10)

        # Author Picture
        author_pic = QLabel()
        pixmap = QPixmap(data["image"]).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        author_pic.setPixmap(pixmap)
        author_pic.setFixedSize(50, 50)
        row_layout.addWidget(author_pic)

        # Text Information
        text_layout = QVBoxLayout()
        name_label = QLabel(data["book"])
        name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        stats_label = QLabel(f"{data['name']} • {data['type']}")
        stats_label.setStyleSheet("font-size: 12px; color: #CCCCCC;")

        text_layout.addWidget(name_label)
        text_layout.addWidget(stats_label)
        row_layout.addLayout(text_layout)

        return row