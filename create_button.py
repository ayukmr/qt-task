from PySide6.QtWidgets import QPushButton

# create button
class CreateButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__('Add Card', parent)

        # stylesheet
        self.setStyleSheet("""
            QPushButton {
                border-radius: 4px;
                border: 1px solid #474747;
                font-size: 15px;
                padding: 3px 6px;
            }

            QPushButton::hover {
                color: white;
                background: #474747;
            }
        """)
