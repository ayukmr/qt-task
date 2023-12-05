from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel

# card widget
class CardWidget(QFrame):
    def __init__(self, card, show_dialog):
        super().__init__()

        description_font = QFont()
        description_font.setPointSize(15)

        # description label
        self.description_label = QLabel(card['description'])
        self.description_label.setFont(description_font)

        title_font = QFont()
        title_font.setPointSize(18)

        # title label
        self.title_label = QLabel(card['title'])
        self.title_label.setFont(title_font)

        difficulty_font = QFont()
        difficulty_font.setPointSize(30)
        difficulty_font.setBold(True)

        # difficulty label
        self.difficulty_label = QLabel(card['difficulty:'])
        self.difficulty_label.setAlignment(Qt.AlignCenter)
        self.difficulty_label.setFont(difficulty_font)

        # main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)
        self.setFixedSize(QSize(150, 150))

        # add widgets
        self.layout.addWidget(self.difficulty_label)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.description_label)

        # show dialog
        self.mousePressEvent = lambda _event: show_dialog(card)

        # stylesheet
        self.setStyleSheet("""
            QFrame {
                border: 1px solid white;
                border-radius: 5px;
            }

            QLabel {
                border: none;
            }
        """)
