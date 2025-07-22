from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QFrame, QVBoxLayout, QHBoxLayout
import sys
from PySide6.QtGui import QCloseEvent, QScreen


class ExampleWindow(QWidget):
    def __init__(self):
        super().__init__()
        screen = QApplication.primaryScreen()
        self.ScreenSize = screen.availableGeometry()
        self.width = self.ScreenSize.width() * 0.6
        self.height = self.ScreenSize.height() * 0.6
        self.setup()

        self.show()

    def setup(self):
        self.setStyleSheet("background-color: #D3B8D8;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.left_panel = self.createLeftPanel()
        layout.addWidget(self.left_panel, 3)

        content = QWidget()
        content_layout = QVBoxLayout(content)

        content_layout.addStretch()

        layout.addWidget(content, 7)

        posX = (self.ScreenSize.width() - self.width)/2
        posY = (self.ScreenSize.height() - self.height)/2

        self.setGeometry(posX, posY, self.width, self.height)
        self.setWindowTitle('Keep And Analyze')

    def createLeftPanel(self):
        frame = QFrame()
        frame.setStyleSheet("background-color: #E0A4A4;")

        layout = QVBoxLayout(frame)
        layout.addStretch()
        return frame


    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(
            self,
            'Message',
            'Are you sure you want to quit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def run():
    app = QApplication(sys.argv)

    ex = ExampleWindow()

    sys.exit(app.exec())

if __name__ == '__main__':
    run()

