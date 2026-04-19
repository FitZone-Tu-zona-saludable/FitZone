from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QFrame, QMessageBox
)
from PySide6.QtCore import Qt

#  Importa UserView oficial del frontend
from frontend.views.user_view import UserView


class PlansView(QWidget):
    def __init__(self, auth, user):
        super().__init__()
        self.auth = auth
        self.user = user

        self.setWindowTitle("FitZone - Planes")
        self.setGeometry(300, 150, 700, 400)

        main_layout = QVBoxLayout()

        title = QLabel("Selecciona tu Plan 💪")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        main_layout.addWidget(title)

        cards_layout = QHBoxLayout()

        # Crear tarjetas
        cards_layout.addWidget(self.create_card("BÁSICO", "$50", "#3498db"))
        cards_layout.addWidget(self.create_card("PREMIUM", "$80", "#2ecc71"))
        cards_layout.addWidget(self.create_card("VIP", "$120", "#e74c3c"))

        main_layout.addLayout(cards_layout)

        self.setLayout(main_layout)

    def create_card(self, title, price, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 15px;
                padding: 15px;
                color: white;
            }}
        """)
        card_layout = QVBoxLayout()

        lbl_title = QLabel(title)
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        card_layout.addWidget(lbl_title)

        lbl_price = QLabel(price)
        lbl_price.setAlignment(Qt.AlignCenter)
        lbl_price.setStyleSheet("font-size: 16px;")
        card_layout.addWidget(lbl_price)

        btn = QPushButton("Seleccionar")
        btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                padding: 8px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ddd;
            }
        """)
        btn.clicked.connect(lambda: self.select_plan(title))
        card_layout.addWidget(btn)

        card.setLayout(card_layout)
        return card

    def select_plan(self, plan):
        self.user.membership = plan

        QMessageBox.information(self, "Plan activado", f"Elegiste el plan {plan}")

        # Ahora abre tu UserView oficial
        self.user_view = UserView(self.user)
        self.user_view.show()
        self.close()