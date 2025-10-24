import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QComboBox, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
import sqlite3


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_database()
        
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
                ('enforcer1', 'enf123', 'Enforcer', 'Juan Dela Cruz'),
                ('citizen1', 'cit123', 'Citizen', 'Maria Santos')
            ]
            cursor.executemany(
                'INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)',
                sample_users
            )
        
        conn.commit()
        conn.close()
        
    def init_ui(self):
        self.setWindowTitle('LTO - Vehicle Violation Monitoring System - Login')
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e3a8a, stop:1 #1e40af);")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left side - Branding
        left_container = QFrame()
        left_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3a8a, stop:1 #1e40af);
                border-right: 3px solid #dc2626;
            }
        """)
        left_container.setFixedWidth(450)
        
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.setSpacing(30)
        
        # LTO Seal
        seal_container = QFrame()
        seal_container.setFixedSize(150, 150)
        seal_container.setStyleSheet("""
            QFrame {
                background-color: #dc2626;
                border-radius: 75px;
                border: 8px solid #fbbf24;
            }
        """)
        seal_layout = QVBoxLayout()
        seal_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        seal_label = QLabel("LTO")
        seal_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        seal_label.setStyleSheet("color: #fbbf24;")
        seal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        seal_layout.addWidget(seal_label)
        seal_container.setLayout(seal_layout)
        
        # Title
        title_label = QLabel("LAND TRANSPORTATION\nOFFICE")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle_label = QLabel("Vehicle Violation Monitoring System")
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setStyleSheet("color: #fbbf24;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Republic text
        republic_label = QLabel("REPUBLIC OF THE PHILIPPINES")
        republic_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        republic_label.setStyleSheet("color: #93c5fd;")
        republic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Department
        dept_label = QLabel("DEPARTMENT OF TRANSPORTATION")
        dept_label.setFont(QFont("Arial", 10))
        dept_label.setStyleSheet("color: #fbbf24;")
        dept_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Bagong Pilipinas
        bagong_label = QLabel("Bagong Pilipinas")
        bagong_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        bagong_label.setStyleSheet("color: white;")
        bagong_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        left_layout.addWidget(seal_container)
        left_layout.addWidget(title_label)
        left_layout.addWidget(subtitle_label)
        left_layout.addSpacing(20)
        left_layout.addWidget(republic_label)
        left_layout.addWidget(dept_label)
        left_layout.addWidget(bagong_label)
        left_layout.addStretch()
        
        left_container.setLayout(left_layout)
        
        # Right side - Login Form
        right_container = QWidget()
        right_container.setStyleSheet("background-color: #f8fafc;")
        
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setSpacing(0)
        
        # Login form container with shadow
        form_container = QFrame()
        form_container.setFixedSize(400, 500)
        form_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 2px solid #e2e8f0;
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 5)
        form_container.setGraphicsEffect(shadow)
        
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(25)
        
        # Login header
        login_header = QLabel('System Login')
        login_header.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        login_header.setStyleSheet("color: #1e3a8a;")
        login_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(login_header)
        
        welcome_label = QLabel('Welcome to LTO Monitoring System')
        welcome_label.setFont(QFont('Arial', 12))
        welcome_label.setStyleSheet("color: #64748b;")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(welcome_label)
        
        form_layout.addSpacing(10)
        
        # User Role Selection
        role_label = QLabel('SELECT ROLE:')
        role_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        role_label.setStyleSheet("color: #374151;")
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(['Traffic Enforcer', 'Citizen', 'Admin'])
        self.role_combo.setFont(QFont('Arial', 11))
        self.role_combo.setFixedHeight(45)
        self.role_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 15px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
                font-size: 13px;
            }
            QComboBox:focus {
                border: 2px solid #1e40af;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #1e40af;
                selection-color: white;
            }
        """)
        
        form_layout.addWidget(role_label)
        form_layout.addWidget(self.role_combo)
        
        # Username
        username_label = QLabel('USERNAME:')
        username_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        username_label.setStyleSheet("color: #374151;")
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setFont(QFont('Arial', 12))
        self.username_input.setFixedHeight(45)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #1e40af;
            }
        """)
        
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel('PASSWORD:')
        password_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        password_label.setStyleSheet("color: #374151;")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont('Arial', 12))
        self.password_input.setFixedHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #1e40af;
            }
        """)
        
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        
        form_layout.addSpacing(10)
        
        # Login button with hover effects
        self.login_btn = QPushButton('LOGIN TO SYSTEM')
        self.login_btn.setFixedHeight(50)
        self.login_btn.setFont(QFont('Arial', 13, QFont.Weight.Bold))
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
            QPushButton:pressed {
                background-color: #991b1b;
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)
        
        form_layout.addWidget(self.login_btn)
        
        # Sample credentials info
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #fef3c7;
                border: 1px solid #fbbf24;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout()
        
        info_title = QLabel('Sample Login Credentials:')
        info_title.setFont(QFont('Arial', 9, QFont.Weight.Bold))
        info_title.setStyleSheet("color: #92400e;")
        
        info_text = QLabel('Admin: admin / admin123\nEnforcer: enforcer1 / enf123\nCitizen: citizen1 / cit123')
        info_text.setFont(QFont('Arial', 8))
        info_text.setStyleSheet("color: #92400e;")
        
        info_layout.addWidget(info_title)
        info_layout.addWidget(info_text)
        info_frame.setLayout(info_layout)
        
        form_layout.addWidget(info_frame)
        
        form_container.setLayout(form_layout)
        
        right_layout.addWidget(form_container)
        right_container.setLayout(right_layout)
        
        # Add both sides to main layout
        main_layout.addWidget(left_container)
        main_layout.addWidget(right_container, stretch=1)
        
        central_widget.setLayout(main_layout)
        
        # Allow Enter key to trigger login
        self.password_input.returnPressed.connect(self.handle_login)
        
        # Set focus to username
        self.username_input.setFocus()
        
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
            QMessageBox.warning(self, 'Input Error', 
                              'Please enter both username and password.')
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
            QMessageBox.information(
                self, 
                'Login Successful', 
                f'Welcome, {full_name}!\nRole: {role}\n\nYou will now be redirected to the main dashboard.'
            )
            # Here you would open the main application window
            # self.open_main_window(user_id, full_name, role)
            # self.close()
        else:
            QMessageBox.critical(
                self, 
                'Login Failed', 
                'Invalid username, password, or role.\nPlease try again.'
            )
            self.password_input.clear()
            self.password_input.setFocus()


def main():
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setFont(QFont('Arial', 10))
    
    window = LoginWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()