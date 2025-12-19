import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QFrame, QLineEdit, QScrollArea, 
                             QHeaderView, QGraphicsDropShadowEffect, QStackedWidget, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QColor

# --- HELPER FUNCTIONS ---
def hex_to_rgba(hex_color, alpha=0.2):
    color = QColor(hex_color)
    return f"rgba({color.red()}, {color.green()}, {color.blue()}, {alpha})"

def apply_shadow(widget, blur_radius=15, x_offset=0, y_offset=4, alpha=30):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur_radius)
    shadow.setXOffset(x_offset)
    shadow.setYOffset(y_offset)
    shadow.setColor(QColor(0, 0, 0, alpha)) 
    widget.setGraphicsEffect(shadow)

class StatCard(QFrame):
    def __init__(self, value, label, icon, color, trend=""):
        super().__init__()
        self.setFixedSize(240, 130)
        self.setObjectName("MainStatCard")
        
        self.setStyleSheet(f"""
            QFrame#MainStatCard {{
                background-color: white;
                border-radius: 12px;
                border-top: 5px solid {color};
                border-bottom: 1px solid #f1f5f9;
                border-left: 1px solid #f1f5f9;
                border-right: 1px solid #f1f5f9;
            }}
            QFrame#MainStatCard:hover {{
                background-color: #fafafa;
                border-top: 5px solid {color};
            }}
        """)
        
        apply_shadow(self)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 10)
        layout.setSpacing(5)
        
        top_layout = QHBoxLayout()
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color}; background-color: transparent;")
        
        rgba_bg = hex_to_rgba(color, 0.15)
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 28))
        icon_label.setFixedSize(50, 50)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"""
            background-color: {rgba_bg};
            border-radius: 10px;
        """)
        
        top_layout.addWidget(value_label)
        top_layout.addStretch()
        top_layout.addWidget(icon_label)
        
        label_widget = QLabel(label)
        label_widget.setFont(QFont("Arial", 11))
        label_widget.setStyleSheet("color: #64748b; background-color: transparent;")
        
        layout.addLayout(top_layout)
        layout.addWidget(label_widget)
        
        if trend:
            trend_label = QLabel(trend)
            trend_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            trend_label.setFixedWidth(80)
            trend_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            if "+" in trend:
                trend_label.setStyleSheet("background-color: #fef3c7; color: #92400e; border-radius: 10px; padding: 4px;")
            else:
                trend_label.setStyleSheet("background-color: #fee2e2; color: #7f1d1d; border-radius: 10px; padding: 4px;")
            layout.addWidget(trend_label)
            
        layout.addStretch()
        self.setLayout(layout)

# CHANGED: Inherit from QWidget
class AdminDashboard(QWidget):
    def __init__(self, user_name="ADMIN USER", user_dept="Administration", user_office="Davao District Office"):
        super().__init__()
        self.user_name = user_name
        self.user_dept = user_dept
        self.user_office = user_office
        # These will be populated by main.py
        self.db_manager = None 
        self.current_user = None
        
        self.init_ui()
        
    def init_ui(self):
        # Removed setGeometry/setCentralWidget logic
        
        # Store all logout buttons for connection
        self.logout_buttons = []
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        

        # Content Area (Stacked)
        self.stack = QStackedWidget()
        
        # 1. Dashboard Page
        self.dashboard_page = self.create_dashboard_page()
        self.stack.addWidget(self.dashboard_page)
        
        # 2. User Management Page
        self.user_page = self.create_user_page()
        self.stack.addWidget(self.user_page)
        
        # 3. Vehicle Management Page
        self.vehicle_page = self.create_vehicle_page()
        self.stack.addWidget(self.vehicle_page)
        
        main_layout.addWidget(self.stack, stretch=1)
        
        # Apply layout to self
        self.setLayout(main_layout)
        
        # Set main logout_btn reference (for compatibility)
        if self.logout_buttons:
            self.logout_btn = self.logout_buttons[0]

    def show_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_page)
        self.btn_dashboard.setStyleSheet(self.get_sidebar_style(True))
        self.btn_manage_users.setStyleSheet(self.get_sidebar_style(False))
        self.btn_manage_vehicles.setStyleSheet(self.get_sidebar_style(False))
        # Refresh stats when showing dashboard
        if self.db_manager: self.update_stats()

    def show_users(self):
        self.stack.setCurrentWidget(self.user_page)
        self.btn_dashboard.setStyleSheet(self.get_sidebar_style(False))
        self.btn_manage_users.setStyleSheet(self.get_sidebar_style(True))
        self.btn_manage_vehicles.setStyleSheet(self.get_sidebar_style(False))
        if self.db_manager: self.refresh_user_table()

    def show_vehicles(self):
        self.stack.setCurrentWidget(self.vehicle_page)
        self.btn_dashboard.setStyleSheet(self.get_sidebar_style(False))
        self.btn_manage_users.setStyleSheet(self.get_sidebar_style(False))
        self.btn_manage_vehicles.setStyleSheet(self.get_sidebar_style(True))
        if self.db_manager: self.refresh_vehicle_table()
        
    def get_sidebar_style(self, active):
        if active:
            return "background-color: #dc2626; color: white; border: none; text-align: left; padding-left: 20px; font-size: 13px; font-weight: bold;"
        return "background-color: transparent; color: white; border: none; text-align: left; padding-left: 20px; font-size: 13px;"

        
    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(235)
        sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e40af, stop:0.5 #1e3a8a, stop:1 #172554);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # --- LOGO SECTION ---
        logo_section = QFrame()
        logo_section.setFixedHeight(180)
        logo_section.setStyleSheet("background-color: transparent;")
        
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.setSpacing(8)
        logo_layout.setContentsMargins(0, 20, 0, 0)
        
        logo_image = QLabel()
        try:
            logo_pixmap = QPixmap("images/cropped_circle_image(1).png")
            logo_image.setPixmap(logo_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        except:
            logo_image.setText("🔍")
            logo_image.setFont(QFont("Arial", 40))
        logo_image.setStyleSheet("background: transparent;")
        logo_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        brand_name = QLabel("Nexus Monitor")
        brand_name.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        brand_name.setStyleSheet("color: #fbbf24; background: transparent;")
        brand_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo_layout.addWidget(logo_image)
        logo_layout.addWidget(brand_name)
        logo_section.setLayout(logo_layout)
        layout.addWidget(logo_section)
        
        # --- SIDEBAR MENU ---
        layout.addWidget(self.create_section_label("MAIN"))
        self.btn_dashboard = self.create_sidebar_btn("🏠 DASHBOARD", active=True)
        layout.addWidget(self.btn_dashboard)

        layout.addWidget(self.create_section_label("ADMIN FUNCTIONS"))
        self.btn_manage_users = self.create_sidebar_btn("👥 Manage Users")
        self.btn_manage_vehicles = self.create_sidebar_btn("🚗 Manage Vehicle Info")
        self.btn_manage_types = self.create_sidebar_btn("⚠️ Violation Types")
        self.btn_view_all_violations = self.create_sidebar_btn("👁️ View All Violations")
        
        layout.addWidget(self.btn_manage_users)
        layout.addWidget(self.btn_manage_vehicles)
        layout.addWidget(self.btn_manage_types)
        layout.addWidget(self.btn_view_all_violations)

        layout.addWidget(self.create_section_label("REPORTS & STATS"))
        self.btn_reports = self.create_sidebar_btn("📑 Generate Reports")
        layout.addWidget(self.btn_reports)
        
        layout.addStretch()
        sidebar.setLayout(layout)
        return sidebar

    def create_section_label(self, text):
        label = QLabel(text)
        label.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        label.setStyleSheet("color: #93c5fd; padding: 15px 15px 5px 15px; background: transparent;")
        return label

    def create_sidebar_btn(self, text, active=False):
        btn = QPushButton(text)
        btn.setFixedHeight(45)
        if active:
            btn.setStyleSheet("""
                QPushButton { background-color: #dc2626; color: white; border: none; text-align: left; padding-left: 20px; font-size: 13px; font-weight: bold; }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton { background-color: transparent; color: white; border: none; text-align: left; padding-left: 20px; font-size: 13px; }
                QPushButton:hover { background-color: #1e40af; }
            """)
        return btn
        
    # Renamed from create_main_content
    def create_dashboard_page(self):
        content = QWidget()
        content.setStyleSheet("background-color: #f1f5f9;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        header = self.create_header("Dashboard")
        layout.addWidget(header)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: #f1f5f9;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(20)
        
        # 1. Statistics Cards
        stats_row = self.create_stats_cards()
        scroll_layout.addLayout(stats_row)
        
        # 2. Main Admin Actions
        actions_row = QHBoxLayout()
        actions_row.setSpacing(20)
        
        shortcuts_card = self.create_shortcuts_card()
        actions_row.addWidget(shortcuts_card, stretch=2)
        
        alert_card = self.create_alert_card()
        actions_row.addWidget(alert_card, stretch=1)
        
        scroll_layout.addLayout(actions_row)
        
        # 3. Violation Management Table (Quick View)
        violation_table = self.create_violation_management()
        scroll_layout.addWidget(violation_table)
        
        # 4. Vehicle Expiration Tracking
        expiration_section = self.create_vehicle_expiration_section()
        scroll_layout.addWidget(expiration_section)
        
        scroll_layout.addStretch()
        
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        
        layout.addWidget(scroll)
        content.setLayout(layout)
        return content

    def create_user_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: #f1f5f9;")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        layout.addWidget(self.create_header("User Management"))
        
        body_layout = QVBoxLayout()
        body_layout.setContentsMargins(20, 20, 20, 20)
        
        # Top Bar
        top_bar = QHBoxLayout()
        self.btn_add_user_page = self.create_action_button("➕ Add New User", "#1e40af")
        self.btn_add_user_page.setFixedSize(150, 40)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_add_user_page)
        body_layout.addLayout(top_bar)
        
        # Table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(6)
        self.user_table.setHorizontalHeaderLabels(["ID", "Name", "Role", "Department", "Office", "Actions"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.user_table.setStyleSheet("background-color: white; border-radius: 8px;")
        body_layout.addWidget(self.user_table)
        
        layout.addLayout(body_layout)
        page.setLayout(layout)
        return page

    def create_vehicle_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: #f1f5f9;")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        layout.addWidget(self.create_header("Vehicle Management"))
        
        body_layout = QVBoxLayout()
        body_layout.setContentsMargins(20, 20, 20, 20)
        
        # Top Bar
        top_bar = QHBoxLayout()
        self.btn_add_vehicle_page = self.create_action_button("➕ Add New Vehicle", "#1e40af")
        self.btn_add_vehicle_page.setFixedSize(160, 40)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_add_vehicle_page)
        body_layout.addLayout(top_bar)
        
        # Top Bar - Add refresh expiration button
        top_bar_actions = QHBoxLayout()
        self.btn_refresh_expiration = self.create_action_button("🔄 Check Expiration", "#059669")
        self.btn_refresh_expiration.setFixedSize(160, 40)
        top_bar_actions.addWidget(self.btn_refresh_expiration)
        top_bar_actions.addStretch()
        body_layout.addLayout(top_bar_actions)
        
        # Table
        self.vehicle_table = QTableWidget()
        self.vehicle_table.setColumnCount(8)
        self.vehicle_table.setHorizontalHeaderLabels(["Plate", "Owner", "Make/Model", "Year", "Color", "Expiry Date", "Status", "Actions"])
        self.vehicle_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.vehicle_table.setStyleSheet("background-color: white; border-radius: 8px;")
        body_layout.addWidget(self.vehicle_table)
        
        layout.addLayout(body_layout)
        page.setLayout(layout)
        return page

        
    def create_header(self, title_text="Dashboard"):
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("QFrame { background-color: #1e40af; border-bottom: 3px solid #fbbf24; }")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 40, 10) 
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        
        title = QLabel("LAND TRANSPORTATION OFFICE")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background-color: transparent; border: none;")
        
        subtitle = QLabel(title_text)
        subtitle.setFont(QFont("Arial", 11))
        subtitle.setStyleSheet("color: #fbbf24; background-color: transparent; border: none;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        user_layout = QVBoxLayout()
        user_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        user_layout.setSpacing(2)
        
        user_name = QLabel(self.user_name)
        user_name.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        user_name.setStyleSheet("color: white; background-color: transparent; border: none;")
        user_name.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        user_dept = QLabel(self.user_dept)
        user_dept.setFont(QFont("Arial", 9))
        user_dept.setStyleSheet("color: #fbbf24; background-color: transparent; border: none;")
        user_dept.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        logout_btn = QPushButton("LOGOUT")
        logout_btn.setFixedSize(80, 28)
        logout_btn.setStyleSheet("""
            QPushButton { background-color: #dc2626; color: white; border: none; border-radius: 5px; font-size: 11px; font-weight: bold; }
            QPushButton:hover { background-color: #b91c1c; }
        """)
        
        # Store all logout buttons for connection
        self.logout_buttons.append(logout_btn)
        
        user_layout.addWidget(user_name)
        user_layout.addWidget(user_dept)
        user_layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addLayout(user_layout)
        
        header.setLayout(layout)
        return header
        
    def create_stats_cards(self):
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        self.card_users = StatCard("...", "TOTAL USERS", "👥", "#dc2626")
        self.card_vehicles = StatCard("...", "REGISTERED VEHICLES", "🚗", "#1e40af")
        self.card_violations = StatCard("...", "TOTAL VIOLATIONS", "⚠️", "#f59e0b")
        self.card_fines = StatCard("...", "COLLECTED FINES", "💰", "#16a34a")
        
        stats_layout.addWidget(self.card_users)
        stats_layout.addWidget(self.card_vehicles)
        stats_layout.addWidget(self.card_violations)
        stats_layout.addWidget(self.card_fines)
        
        return stats_layout

    def create_shortcuts_card(self):
        container = QFrame()
        apply_shadow(container)
        container.setStyleSheet("QFrame { background-color: white; border-radius: 12px; }")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("ADMIN QUICK ACTIONS")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e40af; background: transparent;")
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        self.btn_add_user = self.create_action_button("➕ Add User", "#1e40af")
        self.btn_add_vehicle = self.create_action_button("➕ Add Vehicle", "#1e40af")
        self.btn_add_type = self.create_action_button("⚠️ Add Violation Type", "#f59e0b")
        
        btn_layout.addWidget(self.btn_add_user)
        btn_layout.addWidget(self.btn_add_vehicle)
        btn_layout.addWidget(self.btn_add_type)
        
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addLayout(btn_layout)
        container.setLayout(layout)
        return container

    def create_alert_card(self):
        container = QFrame()
        apply_shadow(container)
        container.setStyleSheet("QFrame { background-color: white; border-radius: 12px; }")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("SYSTEM STATUS")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #dc2626; background: transparent;")
        
        status_label = QLabel("🟢 System Online")
        status_label.setStyleSheet("color: green; font-weight: bold; font-size: 14px;")
        
        db_label = QLabel("🗄️ Database: Connected")
        db_label.setStyleSheet("color: #64748b;")
        
        layout.addWidget(title)
        layout.addWidget(status_label)
        layout.addWidget(db_label)
        layout.addStretch()
        container.setLayout(layout)
        return container

    def create_action_button(self, text, color):
        btn = QPushButton(text)
        btn.setFixedHeight(45)
        btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        btn.setStyleSheet(f"""
            QPushButton {{ background-color: {color}; color: white; border: none; border-radius: 8px; }}
            QPushButton:hover {{ background-color: {color}dd; }}
        """)
        return btn
        
    def create_violation_management(self):
        container = QFrame()
        apply_shadow(container)
        container.setStyleSheet("QFrame { background-color: white; border-radius: 12px; }")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 15)
        layout.setSpacing(0)
        
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("background-color: #1e40af; border-top-left-radius: 12px; border-top-right-radius: 12px;")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        title = QLabel("VIOLATION MANAGEMENT")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background-color: transparent; border: none;")
        
        header_layout.addWidget(title)
        header.setLayout(header_layout)
        
        self.violation_table = QTableWidget()
        self.violation_table.setColumnCount(7) 
        self.violation_table.verticalHeader().setVisible(False)
        self.violation_table.setHorizontalHeaderLabels([
            "CITATION NO.", "PLATE NO.", "VIOLATION", "LOCATION", "DATE", "FINE", "STATUS"
        ])
        
        self.violation_table.setMinimumHeight(300)
        self.violation_table.setStyleSheet("""
            QTableWidget { border: none; gridline-color: transparent; background-color: white; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px; }
            QHeaderView::section { background-color: #f8fafc; padding: 12px; border: none; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #475569; }
            QTableWidget::item { border-bottom: 1px solid #f1f5f9; padding: 5px; color: #334155; }
        """)
        self.violation_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Citation
        self.violation_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # Plate
        self.violation_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # Violation
        self.violation_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) # Location
        self.violation_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # Date
        self.violation_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) # Fine
        self.violation_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents) # Status
        self.violation_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        layout.addWidget(header)
        layout.addWidget(self.violation_table)
        
        container.setLayout(layout)
        return container

    def create_vehicle_expiration_section(self):
        container = QFrame()
        apply_shadow(container)
        container.setStyleSheet("QFrame { background-color: white; border-radius: 12px; }")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 15)
        layout.setSpacing(0)
        
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("background-color: #f8fafc; border-top-left-radius: 12px; border-top-right-radius: 12px;")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        title = QLabel("🚗 VEHICLE EXPIRATION TRACKING")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e40af; background: transparent;")
        
        self.btn_refresh_exp_dashboard = QPushButton("🔄 Refresh")
        self.btn_refresh_exp_dashboard.setFixedSize(100, 35)
        self.btn_refresh_exp_dashboard.setStyleSheet("""
            QPushButton { background-color: #059669; color: white; border: none; border-radius: 6px; font-weight: bold; }
            QPushButton:hover { background-color: #047857; }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_refresh_exp_dashboard)
        header.setLayout(header_layout)
        
        # Content area with tabs for expired and expiring
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Stats row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(15)
        
        self.expired_count_label = QLabel("0")
        self.expired_count_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.expired_count_label.setStyleSheet("color: #dc2626;")
        expired_card = QFrame()
        expired_card.setStyleSheet("QFrame { background-color: #fef2f2; border-radius: 8px; padding: 15px; }")
        expired_layout = QVBoxLayout()
        expired_layout.addWidget(QLabel("Expired"))
        expired_layout.addWidget(self.expired_count_label)
        expired_card.setLayout(expired_layout)
        
        self.expiring_count_label = QLabel("0")
        self.expiring_count_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.expiring_count_label.setStyleSheet("color: #f59e0b;")
        expiring_card = QFrame()
        expiring_card.setStyleSheet("QFrame { background-color: #fffbeb; border-radius: 8px; padding: 15px; }")
        expiring_layout = QVBoxLayout()
        expiring_layout.addWidget(QLabel("Expiring Soon (30 days)"))
        expiring_layout.addWidget(self.expiring_count_label)
        expiring_card.setLayout(expiring_layout)
        
        stats_row.addWidget(expired_card)
        stats_row.addWidget(expiring_card)
        stats_row.addStretch()
        content_layout.addLayout(stats_row)
        
        # Tables for expired and expiring vehicles
        tabs_widget = QWidget()
        tabs_layout = QVBoxLayout()
        tabs_layout.setContentsMargins(0, 0, 0, 0)
        
        # Expired vehicles table
        expired_label = QLabel("Expired Vehicles:")
        expired_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        expired_label.setStyleSheet("color: #dc2626; margin-top: 10px;")
        tabs_layout.addWidget(expired_label)
        
        self.expired_vehicles_table = QTableWidget()
        self.expired_vehicles_table.setColumnCount(6)
        self.expired_vehicles_table.setHorizontalHeaderLabels(["Plate", "Owner", "Make/Model", "Expiry Date", "Days Overdue", "Actions"])
        self.expired_vehicles_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.expired_vehicles_table.setMaximumHeight(200)
        tabs_layout.addWidget(self.expired_vehicles_table)
        
        # Expiring vehicles table
        expiring_label = QLabel("Expiring Soon (within 30 days):")
        expiring_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        expiring_label.setStyleSheet("color: #f59e0b; margin-top: 10px;")
        tabs_layout.addWidget(expiring_label)
        
        self.expiring_vehicles_table = QTableWidget()
        self.expiring_vehicles_table.setColumnCount(6)
        self.expiring_vehicles_table.setHorizontalHeaderLabels(["Plate", "Owner", "Make/Model", "Expiry Date", "Days Remaining", "Actions"])
        self.expiring_vehicles_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.expiring_vehicles_table.setMaximumHeight(200)
        tabs_layout.addWidget(self.expiring_vehicles_table)
        
        tabs_widget.setLayout(tabs_layout)
        content_layout.addWidget(tabs_widget)
        
        content_widget.setLayout(content_layout)
        
        layout.addWidget(header)
        layout.addWidget(content_widget)
        
        container.setLayout(layout)
        return container

    # --- POPULATE FUNCTIONS ---
    def populate_violation_table(self, violations):
        self.violation_table.setRowCount(0)
        for row, v in enumerate(violations):
            self.violation_table.insertRow(row)
            
            citation = str(v.get('citation_number', 'N/A'))
            self.violation_table.setItem(row, 0, QTableWidgetItem(citation))
            self.violation_table.setItem(row, 1, QTableWidgetItem(v['plate_number']))
            self.violation_table.setItem(row, 2, QTableWidgetItem(v['violation_name']))
            self.violation_table.setItem(row, 3, QTableWidgetItem(v['location']))
            self.violation_table.setItem(row, 4, QTableWidgetItem(str(v['violation_date'])))
            self.violation_table.setItem(row, 5, QTableWidgetItem(f"₱{v['fine_amount']:,.2f}"))
            
            status_item = QTableWidgetItem(v['status'].upper())
            if v['status'] == 'paid':
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            elif v['status'] == 'overdue':
                status_item.setForeground(Qt.GlobalColor.red)
            
            self.violation_table.setItem(row, 6, status_item)

    def update_stats(self):
        if not self.db_manager: return
        stats = self.db_manager.get_dashboard_stats()
        
        self.card_users.findChild(QLabel).setText(str(stats['users']))
        self.card_vehicles.findChild(QLabel).setText(str(stats['vehicles']))
        self.card_violations.findChild(QLabel).setText(str(stats['violations']))
        self.card_fines.findChild(QLabel).setText(f"₱{stats['fines']:,.0f}")
        
        # Update expiration tracking
        self.refresh_expiration_tracking()
    
    def refresh_expiration_tracking(self):
        """Refresh the vehicle expiration tracking section"""
        if not self.db_manager: return
        if not hasattr(self, 'expired_vehicles_table'): return
        
        # Check and update expiration status
        self.db_manager.check_and_update_vehicle_expiration()
        
        # Get expired and expiring vehicles
        expired = self.db_manager.get_expired_vehicles()
        expiring = self.db_manager.get_expiring_vehicles(30)
        
        # Update counts
        if hasattr(self, 'expired_count_label'):
            self.expired_count_label.setText(str(len(expired)))
        if hasattr(self, 'expiring_count_label'):
            self.expiring_count_label.setText(str(len(expiring)))
        
        # Populate expired table
        self.expired_vehicles_table.setRowCount(0)
        from datetime import date
        today = date.today()
        
        for row, v in enumerate(expired):
            self.expired_vehicles_table.insertRow(row)
            self.expired_vehicles_table.setItem(row, 0, QTableWidgetItem(v['plate_number']))
            self.expired_vehicles_table.setItem(row, 1, QTableWidgetItem(v['owner_name']))
            self.expired_vehicles_table.setItem(row, 2, QTableWidgetItem(f"{v['make']} {v['model']}"))
            self.expired_vehicles_table.setItem(row, 3, QTableWidgetItem(str(v['expiry_date'])))
            
            # Calculate days overdue
            if v['expiry_date']:
                days_overdue = (today - v['expiry_date']).days
                overdue_item = QTableWidgetItem(f"{days_overdue} days")
                overdue_item.setForeground(QColor('#dc2626'))
                self.expired_vehicles_table.setItem(row, 4, overdue_item)
            else:
                self.expired_vehicles_table.setItem(row, 4, QTableWidgetItem("N/A"))
            
            # Action button
            action_btn = QPushButton("✏️ Edit Date")
            action_btn.setFixedSize(100, 30)
            action_btn.setStyleSheet("background-color: #f59e0b; color: white; border-radius: 4px; font-weight: bold;")
            action_btn.clicked.connect(lambda checked, veh=v: self.edit_vehicle_callback(veh))
            self.expired_vehicles_table.setCellWidget(row, 5, action_btn)
        
        # Populate expiring table
        self.expiring_vehicles_table.setRowCount(0)
        for row, v in enumerate(expiring):
            self.expiring_vehicles_table.insertRow(row)
            self.expiring_vehicles_table.setItem(row, 0, QTableWidgetItem(v['plate_number']))
            self.expiring_vehicles_table.setItem(row, 1, QTableWidgetItem(v['owner_name']))
            self.expiring_vehicles_table.setItem(row, 2, QTableWidgetItem(f"{v['make']} {v['model']}"))
            self.expiring_vehicles_table.setItem(row, 3, QTableWidgetItem(str(v['expiry_date'])))
            
            # Calculate days remaining
            if v['expiry_date']:
                days_remaining = (v['expiry_date'] - today).days
                remaining_item = QTableWidgetItem(f"{days_remaining} days")
                remaining_item.setForeground(QColor('#f59e0b'))
                self.expiring_vehicles_table.setItem(row, 4, remaining_item)
            else:
                self.expiring_vehicles_table.setItem(row, 4, QTableWidgetItem("N/A"))
            
            # Action button
            action_btn = QPushButton("✏️ Edit Date")
            action_btn.setFixedSize(100, 30)
            action_btn.setStyleSheet("background-color: #f59e0b; color: white; border-radius: 4px; font-weight: bold;")
            action_btn.clicked.connect(lambda checked, veh=v: self.edit_vehicle_callback(veh))
            self.expiring_vehicles_table.setCellWidget(row, 5, action_btn)

    def refresh_user_table(self):
        if not self.db_manager: return
        users = self.db_manager.get_all_users()
        self.user_table.setRowCount(0)
        for row, u in enumerate(users):
            self.user_table.insertRow(row)
            self.user_table.setItem(row, 0, QTableWidgetItem(str(u['user_id'])))
            self.user_table.setItem(row, 1, QTableWidgetItem(u['full_name']))
            self.user_table.setItem(row, 2, QTableWidgetItem(u['role'].upper()))
            self.user_table.setItem(row, 3, QTableWidgetItem(u.get('department') or '-'))
            self.user_table.setItem(row, 4, QTableWidgetItem(u.get('office_location') or '-'))
            
            # Actions
            btn_widget = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(2, 2, 2, 2)
            btn_layout.setSpacing(5)
            
            # REMOVED EDIT BUTTON
            
            del_btn = QPushButton("🗑️")
            del_btn.setFixedSize(30, 30)
            del_btn.setStyleSheet("background-color: #dc2626; color: white; border-radius: 4px;")
            del_btn.clicked.connect(lambda checked, uid=u['user_id']: self.delete_user_callback(uid))
            
            btn_layout.addWidget(del_btn)
            btn_layout.addStretch()
            btn_widget.setLayout(btn_layout)
            self.user_table.setCellWidget(row, 5, btn_widget)

    def refresh_vehicle_table(self):
        if not self.db_manager: return
        # Check and update expiration status first
        self.db_manager.check_and_update_vehicle_expiration()
        vehicles = self.db_manager.get_all_vehicles()
        self.vehicle_table.setRowCount(0)
        for row, v in enumerate(vehicles):
            self.vehicle_table.insertRow(row)
            self.vehicle_table.setItem(row, 0, QTableWidgetItem(v['plate_number']))
            self.vehicle_table.setItem(row, 1, QTableWidgetItem(v['owner_name']))
            self.vehicle_table.setItem(row, 2, QTableWidgetItem(f"{v['make']} {v['model']}"))
            self.vehicle_table.setItem(row, 3, QTableWidgetItem(str(v['year'])))
            self.vehicle_table.setItem(row, 4, QTableWidgetItem(v['color']))
            
            # Expiry Date
            expiry_date = v.get('expiry_date', 'N/A')
            expiry_item = QTableWidgetItem(str(expiry_date) if expiry_date else 'N/A')
            self.vehicle_table.setItem(row, 5, expiry_item)
            
            # Status with color coding
            status = v.get('status', 'active').upper()
            status_item = QTableWidgetItem(status)
            if status == 'EXPIRED':
                status_item.setForeground(QColor('#dc2626'))
            elif status == 'EXPIRING':
                status_item.setForeground(QColor('#f59e0b'))
            else:
                status_item.setForeground(QColor('#059669'))
            self.vehicle_table.setItem(row, 6, status_item)
            
            # Actions
            btn_widget = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(2, 2, 2, 2)
            btn_layout.setSpacing(5)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(30, 30)
            edit_btn.setStyleSheet("background-color: #f59e0b; color: white; border-radius: 4px;")
            edit_btn.clicked.connect(lambda checked, veh=v: self.edit_vehicle_callback(veh))
            
            del_btn = QPushButton("🗑️")
            del_btn.setFixedSize(30, 30)
            del_btn.setStyleSheet("background-color: #dc2626; color: white; border-radius: 4px;")
            del_btn.clicked.connect(lambda checked, vid=v['vehicle_id']: self.delete_vehicle_callback(vid))
            
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(del_btn)
            btn_layout.addStretch()
            btn_widget.setLayout(btn_layout)
            self.vehicle_table.setCellWidget(row, 7, btn_widget)

    # Callbacks to be connected in main.py
    def edit_user_callback(self, user_data): pass
    def delete_user_callback(self, user_id): pass
    def edit_vehicle_callback(self, vehicle_data): pass
    def delete_vehicle_callback(self, vehicle_id): pass