import sys 
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QFrame, 
                             QGraphicsDropShadowEffect, QComboBox) 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPixmap

# --- HELPER FOR SHADOWS ---
def apply_shadow(widget, blur=20, x=0, y=5, alpha=50, color=None):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setXOffset(x)
    shadow.setYOffset(y)
    if color:
        shadow.setColor(color)
    else:
        shadow.setColor(QColor(0, 0, 0, alpha))
    widget.setGraphicsEffect(shadow)

# CHANGED: Inherit from QWidget, NOT QMainWindow
class LoginWindow(QWidget): 
    def __init__(self):  
        super().__init__()  
        self.init_ui()

    def init_ui(self): 
        # Removed setGeometry and setCentralWidget
      
        main_layout = QHBoxLayout() 
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        left_container = self.create_branding_section() 
        right_container = self.create_login_section() 

        main_layout.addWidget(left_container)
        main_layout.addWidget(right_container, stretch=1)

        # Apply layout directly to self (the Widget)
        self.setLayout(main_layout)

    def create_branding_section(self):
        left_container = QFrame()
        left_container.setStyleSheet("""
            QFrame { background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e40af, stop:0.5 #1e3a8a, stop:1 #172554);
            }
        """)
        left_container.setFixedWidth(700) 

        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.setSpacing(25) 
        left_layout.setContentsMargins(50, 60, 50, 40)

        # --- 1. MAIN IDENTITY SECTION ---
        # Logo Circle
        logo_container = QWidget()
        logo_container.setFixedSize(220, 220) 
        logo_container.setStyleSheet("background: transparent;")
        
        logo_layout_inner = QVBoxLayout()
        logo_layout_inner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout_inner.setContentsMargins(0, 0, 0, 0)
        
        logo_logo = QLabel()
        try:
            # Using scaled for better quality
            p = QPixmap("images/cropped_circle_image(1).png")
            logo_logo.setPixmap(p.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        except:
             logo_logo.setText("🔍")
             logo_logo.setFont(QFont("Arial", 60))
             logo_logo.setStyleSheet("color: #fbbf24")

        logo_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout_inner.addWidget(logo_logo)
        logo_container.setLayout(logo_layout_inner)
        
        # Add Glow to Main Logo
        apply_shadow(logo_logo, blur=50, alpha=150, color=QColor("#fbbf24"))

        # Title
        title_label = QLabel("Nexus Monitor")
        title_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #fbbf24; background: transparent;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        apply_shadow(title_label, blur=20, alpha=100)

        subtitle_label = QLabel("Vehicle Violation and Monitoring System")
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setStyleSheet("color: #e2e8f0; background: transparent; letter-spacing: 1px;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Gradient Line Divider
        line = QFrame() 
        line.setFixedHeight(2) 
        line.setFixedWidth(400)
        line.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 transparent, stop:0.5 #fbbf24, stop:1 transparent);
        """)
        
        # --- 2. GOVERNMENT INFO SECTION (Glass Box) ---
        gov_box = QFrame()
        gov_box.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        gov_layout = QVBoxLayout()
        gov_layout.setSpacing(5)
        gov_layout.setContentsMargins(20, 15, 20, 15)

        republic_label = QLabel("REPUBLIC OF THE PHILIPPINES")
        republic_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        republic_label.setStyleSheet("color: #93c5fd; letter-spacing: 2px; background: transparent; border: none;")
        republic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        dept_label = QLabel("DEPARTMENT OF TRANSPORTATION")
        dept_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        dept_label.setStyleSheet("color: #fbbf24; background: transparent; border: none;")
        dept_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        gov_layout.addWidget(republic_label)
        gov_layout.addWidget(dept_label)
        gov_box.setLayout(gov_layout)

        # --- 3. PARTNER LOGOS SECTION (Glass Box) ---
        partners_box = QFrame()
        partners_box.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.1); 
                border-radius: 15px;
            }
        """)
        partners_layout = QVBoxLayout()
        partners_layout.setSpacing(15)
        partners_layout.setContentsMargins(10, 20, 10, 20)

        # Helper to create logo label
        def make_logo(path):
            lbl = QLabel()
            try:
                p = QPixmap(path)
                lbl.setPixmap(p.scaled(100, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            except:
                lbl.setText("LOGO")
                lbl.setStyleSheet("color: white;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("border: none; background: transparent;")
            return lbl

        bagong_logo = make_logo("images/BAGONG-PILIPINAS-LOGO-1-1-150x150.png")
        um_logo = make_logo("images/UM davao.png")

        partners_layout.addWidget(bagong_logo)
        partners_layout.addWidget(um_logo)
        partners_box.setLayout(partners_layout)

        # --- ASSEMBLING LEFT PANEL ---
        left_layout.addStretch(1)
        left_layout.addWidget(logo_container, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(title_label)
        left_layout.addWidget(subtitle_label)
        left_layout.addSpacing(20)
        left_layout.addWidget(line, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addSpacing(20)
        left_layout.addWidget(gov_box)
        left_layout.addSpacing(15)
        left_layout.addWidget(partners_box)
        left_layout.addStretch(1)

        left_container.setLayout(left_layout)
        return left_container
    
    def create_login_section(self):
        right_container = QWidget()
        right_container.setStyleSheet("background-color: #f1f5f9;")

        right_layout = QVBoxLayout()
        right_layout.setSpacing(0)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        right_layout.addStretch(1)

        # Login form container
        form_container = QFrame()
        form_container.setFixedSize(500, 660) 
        form_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: 2px solid #e2e8f0;
            }
        """)

        # Stronger Shadow for "Floating" effect
        apply_shadow(form_container, blur=40, y=10, alpha=40)
        
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(45, 40, 45, 40)
        form_layout.setSpacing(12)

        # Header
        header_container = QFrame()
        header_container.setStyleSheet("background: transparent; border: none;")
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        header_layout.setContentsMargins(0, 0, 0, 0)

        icon_label = QLabel("🔐")
        icon_label.setFont(QFont("Arial", 36))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("background: transparent; border: none;")

        login_header = QLabel('SYSTEM LOGIN')
        login_header.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        login_header.setStyleSheet("color: #1e3a8a; background: transparent; border: none;")
        login_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        welcome_label = QLabel('Access the Nexus Monitoring System')
        welcome_label.setFont(QFont("Arial", 12))
        welcome_label.setStyleSheet("color: #64748b; background: transparent; border: none;")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(icon_label)
        header_layout.addWidget(login_header)
        header_layout.addWidget(welcome_label)
        header_container.setLayout(header_layout)

        form_layout.addWidget(header_container)
        form_layout.addSpacing(15)

        # Role Selection (Styled Section)
        role_container = QFrame()
        role_container.setStyleSheet("""
            QFrame {
                background-color: #f8fafc;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        role_layout = QVBoxLayout()
        role_layout.setSpacing(8)
        role_layout.setContentsMargins(15, 15, 15, 15)

        role_label = QLabel('👤 SELECT YOUR ROLE')
        role_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        role_label.setStyleSheet("color: #1e3a8a; background: transparent; border: none;")

        self.role_combo = QComboBox()
        self.role_combo.addItems(['Admin', 'Traffic Enforcer', 'Citizen']) 
        self.role_combo.setFont(QFont("Arial", 12))
        self.role_combo.setFixedHeight(45)
        self.role_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.role_combo.setStyleSheet("""
            QComboBox {
                padding: 5px 15px;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                background-color: white;
                color: #1e293b;
            }
            QComboBox:hover { border: 2px solid #1e40af; }
            QComboBox::drop-down { border: none; width: 30px; }
        """)

        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)
        role_container.setLayout(role_layout)
        form_layout.addWidget(role_container)
        form_layout.addSpacing(5)

        # Username
        username_label = QLabel('📧 USERNAME')
        username_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        username_label.setStyleSheet("color: #1e3a8a; background: transparent; border: none;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setFont(QFont("Arial", 12))
        self.username_input.setFixedHeight(45)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 0px 15px; 
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                background-color: white; 
                color: #1e293b;
            }
            QLineEdit:focus { border: 2px solid #1e40af; background-color: #f0f9ff; }
        """)
        
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addSpacing(5)

        # Password
        password_label = QLabel('🔑 PASSWORD')
        password_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        password_label.setStyleSheet("color: #1e3a8a; background: transparent; border: none;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your Password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Arial", 12))
        self.password_input.setFixedHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit { 
                padding: 0px 15px;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                background-color: white;
                color: #1e293b;
            }
            QLineEdit:focus { border: 2px solid #1e40af; background-color: #f0f9ff; }
        """)
        
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addStretch(1)

        # Login Button with Highlights
        self.login_btn = QPushButton('🚀 LOGIN TO SYSTEM')
        self.login_btn.setFixedHeight(50)
        self.login_btn.setFont(QFont("Arial",13 ,QFont.Weight.Bold))
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #dc2626, stop:1 #b91c1c);
                color: white;
                border: none;
                border-radius: 12px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #b91c1c, stop:1 #991b1b);
                border: 2px solid #fecaca;
            }
            QPushButton:pressed {
                background-color: #7f1d1d;
            }
        """)
        apply_shadow(self.login_btn, blur=15, y=5, alpha=60, color=QColor("#dc2626"))

        form_layout.addWidget(self.login_btn)
        
        form_container.setLayout(form_layout)
        
        # Center the form
        form_wrapper = QHBoxLayout()
        form_wrapper.addStretch(1)
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch(1)
        
        right_layout.addLayout(form_wrapper)
        right_layout.addStretch(1)

        right_container.setLayout(right_layout)
        return right_container