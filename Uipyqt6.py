import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QFrame, QLineEdit, QScrollArea)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont, QIcon

class StatCard(QFrame):
    """Custom widget for statistics cards"""
    def __init__(self, value, label, icon, color, trend=""):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                border-top: 8px solid {color};
            }}
        """)
        self.setFixedSize(240, 120)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 10)
        
        # Value and Icon row
        top_layout = QHBoxLayout()
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 24))
        icon_label.setFixedSize(45, 45)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"""
            background-color: {color}20;
            border-radius: 10px;
        """)
        
        top_layout.addWidget(value_label)
        top_layout.addStretch()
        top_layout.addWidget(icon_label)
        
        # Label
        label_widget = QLabel(label)
        label_widget.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        label_widget.setStyleSheet("color: #64748b;")
        
        # Trend
        if trend:
            trend_label = QLabel(trend)
            trend_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            trend_label.setStyleSheet("""
                background-color: #fef3c7;
                color: #92400e;
                border-radius: 12px;
                padding: 4px 10px;
            """)
            trend_label.setFixedWidth(80)
        
        layout.addLayout(top_layout)
        layout.addWidget(label_widget)
        if trend:
            layout.addWidget(trend_label)
        layout.addStretch()
        
        self.setLayout(layout)


class LTODashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LTO - Vehicle Violation Monitoring System")
        self.setGeometry(100, 50, 1400, 900)
        
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Content area (sidebar + main content)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        sidebar = self.create_sidebar()
        content_layout.addWidget(sidebar)
        
        # Main content area
        main_content = self.create_main_content()
        content_layout.addWidget(main_content, stretch=1)
        
        main_layout.addLayout(content_layout)
        main_widget.setLayout(main_layout)
        
        # Timer for clock
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
    def create_header(self):
        """Create the header with LTO branding"""
        header = QFrame()
        header.setFixedHeight(98)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e40af, stop:1 #1e3a8a);
                border-bottom: 8px solid #dc2626;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        
        # LTO Logo and Title
        left_layout = QVBoxLayout()
        
        title = QLabel("LAND TRANSPORTATION OFFICE")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        
        subtitle = QLabel("Vehicle Violation Monitoring System")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: #fbbf24;")
        
        left_layout.addWidget(title)
        left_layout.addWidget(subtitle)
        
        # Search Bar
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search Plate Number...")
        search_input.setFixedSize(280, 35)
        search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 13px;
            }
        """)
        
        search_btn = QPushButton("🔍")
        search_btn.setFixedSize(40, 35)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_btn)
        
        # User Info and Logout
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        user_name = QLabel("ADMIN USER")
        user_name.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        user_name.setStyleSheet("color: white;")
        user_name.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        user_dept = QLabel("Traffic Enforcement Division")
        user_dept.setFont(QFont("Arial", 9))
        user_dept.setStyleSheet("color: #fbbf24;")
        user_dept.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        user_office = QLabel("Manila District Office")
        user_office.setFont(QFont("Arial", 9))
        user_office.setStyleSheet("color: #93c5fd;")
        user_office.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        logout_btn = QPushButton("LOGOUT")
        logout_btn.setFixedSize(80, 30)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        
        right_layout.addWidget(user_name)
        right_layout.addWidget(user_dept)
        right_layout.addWidget(user_office)
        right_layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(left_layout)
        layout.addStretch()
        layout.addLayout(search_layout)
        layout.addStretch()
        layout.addLayout(right_layout)
        
        header.setLayout(layout)
        return header
    
    def create_sidebar(self):
        """Create the sidebar navigation"""
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1e3a8a;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 10)
        layout.setSpacing(5)
        
        # LTO Seal
        seal_layout = QVBoxLayout()
        seal_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        seal = QLabel("LTO")
        seal.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        seal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        seal.setFixedSize(70, 70)
        seal.setStyleSheet("""
            background-color: #dc2626;
            color: #fbbf24;
            border-radius: 35px;
            border: 5px solid #1e40af;
        """)
        
        republic = QLabel("REPUBLIC OF THE PHILIPPINES")
        republic.setFont(QFont("Arial", 8, QFont.Weight.Bold))
        republic.setStyleSheet("color: #fbbf24;")
        republic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        seal_layout.addWidget(seal)
        seal_layout.addSpacing(10)
        seal_layout.addWidget(republic)
        
        layout.addLayout(seal_layout)
        layout.addSpacing(20)
        
        # Menu items
        menus = [
            ("MAIN", [("📊 DASHBOARD", True)]),
            ("RECORDS", [("⚠️ Violations", False), ("🚗 Vehicles", False), ("👤 Motorists", False)]),
            ("TRANSACTIONS", [("💰 Payments", False), ("📑 Reports", False)]),
            ("MANAGEMENT", [("👮 Officers", False), ("📋 Violation Types", False), ("⚙️ Settings", False)])
        ]
        
        for section_title, items in menus:
            # Section header
            section_label = QLabel(section_title)
            section_label.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            section_label.setStyleSheet("color: #93c5fd; padding: 10px 5px 5px 5px;")
            layout.addWidget(section_label)
            
            # Menu items
            for item_text, is_active in items:
                btn = QPushButton(item_text)
                btn.setFixedHeight(40)
                if is_active:
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #dc2626;
                            color: white;
                            border: none;
                            border-left: 5px solid #fbbf24;
                            border-radius: 8px;
                            text-align: left;
                            padding-left: 50px;
                            font-size: 14px;
                            font-weight: bold;
                        }
                    """)
                else:
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: transparent;
                            color: white;
                            border: none;
                            border-radius: 8px;
                            text-align: left;
                            padding-left: 50px;
                            font-size: 13px;
                        }
                        QPushButton:hover {
                            background-color: #1e40af;
                        }
                    """)
                layout.addWidget(btn)
        
        layout.addStretch()
        
        # Footer
        footer = QFrame()
        footer.setStyleSheet("""
            background-color: #172554;
            border-radius: 8px;
        """)
        footer.setFixedHeight(60)
        footer_layout = QVBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        dept1 = QLabel("DEPARTMENT OF")
        dept1.setFont(QFont("Arial", 8))
        dept1.setStyleSheet("color: #fbbf24;")
        dept1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        dept2 = QLabel("TRANSPORTATION")
        dept2.setFont(QFont("Arial", 8))
        dept2.setStyleSheet("color: #fbbf24;")
        dept2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        bagong = QLabel("Bagong Pilipinas")
        bagong.setFont(QFont("Arial", 7))
        bagong.setStyleSheet("color: #93c5fd;")
        bagong.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        footer_layout.addWidget(dept1)
        footer_layout.addWidget(dept2)
        footer_layout.addWidget(bagong)
        footer.setLayout(footer_layout)
        
        layout.addWidget(footer)
        
        sidebar.setLayout(layout)
        return sidebar
    
    def create_main_content(self):
        """Create the main content area"""
        main_content = QWidget()
        main_content.setStyleSheet("background-color: #f8fafc;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Statistics Cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        card1 = StatCard("87", "TODAY'S VIOLATIONS", "⚠️", "#dc2626", "+15 New")
        card2 = StatCard("₱342K", "UNPAID FINES", "💰", "#fbbf24", "245 Pending")
        card3 = StatCard("12,547", "REGISTERED VEHICLES", "🚗", "#1e40af", "+128 Today")
        card4 = StatCard("48", "OFFICERS ON DUTY", "👮", "#16a34a", "On Field")
        
        stats_layout.addWidget(card1)
        stats_layout.addWidget(card2)
        stats_layout.addWidget(card3)
        stats_layout.addWidget(card4)
        
        # Main content with table and sidebar
        content_row = QHBoxLayout()
        content_row.setSpacing(15)
        
        # Violations Table
        table_section = self.create_violations_table()
        content_row.addWidget(table_section, stretch=3)
        
        # Right sidebar with actions and alerts
        right_sidebar = self.create_right_sidebar()
        content_row.addWidget(right_sidebar, stretch=1)
        
        layout.addLayout(stats_layout)
        layout.addLayout(content_row)
        
        main_content.setLayout(layout)
        return main_content
    
    def create_violations_table(self):
        """Create the violations table section"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("""
            background-color: #1e40af;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        title = QLabel("RECENT VIOLATIONS RECORD")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        
        add_btn = QPushButton("+ ADD VIOLATION")
        add_btn.setFixedSize(150, 28)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)
        header.setLayout(header_layout)
        
        # Table
        table = QTableWidget()
        table.setColumnCount(6)
        table.setRowCount(7)
        table.setHorizontalHeaderLabels(["PLATE NO.", "VIOLATION", "LOCATION", "DATE", "FINE", "STATUS"])
        
        # Sample data
        data = [
            ("NCR 1234", "Overspeeding", "EDSA-Shaw", "Oct 24, 2025", "₱1,200", "PENDING"),
            ("ABC 7890", "No Helmet", "C5 Road", "Oct 24, 2025", "₱1,500", "OVERDUE"),
            ("XYZ 4567", "Illegal Parking", "Taft Avenue", "Oct 23, 2025", "₱500", "PAID"),
            ("DEF 1122", "Red Light", "Ortigas Ave", "Oct 23, 2025", "₱2,000", "PAID"),
            ("GHI 8899", "No License", "Commonwealth", "Oct 22, 2025", "₱3,000", "PENDING"),
            ("JKL 3344", "Reckless Driving", "Roxas Blvd", "Oct 22, 2025", "₱5,000", "PENDING"),
            ("MNO 5566", "Illegal Turn", "España Blvd", "Oct 21, 2025", "₱800", "PAID"),
        ]
        
        for row, (plate, violation, location, date, fine, status) in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(plate))
            table.setItem(row, 1, QTableWidgetItem(violation))
            table.setItem(row, 2, QTableWidgetItem(location))
            table.setItem(row, 3, QTableWidgetItem(date))
            table.setItem(row, 4, QTableWidgetItem(fine))
            
            status_item = QTableWidgetItem(status)
            if status == "PAID":
                status_item.setBackground(Qt.GlobalColor.green)
            elif status == "OVERDUE":
                status_item.setBackground(Qt.GlobalColor.red)
            else:
                status_item.setBackground(Qt.GlobalColor.yellow)
            table.setItem(row, 5, status_item)
        
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: #e2e8f0;
                background-color: white;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #f1f5f9;
                padding: 10px;
                border: none;
                font-weight: bold;
                color: #1e293b;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #e2e8f0;
            }
        """)
        
        table.horizontalHeader().setStretchLastSection(True)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        layout.addWidget(header)
        layout.addWidget(table)
        
        container.setLayout(layout)
        return container
    
    def create_right_sidebar(self):
        """Create the right sidebar with quick actions and alerts"""
        container = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Quick Actions
        actions_frame = QFrame()
        actions_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
            }
        """)
        actions_layout = QVBoxLayout()
        actions_layout.setContentsMargins(0, 0, 0, 15)
        
        # Header
        actions_header = QFrame()
        actions_header.setFixedHeight(45)
        actions_header.setStyleSheet("""
            background-color: #1e40af;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)
        actions_header_layout = QVBoxLayout()
        actions_header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        actions_title = QLabel("QUICK ACTIONS")
        actions_title.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        actions_title.setStyleSheet("color: white;")
        actions_header_layout.addWidget(actions_title)
        actions_header.setLayout(actions_header_layout)
        
        # Buttons
        btn1 = QPushButton("🚨 RECORD VIOLATION")
        btn1.setFixedHeight(45)
        btn1.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        
        btn2 = QPushButton("💳 PROCESS PAYMENT")
        btn2.setFixedHeight(45)
        btn2.setStyleSheet("""
            QPushButton {
                background-color: #fbbf24;
                color: #1e293b;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f59e0b;
            }
        """)
        
        btn3 = QPushButton("🔍 SEARCH VEHICLE")
        btn3.setFixedHeight(45)
        btn3.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e40af;
                border: 2px solid #1e40af;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dbeafe;
            }
        """)
        
        btn4 = QPushButton("📊 VIEW REPORTS")
        btn4.setFixedHeight(45)
        btn4.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #16a34a;
                border: 2px solid #16a34a;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dcfce7;
            }
        """)
        
        actions_layout.addWidget(actions_header)
        actions_layout.addSpacing(15)
        actions_layout.addWidget(btn1)
        actions_layout.addWidget(btn2)
        actions_layout.addWidget(btn3)
        actions_layout.addWidget(btn4)
        actions_frame.setLayout(actions_layout)
        
        # Alerts Section
        alerts_frame = QFrame()
        alerts_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
            }
        """)
        alerts_layout = QVBoxLayout()
        alerts_layout.setContentsMargins(0, 0, 0, 15)
        
        # Header
        alerts_header = QFrame()
        alerts_header.setFixedHeight(45)
        alerts_header.setStyleSheet("""
            background-color: #dc2626;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)
        alerts_header_layout = QVBoxLayout()
        alerts_header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        alerts_title = QLabel("⚠️ ALERTS")
        alerts_title.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        alerts_title.setStyleSheet("color: white;")
        alerts_header_layout.addWidget(alerts_title)
        alerts_header.setLayout(alerts_header_layout)
        
        # Alert items
        alert1 = QFrame()
        alert1.setStyleSheet("background-color: #fee2e2; border-radius: 8px;")
        alert1.setFixedHeight(50)
        alert1_layout = QVBoxLayout()
        alert1_text1 = QLabel("24 OVERDUE PAYMENTS")
        alert1_text1.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        alert1_text1.setStyleSheet("color: #7f1d1d;")
        alert1_text2 = QLabel("Total: ₱48,500")
        alert1_text2.setFont(QFont("Arial", 9))
        alert1_text2.setStyleSheet("color: #991b1b;")
        alert1_layout.addWidget(alert1_text1)
        alert1_layout.addWidget(alert1_text2)
        alert1.setLayout(alert1_layout)
        
        alert2 = QFrame()
        alert2.setStyleSheet("background-color: #fef3c7; border-radius: 8px;")
        alert2.setFixedHeight(50)
        alert2_layout = QVBoxLayout()
        alert2_text1 = QLabel("87 NEW VIOLATIONS")
        alert2_text1.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        alert2_text1.setStyleSheet("color: #92400e;")
        alert2_text2 = QLabel("Today's records")
        alert2_text2.setFont(QFont("Arial", 9))
        alert2_text2.setStyleSheet("color: #92400e;")
        alert2_layout.addWidget(alert2_text1)
        alert2_layout.addWidget(alert2_text2)
        alert2.setLayout(alert2_layout)
        
        alert3 = QFrame()
        alert3.setStyleSheet("background-color: #dbeafe; border-radius: 8px;")
        alert3.setFixedHeight(50)
        alert3_layout = QVBoxLayout()
        alert3_text1 = QLabel("5 OFFICERS OFFLINE")
        alert3_text1.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        alert3_text1.setStyleSheet("color: #1e3a8a;")
        alert3_text2 = QLabel("Check status")
        alert3_text2.setFont(QFont("Arial", 9))
        alert3_text2.setStyleSheet("color: #1e40af;")
        alert3_layout.addWidget(alert3_text1)
        alert3_layout.addWidget(alert3_text2)
        alert3.setLayout(alert3_layout)
        
        alerts_layout.addWidget(alerts_header)
        alerts_layout.addSpacing(15)
        alerts_layout.addWidget(alert1)
        alerts_layout.addWidget(alert2)
        alerts_layout.addWidget(alert3)
        alerts_frame.setLayout(alerts_layout)
        
        # Date and Time
        datetime_layout = QHBoxLayout()
        
        self.date_label = QLabel()
        self.date_label.setFixedHeight(30)
        self.date_label.setStyleSheet("""
            background-color: #1e3a8a;
            color: white;
            border-radius: 6px;
            padding: 5px 10px;
            font-size: 12px;
            font-weight: bold;
        """)
        
        self.time_label = QLabel()
        self.time_label.setFixedHeight(30)
        self.time_label.setStyleSheet("""
            background-color: #1e293b;
            color: #fbbf24;
            border-radius: 6px;
            padding: 5px 10px;
            font-size: 14px;
            font-weight: bold;
        """)
        
        datetime_layout.addWidget(self.date_label)
        datetime_layout.addWidget(self.time_label)
        
        layout.addWidget(actions_frame)
        layout.addWidget(alerts_frame)
        layout.addLayout(datetime_layout)
        layout.addStretch()
        
        container.setLayout(layout)
        return container
    
    def update_time(self):
        """Update the time display"""
        current = QDateTime.currentDateTime()
        self.date_label.setText(current.toString("MMM dd, yyyy"))
        self.time_label.setText(current.toString("h:mm AP"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LTODashboard()
    window.show()
    sys.exit(app.exec())