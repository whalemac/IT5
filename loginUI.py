import sys 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
                            QFrame,  QGraphicsDropShadowEffect, QComboBox) 
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer 
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtGui import QFont, QColor, QPixmap
import sqlite3
 
class LoginWindow(QMainWindow): 
    
    def __init__(self):  
        super().__init__()  
        self.init_ui()

    def init_ui(self): 
        self.setWindowTitle('Vehicle Violation and Monitoring') 
        self.setGeometry(100, 50, 1300, 750) 
        self.setMinimumSize(1200, 700) 
     
        central_widget = QWidget() 
        self.setCentralWidget(central_widget)
         
        #main Layout 
        main_layout = QHBoxLayout() 
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        #container left
        left_container = self.create_branding_section() 
        #container right 
        right_container = self.create_login_section() 

        #main layout two side
        main_layout.addWidget(left_container)
        main_layout.addWidget(right_container, stretch=1)

        #layout in the central Widget
        central_widget.setLayout(main_layout)

    def create_branding_section(self):

        #left section branding and logo 
        left_container = QFrame()
        left_container.setStyleSheet("""
            QFrame { background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e40af, stop:0.5 #1e3a8a, stop:1 #172554);
            }
        """)
        left_container.setFixedWidth(750)

        # main layout for the left section 
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.setSpacing(0) 
        left_layout.setContentsMargins(40, 60, 40, 40)


        #logo Circle
        logo_container = QFrame()
        logo_container.setFixedSize(180, 180)
        logo_container.setStyleSheet("""
            QFrame { 
                background-color: #dc2626;
                border-radius: 90px;
                border: 10px solid #fbbf24;
            }
                """)
        
        #add effect on the logo 
        logo_shadow = QGraphicsDropShadowEffect() 
        logo_shadow.setBlurRadius(40) 
        logo_shadow.setColor (QColor(251, 191, 36, 200))   
        logo_shadow.setOffset(0, 0) 
        logo_container.setGraphicsEffect(logo_shadow)

        logo_layout = QVBoxLayout() 
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_label = QLabel ("Nexus Monitor")
        logo_label.setFont(QFont ("Arial", 14, QFont.Weight.Bold))
        logo_label.setStyleSheet("color: #fbbf24; border: none;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_layout.addWidget(logo_label)
        logo_container.setLayout(logo_layout)
        
        

        #Title style and Alignment and effect
        title_label = QLabel("Nexus Monitor")
        title_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #fbbf24; background: transparent; ")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle_label = QLabel("Vehicle Violation and Monitoring System")
        subtitle_label.setFont(QFont("Arial", 15))
        subtitle_label.setStyleSheet("color: #fbbf24; background: transparent; ")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Line design 
        line = QFrame() 
        line.setFixedHeight(2) 
        line.setFixedWidth(500)
        line.setStyleSheet("background-color: #fbbf24; border-radius: 2px;")
        
        #republic and department info 
        republic_label = QLabel("REPUBLIC OF THE PHILIPPINES")
        republic_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        republic_label.setStyleSheet("color: #93c5fd; letter-spacing: 2px; background: transparent;")
        republic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        #dep label 
        dept_label = QLabel("DEPARTMENT OF TRANSPORTATION")
        dept_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        dept_label.setStyleSheet("color: #fbbf24; background: transparent;")
        dept_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # Bagong Pilipinas badge
        bagong_container = QWidget()
        bagong_container.setFixedSize(240, 120)
        bagong_container.setStyleSheet("background: transparent;")

        bagong_layout = QVBoxLayout()
        bagong_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bagong_layout.setContentsMargins(0, 0, 0, 0)
        
        bagong_logo = QLabel()
        bagong_logo.setPixmap(QPixmap("BAGONG-PILIPINAS-LOGO-1-1-150x150.png").scaled(
                 180, 100, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
                ))
        bagong_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bagong_layout.addWidget(bagong_logo)
        bagong_container.setLayout(bagong_layout)

        #UM logo
        um_container = QWidget()
        um_container.setFixedSize(240, 120)
        um_container.setStyleSheet("background: transparent;")

        um_layout = QVBoxLayout()
        um_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        um_layout.setContentsMargins(0, 0, 0, 0)
        
        um_logo = QLabel()
        um_logo.setPixmap(QPixmap("UM davao.png").scaled(
                 180, 100, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
                ))
        um_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        um_layout.addWidget(um_logo)
        um_container.setLayout(um_layout)


        #alignment on left panel
        left_layout.addWidget(logo_container, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addSpacing(30)
        left_layout.addWidget(title_label)
        left_layout.addSpacing(8)
        left_layout.addWidget(subtitle_label)
        left_layout.addSpacing(25)
        left_layout.addWidget(line, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addSpacing(25)
        left_layout.addWidget(republic_label)
        left_layout.addSpacing(8)
        left_layout.addWidget(dept_label)
        left_layout.addSpacing(25)
        left_layout.addWidget(bagong_container, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addSpacing(15)
        left_layout.addWidget(um_container, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addStretch()



        left_container.setLayout(left_layout)
        return left_container

    
    def create_login_section(self):

        #Login section 
        right_container = QWidget()
        right_container.setStyleSheet("background-color: #f1f5f9;")

        # FIXED: Changed alignment and added stretch to keep form centered
        right_layout = QVBoxLayout()
        right_layout.setSpacing(0)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add top stretch
        right_layout.addStretch(1)

        # Login form container with modern shadow
        form_container = QFrame()
        form_container.setFixedSize(500, 640)  # Fixed size prevents movement
        form_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: 3px solid #e2e8f0;
            }
        """)

        # Add modern shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(30, 58, 138, 60))
        shadow.setOffset(0, 10)
        form_container.setGraphicsEffect(shadow)
        
        # FIXED: Consistent spacing in form layout
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(45, 40, 45, 40)
        form_layout.setSpacing(10)

        # Login header with icon
        header_container = QFrame()
        header_container.setStyleSheet("background: transparent; border: none;")
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        header_layout.setContentsMargins(0, 0, 0, 0)

        #icon label 
        icon_label = QLabel("🔐")
        icon_label.setFont(QFont("Arial", 30))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("background: transparent; border: none;")

        #log in Header 
        login_header = QLabel('SYSTEM LOGIN')
        login_header.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        login_header.setStyleSheet("color: #1e3a8a; background: transparent; border: none;")
        login_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        welcome_label = QLabel('Access the Nexus Monitoring System')
        welcome_label.setFont(QFont("Arial", 12))
        welcome_label.setStyleSheet("color: #64748b; background: transparent; border: none;")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #function Panel 
        header_layout.addWidget(icon_label)
        header_layout.addWidget(login_header)
        header_layout.addWidget(welcome_label)
        header_container.setLayout(header_layout)

        form_layout.addWidget(header_container)
        form_layout.addSpacing(15)

        # User Role Selection with icon
        role_container = QFrame()
        role_container.setStyleSheet("""
            QFrame {
                background-color: #f8fafc;
                border-radius: 12px;
                padding: 15px;
                border: none;
            }
        """)
        role_layout = QVBoxLayout()
        role_layout.setSpacing(10)
        role_layout.setContentsMargins(10, 5, 10, 5)

        role_label = QLabel('👤 SELECT YOUR ROLE')
        role_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        role_label.setStyleSheet("color: #1e3a8a; background: transparent; border: none;")

        #box and function for username
        self.role_combo = QComboBox()
        self.role_combo.addItems(['Traffic Enforcer', 'Citizen'])
        self.role_combo.setFont(QFont("Arial", 12))
        self.role_combo.setFixedHeight(45)
        self.role_combo.setStyleSheet("""
            QComboBox {
                padding: 12px 15px;
                border: 2px solid #cbd5e1;
                border-radius: 10px;
                background-color: white;
                font-size: 14px;
                color: #1e293b;
            }
            QComboBox:hover {
                border: 2px solid #1e40af;
            }
            QComboBox:focus {
                border: 2px solid #1e40af;
                background-color: #f0f9ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 35px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #1e40af;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #cbd5e1;
                border-radius: 10px;
                background-color: white;
                selection-background-color: #1e40af;
                selection-color: white;
                padding: 5px;
            }
        """)

        #Show Panel
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)
        role_container.setLayout(role_layout)
        form_layout.addWidget(role_container)
        form_layout.addSpacing(10)

        # Username with modern design
        username_label = QLabel('📧 USERNAME')
        username_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        username_label.setStyleSheet("color: #1e3a8a; background: transparent; border: none;")

        #function and typein username 
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setFont(QFont("Arial", 13))
        self.username_input.setFixedHeight(45)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px; 
                border: 2px solid #cbd5e1;
                border-radius: 10px;
                background-color: white; 
                font-size: 14px;
                color: #1e293b;
            }
            QLineEdit:hover {
                border: 2px solid #1e40af;
            }
            QLineEdit:focus {
                border: 2px solid #1e40af;
                background-color: #f0f9ff;
            }                             
        """)
        
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addSpacing(10)

        # Password with modern design
        password_label = QLabel('🔑 PASSWORD')
        password_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        password_label.setStyleSheet("color: #1e3a8a; background: transparent; border: none;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your Password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Arial", 13))
        self.password_input.setFixedHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit { 
                padding: 12px 15px;
                border: 2px solid #cbd5e1;
                border-radius: 10px;
                background-color: white;
                font-size: 14px;
                color: #1e293b;
            }
            QLineEdit:hover {
                border: 2px solid #1e40af;
            }
            QLineEdit:focus { 
                border: 2px solid #1e40af;
                background-color: #f0f9ff;
            }
        """)
        
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addStretch(1)
        
        

        #log in button 

        self.login_btn = QPushButton('🚀 LOGIN TO SYSTEM')
        self.login_btn.setFixedHeight(45)
        self.login_btn.setFont(QFont("Arial",14 ,QFont.Weight.Bold))
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #dc2626, stop:1 #b91c1c);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                padding: 15px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #b91c1c, stop:1 #991b1b);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #991b1b, stop:1 #7f1d1d);
            }
        """)

        form_layout.addWidget(self.login_btn)
        
        # Sample credentials info
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #fef3c7, stop:1 #fef08a);
                border: 2px solid #fbbf24;
                border-radius: 12px;
                padding: 12px;
                                 }
         """)
        
        form_container.setLayout(form_layout)
        
        # Center the form horizontally
        form_wrapper = QHBoxLayout()
        form_wrapper.addStretch(1)
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch(1)
        
        right_layout.addLayout(form_wrapper)
        right_layout.addStretch(1)

        



        right_container.setLayout(right_layout)
        return right_container
    


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont('Arial', 10))  
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()