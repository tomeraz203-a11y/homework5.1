import os
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

class Aboutwindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('About Me')
        self.setGeometry(150, 150, 350, 500) 
        
        self.setStyleSheet("background-color: white;")

        self.name = QLabel('Tomer Raz', self)
        self.name.setGeometry(20, 20, 310, 40)
        self.name.setFont(QFont("Arial", 16, QFont.Bold))
        self.name.setAlignment(Qt.AlignCenter)

        self.my_picture = QLabel(self)
        self.my_picture.setGeometry(25, 70, 300, 300)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'barcelona.webp')
        
        image = QPixmap(image_path).scaled(300, 300, Qt.KeepAspectRatio)
        self.my_picture.setPixmap(image)
        self.my_picture.setAlignment(Qt.AlignCenter)

        self.email = QLabel('<a href="mailto:TOMERAZ203@GMAIL.COM">Email: TOMERAZ203@GMAIL.COM</a>', self)
        self.email.setGeometry(20, 390, 310, 30)
        self.email.setOpenExternalLinks(True) 
        self.email.setAlignment(Qt.AlignCenter)
        self.email.setFont(QFont("Arial", 10))
        
        self.linkedin = QLabel('<a href="https://www.linkedin.com/in/תומר-רז-2806b7431">Click here for my LinkedIn Profile</a>', self)
        self.linkedin.setGeometry(20, 420, 310, 30)
        self.linkedin.setOpenExternalLinks(True) 
        self.linkedin.setAlignment(Qt.AlignCenter)
        self.linkedin.setFont(QFont("Arial", 10))

        self.github = QLabel(
            '<a href="https://github.com/tomeraz203-a11y/homework5.1">Click here for my GitHub Profile</a>',
            self,
        )
        self.github.setGeometry(20, 450, 310, 30)
        self.github.setOpenExternalLinks(True)
        self.github.setAlignment(Qt.AlignCenter)
        self.github.setFont(QFont("Arial", 10))

if __name__ == '__main__':
    app = QApplication([])
    window = Aboutwindow()
    window.show()
    app.exec()