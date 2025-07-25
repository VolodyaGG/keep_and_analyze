from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QGraphicsDropShadowEffect
import sys
from PySide6.QtGui import QCloseEvent, QScreen, QPixmap, QColor
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QSize, QRect, QEasingCurve


class Window(QWidget):
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

        #shadow and splitter
        splitter = self.createLeftSPlitter()
        splitter.setGraphicsEffect(QGraphicsDropShadowEffect(self, blurRadius=15, offset=QPoint(3, 0), color=QColor(0, 0, 0, 160)))
        main_layout.addWidget(splitter)

        #content part
        self.content_part = self.createContent()
        main_layout.addWidget(self.content_part, 7)
        
        splitter.raise_()

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
        image_label.setAlignment(Qt.AlignCenter)

        width = 0.3 * self.width

        image_label.setMinimumSize(width,width)
        image_label.setScaledContents(True)

        image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        raise_scale(image_label, 1.05, 200)
        
        
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

"""
def raise_scale(label, scale_factor=1.2, duration=500):
    original_size = label.minimumSize()
    label.anim = QPropertyAnimation(label, b"size")

    def enter_image(event):
        label.anim.stop()
        label.anim.setDuration(duration)
        label.anim.setStartValue(label.size())
        label.anim.setEndValue(QSize(int(original_size.width() * scale_factor), int(original_size.height() * scale_factor)))    
        label.anim.start()

    def leave_image(event):
        label.anim.stop()
        label.anim.setDuration(duration)
        label.anim.setStartValue(label.size())
        label.anim.setEndValue(original_size)
        label.anim.start()

    label.enterEvent = enter_image
    label.leaveEvent = leave_image
"""
def raise_scale(label, scale_factor=1.2, duration=300):
    original_geometry = None
    is_animating = False
    
    #Создаем анимацию для geometry (позиция + размер)
    label.anim = QPropertyAnimation(label, b"geometry")
    label.anim.setEasingCurve(QEasingCurve.OutCubic)  # Плавная кривая анимации
    
    def animation_finished():
        nonlocal is_animating
        is_animating = False

    label.anim.finished.connect(animation_finished)

    def enter_image(event):
        nonlocal original_geometry, is_animating
        
        if is_animating:
            return
            
        if original_geometry is None:
            original_geometry = label.geometry()
        
        is_animating = True
        current_rect = label.geometry()
        
        # Вычисляем новый размер
        new_width = int(original_geometry.width() * scale_factor)
        new_height = int(original_geometry.height() * scale_factor)
        
        # Вычисляем новую позицию для центрирования относительно оригинальной позиции
        center_x = original_geometry.x() + original_geometry.width() // 2
        center_y = original_geometry.y() + original_geometry.height() // 2
        
        new_x = center_x - new_width // 2
        new_y = center_y - new_height // 2
        
        new_rect = QRect(new_x, new_y, new_width, new_height)
        
        label.anim.setDuration(duration)
        label.anim.setStartValue(current_rect)
        label.anim.setEndValue(new_rect)
        label.anim.start()

    def leave_image(event):
        nonlocal original_geometry, is_animating
        
        if is_animating or original_geometry is None:
            return
            
        is_animating = True
        current_rect = label.geometry()
        
        label.anim.setDuration(duration)
        label.anim.setStartValue(current_rect)
        label.anim.setEndValue(original_geometry)
        label.anim.start()

    label.enterEvent = enter_image
    label.leaveEvent = leave_image

def run():
    app = QApplication(sys.argv)

    ex = Window()

    sys.exit(app.exec())

if __name__ == '__main__':
    run()

