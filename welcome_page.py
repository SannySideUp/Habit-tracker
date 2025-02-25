import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class WelcomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Welcome!")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # Logo (Optional)
        logo = QLabel(self)
        pixmap = QPixmap("logo.jpeg")  # Replace with your logo file
        logo.setPixmap(pixmap)
        logo.setScaledContents(True)
        logo.resize(200, 100)
        
        # Welcome Message
        welcome_label = QLabel("Welcome to habits buddy!", self)
        welcome_label.setFont(QFont("Arial", 16))
        welcome_label.setStyleSheet("color: #333;")
        welcome_label.setAlignment(Qt.AlignCenter)
        
        # Start Button
        start_button = QPushButton("Get Started", self)
        start_button.setFont(QFont("Arial", 12))
        start_button.setStyleSheet("background-color: #0078D7; color: white; padding: 10px;")
        start_button.clicked.connect(self.start_app)
        
        # Adding widgets to layout
        layout.addWidget(logo)
        layout.addWidget(welcome_label)
        layout.addWidget(start_button)
        
        self.setLayout(layout)
    
    def start_app(self):
        print("Starting application...")  # Replace with actual functionality
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomePage()
    window.show()
    sys.exit(app.exec_())
