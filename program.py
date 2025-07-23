from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
import sys
from PySide6.QtGui import QCloseEvent, QScreen, QPixmap
from PySide6.QtCore import Qt


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
        #the bottom layer
        main_layout = QHBoxLayout(self) 
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        #left panel
        self.left_panel = self.createLeftPanel()
        main_layout.addWidget(self.left_panel, 3)

        splitter = self.createLeftSPlitter()
        main_layout.addWidget(splitter)

        #content part
        self.content_part = self.createContent()
        main_layout.addWidget(self.content_part, 7)

        #center location
        posX = (self.ScreenSize.width() - self.width)/2
        posY = (self.ScreenSize.height() - self.height)/2

        self.setGeometry(posX, posY, self.width, self.height)
        self.setWindowTitle('Keep And Analyze')

    def createLeftPanel(self):
        frame = QFrame()
        frame.setStyleSheet("background-color: #E0A4A4;")

        layout = QVBoxLayout(frame)
        image_label = QLabel()
        pixmap = QPixmap("images/logo.png")
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(False)
        image_label.setAlignment(Qt.AlignCenter)

        image_label.setMinimumSize(100,100)
        image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        image_label.setPixmap(pixmap.scaled(image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        def resizeEvent(event):
            size = min(image_label.width(), image_label.height())
            image_label.setFixedSize(size,size)
            image_label.setPixmap(pixmap.scaled(size,size,Qt.KeepAspectRatio, Qt.SmoothTransformation))
            event.accept()

        image_label.resizeEvent = resizeEvent
        
        layout.addWidget(image_label)
        layout.addStretch()
        return frame
    
    def createContent(self):
        content = QFrame()
        content.setStyleSheet("background-color: #D3B8D8;")

        layout = QVBoxLayout(content)
        layout.addStretch()
        return content
        
    def createLeftSPlitter(self):
        frame = QFrame()
        frame.setStyleSheet("background-color: white;")
        frame.setFixedWidth(5)
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

