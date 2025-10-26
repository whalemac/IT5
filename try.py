import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QComboBox, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette
import sqlite3


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_database()
        self.init_ui()
        
    def init_database(self):
        """Initialize database with sample users"""
        conn = sqlite3.connect('vehicle_violation.db')
        cursor = conn.cursor()
        
        # Create users table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT
            )
        ''')
        
        # Insert sample users (only if table is empty)
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            sample_users = [
                ('admin', 'admin123', 'Admin', 'System Administrator'),
                ('enforcer1', 'enf123', 'Enforcer', 'Officer Juan Dela Cruz'),
                ('citizen1', 'cit123', 'Citizen', 'Maria Santos')
            ]
            cursor.executemany(
                'INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)',
                sample_users
            )
        
        conn.commit()
        conn.close()
        
    def init_ui(self):
        self.setWindowTitle('LTO - Vehicle Violation Monitoring System')
        self.setGeometry(100, 50, 1300, 750)
        self.setMinimumSize(1200, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left side - Branding (Wider and more impressive)
        left_container = self.create_branding_section()
        
        # Right side - Login Form
        right_container = self.create_login_section()
        
        # Add both sides to main layout
        main_layout.addWidget(left_container)
        main_layout.addWidget(right_container, stretch=1)
        
        central_widget.setLayout(main_layout)
        
        # Set focus to username
        self.username_input.setFocus()
        
    def create_branding_section(self):
        """Create the left branding section"""
        left_container = QFrame()
        left_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e40af, stop:0.5 #1e3a8a, stop:1 #172554);
            }
        """)
        left_container.setFixedWidth(550)
        
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.setSpacing(25)
        left_layout.setContentsMargins(40, 40, 40, 40)
        
        # LTO Seal with glow effect
        seal_container = QFrame()
        seal_container.setFixedSize(180, 180)
        seal_container.setStyleSheet("""
            QFrame {
                background-color: #dc2626;
                border-radius: 90px;
                border: 10px solid #fbbf24;
            }
        """)
        
        # Add glow effect to seal
        seal_shadow = QGraphicsDropShadowEffect()
        seal_shadow.setBlurRadius(40)
        seal_shadow.setColor(QColor(251, 191, 36, 200))
        seal_shadow.setOffset(0, 0)
        seal_container.setGraphicsEffect(seal_shadow)
        
        seal_layout = QVBoxLayout()
        seal_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        seal_label = QLabel("LTO")
        seal_label.setFont(QFont("Arial", 42, QFont.Weight.Bold))
        seal_label.setStyleSheet("color: #fbbf24; border: none;")
        seal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        seal_layout.addWidget(seal_label)
        seal_container.setLayout(seal_layout)
        
        # Title with gradient effect
        title_container = QFrame()
        title_layout = QVBoxLayout()
        title_layout.setSpacing(10)
        
        title_label = QLabel("LAND TRANSPORTATION OFFICE")
        title_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle_label = QLabel("Vehicle Violation Monitoring System")
        subtitle_label.setFont(QFont("Arial", 15))
        subtitle_label.setStyleSheet("color: #fbbf24;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        title_container.setLayout(title_layout)
        
        # Decorative line
        line = QFrame()
        line.setFixedHeight(3)
        line.setFixedWidth(300)
        line.setStyleSheet("background-color: #fbbf24; border-radius: 2px;")
        
        # Republic and Department info
        republic_label = QLabel("REPUBLIC OF THE PHILIPPINES")
        republic_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        republic_label.setStyleSheet("color: #93c5fd; letter-spacing: 2px;")
        republic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        dept_label = QLabel("DEPARTMENT OF TRANSPORTATION")
        dept_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        dept_label.setStyleSheet("color: #fbbf24;")
        dept_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Bagong Pilipinas badge
        bagong_container = QFrame()
        bagong_container.setFixedSize(200, 60)
        bagong_container.setStyleSheet("""
            QFrame {
                background-color: #dc2626;
                border-radius: 10px;
                border: 2px solid #fbbf24;
            }
        """)
        bagong_layout = QVBoxLayout()
        bagong_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        bagong_label = QLabel("Bagong Pilipinas")
        bagong_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        bagong_label.setStyleSheet("color: white; border: none;")
        bagong_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        bagong_layout.addWidget(bagong_label)
        bagong_container.setLayout(bagong_layout)
        
        # Feature highlights
        features_container = QFrame()
        features_container.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 58, 138, 0.5);
                border-radius: 15px;
                border: 2px solid rgba(251, 191, 36, 0.3);
                padding: 20px;
            }
        """)
        features_layout = QVBoxLayout()
        features_layout.setSpacing(12)
        
        features_title = QLabel("🔐 SECURE ACCESS")
        features_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        features_title.setStyleSheet("color: white; border: none;")
        
        feature1 = QLabel("✓ Real-time Violation Tracking")
        feature1.setFont(QFont("Arial", 11))
        feature1.setStyleSheet("color: #93c5fd; border: none;")
        
        feature2 = QLabel("✓ Centralized Database System")
        feature2.setFont(QFont("Arial", 11))
        feature2.setStyleSheet("color: #93c5fd; border: none;")
        
        feature3 = QLabel("✓ Officer & Citizen Portal")
        feature3.setFont(QFont("Arial", 11))
        feature3.setStyleSheet("color: #93c5fd; border: none;")
        
        features_layout.addWidget(features_title)
        features_layout.addWidget(feature1)
        features_layout.addWidget(feature2)
        features_layout.addWidget(feature3)
        features_container.setLayout(features_layout)
        
        # Add all elements
        left_layout.addWidget(seal_container, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(title_container)
        left_layout.addWidget(line, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addSpacing(15)
        left_layout.addWidget(republic_label)
        left_layout.addWidget(dept_label)
        left_layout.addSpacing(10)
        left_layout.addWidget(bagong_container, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addSpacing(20)
        left_layout.addWidget(features_container)
        left_layout.addStretch()
        
        left_container.setLayout(left_layout)
        return left_container
    
    def create_login_section(self):
        """Create the right login form section"""
        right_container = QWidget()
        right_container.setStyleSheet("background-color: #f1f5f9;")
        
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setSpacing(0)
        
        # Login form container with modern shadow
        form_container = QFrame()
        form_container.setFixedSize(480, 620)
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
        
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(45, 45, 45, 45)
        form_layout.setSpacing(20)
        
        # Login header with icon
        header_container = QFrame()
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        
        icon_label = QLabel("🔐")
        icon_label.setFont(QFont("Arial", 40))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        login_header = QLabel('SYSTEM LOGIN')
        login_header.setFont(QFont('Arial', 28, QFont.Weight.Bold))
        login_header.setStyleSheet("color: #1e3a8a;")
        login_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        welcome_label = QLabel('Access the LTO Monitoring System')
        welcome_label.setFont(QFont('Arial', 12))
        welcome_label.setStyleSheet("color: #64748b;")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(login_header)
        header_layout.addWidget(welcome_label)
        header_container.setLayout(header_layout)
        
        form_layout.addWidget(header_container)
        form_layout.addSpacing(20)
        
        # User Role Selection with icon
        role_container = QFrame()
        role_container.setStyleSheet("""
            QFrame {
                background-color: #f8fafc;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        role_layout = QVBoxLayout()
        role_layout.setSpacing(10)
        
        role_label = QLabel('👤 SELECT YOUR ROLE')
        role_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        role_label.setStyleSheet("color: #1e3a8a; background: transparent;")
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(['Admin', 'Traffic Enforcer', 'Citizen'])
        self.role_combo.setFont(QFont('Arial', 12))
        self.role_combo.setFixedHeight(50)
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
        
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)
        role_container.setLayout(role_layout)
        form_layout.addWidget(role_container)
        
        # Username with modern design
        username_label = QLabel('📧 USERNAME')
        username_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        username_label.setStyleSheet("color: #1e3a8a;")
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setFont(QFont('Arial', 13))
        self.username_input.setFixedHeight(50)
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
        
        # Password with modern design
        password_label = QLabel('🔑 PASSWORD')
        password_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        password_label.setStyleSheet("color: #1e3a8a;")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont('Arial', 13))
        self.password_input.setFixedHeight(50)
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
        
        form_layout.addSpacing(15)
        
        # Modern login button with gradient
        self.login_btn = QPushButton('🚀 LOGIN TO SYSTEM')
        self.login_btn.setFixedHeight(55)
        self.login_btn.setFont(QFont('Arial', 14, QFont.Weight.Bold))
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
        self.login_btn.clicked.connect(self.handle_login)
        
        form_layout.addWidget(self.login_btn)
        
        # Sample credentials with modern card design
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #fef3c7, stop:1 #fef08a);
                border: 2px solid #fbbf24;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)
        
        info_title = QLabel('💡 SAMPLE LOGIN CREDENTIALS')
        info_title.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        info_title.setStyleSheet("color: #92400e; background: transparent; border: none;")
        
        info_text = QLabel(
            '👑 Admin: admin / admin123\n'
            '👮 Enforcer: enforcer1 / enf123\n'
            '👤 Citizen: citizen1 / cit123'
        )
        info_text.setFont(QFont('Arial', 9))
        info_text.setStyleSheet("color: #92400e; background: transparent; border: none;")
        
        info_layout.addWidget(info_title)
        info_layout.addWidget(info_text)
        info_frame.setLayout(info_layout)
        
        form_layout.addWidget(info_frame)
        
        form_container.setLayout(form_layout)
        
        right_layout.addWidget(form_container)
        right_container.setLayout(right_layout)
        
        # Allow Enter key to trigger login
        self.password_input.returnPressed.connect(self.handle_login)
        
        return right_container
        
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        selected_role = self.role_combo.currentText()
        
        # Map display role to database role
        role_mapping = {
            'Admin': 'Admin',
            'Traffic Enforcer': 'Enforcer',
            'Citizen': 'Citizen'
        }
        db_role = role_mapping[selected_role]
        
        if not username or not password:
            self.show_error_message('Input Error', 
                                  '⚠️ Please enter both username and password.')
            return
        
        # Verify credentials
        conn = sqlite3.connect('vehicle_violation.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, full_name, role FROM users 
            WHERE username = ? AND password = ? AND role = ?
        ''', (username, password, db_role))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            user_id, full_name, role = user
            self.show_success_message(full_name, role)
            # Here you would open the main application window
            # self.open_main_window(user_id, full_name, role)
            # self.close()
        else:
            self.show_error_message(
                'Login Failed', 
                '❌ Invalid username, password, or role.\n\nPlease check your credentials and try again.'
            )
            self.password_input.clear()
            self.password_input.setFocus()
    
    def show_success_message(self, full_name, role):
        """Show custom success message"""
        msg = QMessageBox(self)
        msg.setWindowTitle('Login Successful')
        msg.setText(f'✅ Welcome, {full_name}!')
        msg.setInformativeText(f'Role: {role}\n\nYou will now be redirected to the main dashboard.')
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #1e293b;
                font-size: 13px;
            }
            QMessageBox QPushButton {
                background-color: #16a34a;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #15803d;
            }
        """)
        msg.exec()
    
    def show_error_message(self, title, message):
        """Show custom error message"""
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #1e293b;
                font-size: 13px;
            }
            QMessageBox QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        msg.exec()


def main():
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setFont(QFont('Arial', 10))
    
    window = LoginWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
