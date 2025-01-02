from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget, QWidget, QLabel
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtCore import QSize


class SideMenu(QWidget):
    def __init__(self, pages: QStackedWidget): #pages
        super().__init__()
        self.pages = pages

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(118)
        sidebar.setStyleSheet("""
                          QFrame {
                              background-color: #333333;
                              border: none;
                              border-radius: 13px;
                          }
                          QPushButton {
                              background-color: transparent;
                              border: none;
                              color: #FFFFFF;
                               font-size: 12px;
                              padding: 10px;
                              text-align: left;
                          }
                          QPushButton:hover {
                              background-color: #444444;
                              border-radius: 10px;
                          }
                      """)


        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 30)
        sidebar_layout.setSpacing(20)

        # Logo at the top
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/icons/logo.jpg").scaled(80, 80, aspectMode=Qt.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setStyleSheet(
            "border-radius: 10px;")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setContentsMargins(0,20,0,0)


        sidebar_layout.addWidget(logo_label)

        # Separator line 1
        separator_layout = QHBoxLayout()
        separator_layout.setContentsMargins(18, 0, 18, 0)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("QFrame { border: 1px solid #555555; background-color: #777777; }")

        separator_layout.addWidget(separator)
        sidebar_layout.addLayout(separator_layout)
        sidebar_layout.addSpacing(35)


        buttons = [
            {"text": "Home", "icon": "assets/icons/home_icon.png", "index": 2},
            {"text": "Library", "icon": "assets/icons/book_icon.png", "index": 3},
            {"text": "Downloads", "icon": "assets/icons/download_icon.png", "index": 4},
        ]

        for button in buttons:
            btn = QPushButton(button["text"])
            btn.setIcon(QIcon(button["icon"]))
            btn.setIconSize(QSize(24, 24))
            btn.clicked.connect(lambda checked, index=button["index"]: self.pages.setCurrentIndex(index))
            sidebar_layout.addWidget(btn)

        # push content up
        sidebar_layout.addStretch()

        # Separator line 2
        separator_layout = QHBoxLayout()
        separator_layout.setContentsMargins(18, 0, 18, 0)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("QFrame { border: 1px solid #555555; background-color: #777777; }")

        separator_layout.addWidget(separator)
        sidebar_layout.addLayout(separator_layout)


        bottom_buttons = [
            {"text": "Profile", "icon": "assets/icons/profile_icon.png", "index": 5},
            {"text": "Logout", "icon": "assets/icons/logout_icon.png", "index": 1},
        ]

        for button in bottom_buttons:
            btn = QPushButton(button["text"])
            btn.setIcon(QIcon(button["icon"]))
            btn.setIconSize(QSize(24, 24))
            btn.clicked.connect(lambda checked, index=button["index"]: self.pages.setCurrentIndex(index))
            sidebar_layout.addWidget(btn)
        sidebar.setLayout(sidebar_layout)


        layout = QHBoxLayout(self)
        layout.addWidget(sidebar)
        layout.addStretch()

        self.setLayout(layout)