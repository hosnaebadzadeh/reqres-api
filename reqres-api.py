import sys
import requests
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QScrollArea
from PyQt6.QtGui import QPixmap


class UserApp(QWidget):
    def __init__(self):
        super(UserApp, self).__init__()
        self.setWindowTitle("User List")

        scrl = QScrollArea()
        scrl.setWidgetResizable(True)


        user_container = QWidget()
        user_layout = QVBoxLayout()

        users = self.fetch_users()
        for user in users:
            user_widget = UserWidget(user)
            user_layout.addWidget(user_widget)

        user_container.setLayout(user_layout)
        scrl.setWidget(user_container)

        # Main Layout
        mlayout = QVBoxLayout()
        mlayout.addWidget(scrl)
        self.setLayout(mlayout)

        welcomelbl = QLabel("Welcome ReqRes users, connect to anyone you want using their email")
        welcomelbl .setStyleSheet("font-size: 16px; font-weight: bold; text-align: center; margin: 10px;")
        mlayout.addWidget(welcomelbl )


    def fetch_users(self):
        try:
            response = requests.get("https://reqres.in/api/users?page=1")
            if response.status_code == 200:
                data = response.json()
                return data["data"]
            else:
                print("Failed to fetch data from API")
                return
        except Exception as e:
            print(f"Error: {e}")
            return


class UserWidget(QWidget):
    def __init__(self, user):
        super(UserWidget, self).__init__()
        layout = QVBoxLayout()

        avatarlbl = QLabel()
        response = requests.get(user["avatar"])
        image = QPixmap()
        image.loadFromData(response.content)
        avatarlbl.setPixmap(image.scaled(100, 100))
        namelbl= QLabel(f"Name: {user['first_name']} {user['last_name']}")
        emaillbl= QLabel(f"Email: {user['email']}")

        layout.addWidget(avatarlbl)
        layout.addWidget(namelbl)
        layout.addWidget(emaillbl)
        self.setLayout(layout)






app = QApplication(sys.argv)
user_app = UserApp()
user_app.resize(800, 800)
user_app.show()
sys.exit(app.exec())

