from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFormLayout, QSlider, QLabel

# card dialog
class CardDialog(QDialog):
    def __init__(self, parent, callback):
        super().__init__(parent)

        # callback function
        self.callback = callback

        # form layout
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        # difficulty slider
        self.difficulty_slider = QSlider(Qt.Horizontal)
        self.difficulty_slider.setMinimum(1)
        self.difficulty_slider.setMaximum(10)
        self.difficulty_slider.setValue(5)
        self.difficulty_slider.setTickInterval(1)

        # difficulty label
        difficulty_label = QLabel(str(self.difficulty_slider.value()))
        difficulty_label.setFixedWidth(15)

        # connect changes
        self.difficulty_slider.valueChanged.connect(
            lambda value: difficulty_label.setText(str(value))
        )

        # difficulty layout
        difficulty_layout = QHBoxLayout()
        difficulty_layout.addWidget(self.difficulty_slider)
        difficulty_layout.addWidget(difficulty_label)

        # value edits
        self.title_edit = QLineEdit(self)
        self.description_edit = QLineEdit(self)

        # layout rows
        form_layout.addRow('Title:', self.title_edit)
        form_layout.addRow('Difficulty:', difficulty_layout)
        form_layout.addRow('Description:', self.description_edit)

        # save button
        save_button = QPushButton('Save Card')
        save_button.clicked.connect(self.on_save)

        # main layout
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(form_layout)
        self.layout.addWidget(save_button)
        self.setMinimumSize(400, 200)

    # save card
    def on_save(self):
        # run callback
        self.callback(
            self.title_edit.text(),
            str(self.difficulty_slider.value()),
            self.description_edit.text()
        )

        # close dialog
        self.accept()