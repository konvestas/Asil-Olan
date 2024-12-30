from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from downloadsPage import DownloadsPage
from homePage import HomePage
from loginPage import LoginPage

from signupPage import SignupPage
from libraryPage import LibraryPage
from profilePage import ProfilePage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ULIBRARY")
        self.setFixedSize(1475, 800)

        # stack pages
        self.pages = QStackedWidget()

        # sign up page 0
        signup_page = SignupPage(self.pages)
        self.pages.addWidget(signup_page)

        # login page 1
        login_page = LoginPage(self.pages)
        self.pages.addWidget(login_page)

        # Home page 2
        home_page = HomePage(self.pages)
        self.pages.addWidget(home_page)

        # Library page 3
        library_page = LibraryPage(self.pages)
        self.pages.addWidget(library_page)

        # Download page 4
        downloads_page = DownloadsPage(self.pages)
        self.pages.addWidget(downloads_page)

        # profile page 5
        profile_page = ProfilePage(self.pages)
        self.pages.addWidget(profile_page)


        self.setCentralWidget(self.pages)
        self.pages.setCurrentIndex(2)



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
