from card_widget import CardWidget
from card_dialog import CardDialog
from create_button import CreateButton

import requests

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QSlider, QScrollArea, QPushButton
from PySide6.QtGui import QFont

# main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # minimum size
        self.setMinimumSize(1200, 600)

        # difficulty slider
        self.difficulty_slider = QSlider(Qt.Horizontal)
        self.difficulty_slider.setMinimum(1)
        self.difficulty_slider.setMaximum(10)
        self.difficulty_slider.setValue(5)
        self.difficulty_slider.setTickInterval(1)

        difficulty_font = QFont()
        difficulty_font.setPointSize(25)

        # difficulty label
        difficulty_label = QLabel(str(self.difficulty_slider.value()))
        difficulty_label.setFont(difficulty_font)
        difficulty_label.setFixedWidth(30)
        difficulty_label.setAlignment(Qt.AlignRight)

        # slider changed
        self.difficulty_slider.valueChanged.connect(lambda value: difficulty_label.setText(str(value)))
        self.difficulty_slider.valueChanged.connect(self.display_cards)

        # create button
        create_button = CreateButton()
        create_button.clicked.connect(lambda: CardDialog(self, self.create_card).exec())

        # top bar layout
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        top_layout.addWidget(difficulty_label)
        top_layout.addWidget(self.difficulty_slider)
        top_layout.addWidget(create_button)

        # cards layout
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setSpacing(10)
        self.cards_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # scroll widget
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.cards_layout)

        # scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        # main layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.addLayout(top_layout)
        self.layout.addWidget(scroll_area)

        # central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # reload cards
        self.reload_cards()

    # card index by id
    def card_index(self, id):
        return [self.cards.index(card) for card in self.cards if card['id'] == id]

    # create card
    def create_card(self, title, difficulty, description):
        # add card
        card = {'title': title, 'difficulty': difficulty, 'description': description}
        requests.post('http://localhost:5000/api/makecard', json = card)

        # reload cards
        self.reload_cards()

    # show card dialog
    def card_dialog(self, card):
        # save button
        delete_button = QPushButton('Delete Card')
        delete_button.clicked.connect(lambda: self.delete_card(card['id']))

        CardDialog(self, lambda *args: self.update_card(card['id'], *args), card, delete_button).exec()

    # update card
    def update_card(self, id, title, difficulty, description):
        # edit card
        card = {'id': id, 'title': title, 'difficulty': difficulty, 'description': description}
        requests.post('http://localhost:5000/api/editcard', json=card)

        # reload cards
        self.reload_cards()

    # delete card
    def delete_card(self, id):
        # remove card
        requests.post('http://localhost:5000/api/removecard', json={'id': id})

        # reload cards
        self.reload_cards()

    # reload cards
    def reload_cards(self):
        self.cards = requests.post('http://localhost:5000/api/getcards').json()['cards']
        self.display_cards()

    # reload cards
    def display_cards(self):
        # remove old cards
        while item := self.cards_layout.takeAt(0):
            if row_layout := item.layout():
                # remove layout cards
                while widget := row_layout.takeAt(0):
                    widget.widget().deleteLater()

                # remove layout
                row_layout.deleteLater()
            elif widget := item.widget():
                # remove priority
                widget.deleteLater()

        # filter difficulties
        cards = list(filter(
            lambda card: int(card['difficulty:']) <= self.difficulty_slider.value(),
            self.cards
        ))

        if not cards:
            return

        # sort cards
        cards.sort(key=lambda card: int(card['difficulty:']), reverse=True)

        # add priority
        priority = cards.pop(0)
        self.cards_layout.addWidget(CardWidget(priority, self.card_dialog))

        # row layout
        row_layout = QHBoxLayout()
        row_layout.setAlignment(Qt.AlignLeft)

        # show cards
        for index, card in enumerate(cards):
            # create row
            if index % 7 == 0:
                self.cards_layout.addLayout(row_layout)
                row_layout = QHBoxLayout()
                row_layout.setAlignment(Qt.AlignLeft)

            # add card
            card_widget = CardWidget(card, self.card_dialog)
            row_layout.addWidget(card_widget)

        self.cards_layout.addLayout(row_layout)
