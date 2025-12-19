import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QFrame, QLineEdit, QScrollArea, 
                             QHeaderView, QGraphicsDropShadowEffect, QMessageBox)
from PyQt6.QtCore import Qt, QSize
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
    """Statistics card widget"""
    def __init__(self, value, label, icon, color, sublabel=""):
        super().__init__()
        self.setFixedSize(240, 130)
        self.setObjectName("MainStatCard")
        
        self.setStyleSheet(f"""
            QFrame#MainStatCard {{
                background-color: white;
                border-radius: 12px;
                border-top: 5px solid {color};
            }}
            QFrame#MainStatCard:hover {{
                background-color: #fafafa;
                margin-top: -2px;
            }}
        """)
        apply_shadow(self)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 15)
        layout.setSpacing(10)
        
        top_layout = QHBoxLayout()
        
        self.value_label = QLabel(value)
        self.value_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        self.value_label.setStyleSheet(f"color: {color}; background: transparent;")
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 24))
        icon_label.setFixedSize(45, 45)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rgba_color = hex_to_rgba(color, 0.15)
        icon_label.setStyleSheet(f"background-color: {rgba_color}; border-radius: 10px;")
        
        top_layout.addWidget(self.value_label)
        top_layout.addStretch()
        top_layout.addWidget(icon_label)
        
        label_widget = QLabel(label)
        label_widget.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        label_widget.setStyleSheet("color: #64748b; background: transparent;")
        
        layout.addLayout(top_layout)
        layout.addWidget(label_widget)
        
        if sublabel:
            sub_lbl = QLabel(sublabel)
            sub_lbl.setFont(QFont("Arial", 9))
            sub_lbl.setStyleSheet("color: #94a3b8; background: transparent;")
            layout.addWidget(sub_lbl)
            
        layout.addStretch()
        self.setLayout(layout)

    def update_value(self, new_value):
        self.value_label.setText(str(new_value))


class CitizenDashboard(QWidget):
    def __init__(self, user_data=None, db_manager=None):
        super().__init__()
        self.user_data = user_data or {"full_name": "GUEST", "user_id": 0}
        self.user_name = self.user_data.get("full_name", "GUEST")
        self.db_manager = db_manager
        
        # State
        self.plate_numbers = []
        self.sidebar_buttons = {} # Store buttons for toggling styles
        
        # Initial Fetch
        if self.db_manager and self.user_data.get("user_id"):
            self.refresh_plates()
            
        self.init_ui()
        
    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        content = self.create_main_content()
        main_layout.addWidget(content, stretch=1)
        
        self.setLayout(main_layout)
        
        # Initial Data Load
        self.update_dashboard()

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
        
        # Logo Section
        logo_section = QFrame()
        logo_section.setFixedHeight(180)
        logo_section.setStyleSheet("background: transparent;")
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.setSpacing(10)
        
        logo_bg = QLabel()
        logo_bg.setFixedSize(80, 80)
        logo_bg.setStyleSheet("background-color: white; border-radius: 40px;")
        logo_bg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        try:
            pix = QPixmap("images/cropped_circle_image(1).png")
            if not pix.isNull():
               logo_bg.setPixmap(pix.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        except: pass
            
        brand = QLabel("Nexus Monitor")
        brand.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        brand.setStyleSheet("color: #fbbf24;")
        
        sub = QLabel("REPUBLIC OF THE PHILIPPINES")
        sub.setFont(QFont("Arial", 7, QFont.Weight.Bold))
        sub.setStyleSheet("color: #93c5fd;")
        
        logo_layout.addWidget(logo_bg)
        logo_layout.addWidget(brand)
        logo_layout.addWidget(sub)
        logo_section.setLayout(logo_layout)
        layout.addWidget(logo_section)
        
        # Menu Items
        menu_items = [
            ("MAIN", [("🏠 MY DASHBOARD", True)]),
            ("MY VEHICLES", [("🚗 My Vehicles", False)]),
            ("VIOLATIONS", [("⚠️ My Violations", False)]),
            ("INFORMATION", [("ℹ️ Help & Support", False)])
        ]
        
        for title, items in menu_items:
            if title:
                lbl = QLabel(title)
                lbl.setFont(QFont("Arial", 8, QFont.Weight.Bold))
                lbl.setStyleSheet("color: #93c5fd; padding: 15px 0 5px 20px; background: transparent;")
                layout.addWidget(lbl)
            
            for text, active in items:
                btn = QPushButton(text)
                btn.setFixedHeight(40)
                btn.setStyleSheet(self.sidebar_btn_style(active))
                btn.clicked.connect(lambda checked, t=text: self.toggle_section(t))
                layout.addWidget(btn)
                self.sidebar_buttons[text] = btn
                
        layout.addStretch()
        sidebar.setLayout(layout)
        return sidebar

    def sidebar_btn_style(self, active):
        if active:
            return """
                QPushButton {
                    background-color: #dc2626; color: white; border: none;
                    text-align: left; padding-left: 20px; font-weight: bold;
                }
            """
        else:
            return """
                QPushButton {
                    background: transparent; color: white; border: none;
                    text-align: left; padding-left: 20px;
                }
                QPushButton:hover { background-color: #1e40af; }
            """

    def create_main_content(self):
        content = QWidget()
        content.setStyleSheet("background-color: #f1f5f9;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        header = self.create_header()
        layout.addWidget(header)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        scroll_content = QWidget()
        main_scroll_layout = QVBoxLayout()
        main_scroll_layout.setContentsMargins(20, 20, 20, 20)
        main_scroll_layout.setSpacing(20)
        
        # 1. Welcome Banner
        main_scroll_layout.addWidget(self.create_welcome_section())
        
        # 2. Stats Row
        main_scroll_layout.addLayout(self.create_stats_cards())
        
        # 3. Main Split (Violations Table | Quick Actions)
        split_row = QHBoxLayout()
        split_row.setSpacing(20)
        
        # Left Side: My Violations Table
        self.violations_container = self.create_blue_panel("MY VIOLATIONS RECORD", refresh_btn=True)
        # We need a body layout inside the container to switch content or just keep table
        # My create_blue_panel helper returns a structure with a body frame
        
        self.violations_table = QTableWidget()
        self.setup_table(self.violations_table)
        
        # Find body frame and set layout
        body_frame = self.violations_container.findChild(QFrame, "body_frame")
        if body_frame:
            table_layout = QVBoxLayout()
            table_layout.setContentsMargins(0, 0, 0, 0)
            # Column legend strip for clarity
            legend = QFrame()
            legend.setStyleSheet("background-color: #f8fafc; border-radius: 6px; padding: 8px 12px;")
            legend_layout = QHBoxLayout()
            legend_layout.setContentsMargins(0, 0, 0, 0)
            legend_layout.setSpacing(20)
            for text in ["CITATION", "PLATE NO.", "VIOLATION", "DATE", "STATUS", "PAYMENT DATE"]:
                lbl = QLabel(text)
                lbl.setStyleSheet("color: #475569; font-weight: bold;")
                legend_layout.addWidget(lbl)
            legend_layout.addStretch()
            legend.setLayout(legend_layout)
            table_layout.addWidget(legend)
            table_layout.addWidget(self.violations_table)
            body_frame.setLayout(table_layout)
        
        split_row.addWidget(self.violations_container, stretch=2)
        
        # Right Side: Quick Actions
        self.qa_panel = self.create_quick_actions()
        split_row.addWidget(self.qa_panel, stretch=1)
        
        main_scroll_layout.addLayout(split_row)
        
        # 4. My Vehicles Section (Initially Hidden)
        self.my_vehicles_section = self.create_my_vehicles_section()
        self.my_vehicles_section.setVisible(False)
        main_scroll_layout.addWidget(self.my_vehicles_section)
        
        main_scroll_layout.addStretch()
        
        scroll_content.setLayout(main_scroll_layout)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        content.setLayout(layout)
        return content

    def create_header(self):
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("background-color: #1e40af; border-bottom: 3px solid #fbbf24;")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 0, 30, 0)
        
        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        t1 = QLabel("LAND TRANSPORTATION OFFICE")
        t1.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        t1.setStyleSheet("color: white; border: none;")
        t2 = QLabel("Vehicle Violation Monitoring System")
        t2.setFont(QFont("Arial", 10))
        t2.setStyleSheet("color: #fbbf24; border: none;")
        title_box.addStretch()
        title_box.addWidget(t1)
        title_box.addWidget(t2)
        title_box.addStretch()
        
        user_box = QVBoxLayout()
        user_box.setSpacing(0)
        user_box.setAlignment(Qt.AlignmentFlag.AlignRight)
        u1 = QLabel(self.user_name)
        u1.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        u1.setStyleSheet("color: white; border: none;")
        u2 = QLabel("Vehicle Owner")
        u2.setFont(QFont("Arial", 8))
        u2.setStyleSheet("color: #93c5fd; border: none;")
        u2.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        user_box.addStretch()
        user_box.addWidget(u1)
        user_box.addWidget(u2)
        user_box.addStretch()
        
        self.logout_btn = QPushButton("LOGOUT")
        self.logout_btn.setFixedSize(80, 30)
        self.logout_btn.setStyleSheet("background: #dc2626; color: white; font-weight: bold; border-radius: 4px;")
        
        layout.addLayout(title_box)
        layout.addStretch()
        layout.addLayout(user_box)
        layout.addSpacing(15)
        layout.addWidget(self.logout_btn)
        
        header.setLayout(layout)
        return header

    def create_welcome_section(self):
        welcome = QFrame()
        welcome.setFixedHeight(80)
        welcome.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e40af, stop:1 #3b82f6);
                border-radius: 12px;
            }
        """)
        apply_shadow(welcome)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(30, 0, 30, 0)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        
        greeting = QLabel(f"Welcome back, {self.user_name}! 👋")
        greeting.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        greeting.setStyleSheet("color: white; background: transparent;")
        
        message = QLabel("Monitor your vehicle violations and stay compliant with traffic regulations")
        message.setFont(QFont("Arial", 11))
        message.setStyleSheet("color: #dbeafe; background: transparent;")
        
        text_layout.addStretch()
        text_layout.addWidget(greeting)
        text_layout.addWidget(message)
        text_layout.addStretch()
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        welcome.setLayout(layout)
        return welcome

    def create_stats_cards(self):
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        self.card_vehicles = StatCard("0", "MY VEHICLES", "🚗", "#1e40af", "Registered")
        self.card_violations = StatCard("0", "TOTAL VIOLATIONS", "⚠️", "#dc2626", "Pending")
        self.card_fines = StatCard("₱0", "OUTSTANDING FINES", "💰", "#f59e0b", "Unpaid Amount")
        
        stats_layout.addWidget(self.card_vehicles)
        stats_layout.addWidget(self.card_violations)
        stats_layout.addWidget(self.card_fines)
        
        return stats_layout

    def create_blue_panel(self, title_text, refresh_btn=False):
        container = QFrame()
        apply_shadow(container)
        container.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("background-color: #1e40af; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(20, 0, 20, 0)
        
        t_label = QLabel(title_text)
        t_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        t_label.setStyleSheet("color: white;")
        h_layout.addWidget(t_label)
        h_layout.addStretch()

        if refresh_btn:
            self.btn_refresh = QPushButton("REFRESH")
            self.btn_refresh.setFixedSize(100, 30)
            self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_refresh.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.2);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.5);
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 11px;
                }
                QPushButton:hover { background-color: rgba(255, 255, 255, 0.3); }
            """)
            self.btn_refresh.clicked.connect(self.update_dashboard)
            h_layout.addWidget(self.btn_refresh)
            
        header.setLayout(h_layout)
        layout.addWidget(header)
        
        # Notice box logic removed or can be re-added if specific design requires it
        # For general table, not always needed.
        
        body_frame = QFrame()
        body_frame.setObjectName("body_frame")
        body_frame.setStyleSheet("background: white; padding: 15px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        layout.addWidget(body_frame)
        
        container.setLayout(layout)
        return container

    def create_quick_actions(self):
        panel = QFrame()
        panel.setStyleSheet("background: white; border-radius: 10px;")
        apply_shadow(panel)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("QUICK ACTIONS")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e40af;")
        layout.addWidget(title)
        
        self.btn_qa_check = self.create_action_btn("🔍 Check Status", "#1e40af")
        self.btn_qa_payment = self.create_action_btn("💳 Make Payment", "#16a34a")
        self.btn_qa_edit = self.create_action_btn("✏️ Edit Profile", "#475569", outline=True)
        self.btn_qa_help = self.create_action_btn("❓ Help/Support", "#f59e0b", outline=True)
        
        layout.addWidget(self.btn_qa_check)
        layout.addWidget(self.btn_qa_payment)
        layout.addWidget(self.btn_qa_edit)
        layout.addWidget(self.btn_qa_help)
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel

    def create_action_btn(self, text, color, outline=False):
        btn = QPushButton(text)
        btn.setFixedHeight(45)
        btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        if outline:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: white; color: {color}; border: 2px solid {color}; border-radius: 8px;
                }}
                QPushButton:hover {{ background: {color}10; }}
            """)
        else:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {color}; color: white; border: none; border-radius: 8px;
                }}
                QPushButton:hover {{ opacity: 0.9; }}
            """)
        return btn

    def create_my_vehicles_section(self):
        container = QFrame()
        container.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(15)
        
        header = self.create_blue_panel("MY REGISTERED VEHICLES")
        # Reuse just the header visual or full
        
        # Vehicle Cards Layout
        self.vehicles_layout = QHBoxLayout()
        self.vehicles_layout.setSpacing(20)
        self.vehicles_layout.addStretch() # Initial
        
        layout.addWidget(header)
        layout.addLayout(self.vehicles_layout)
        
        container.setLayout(layout)
        return container

    def create_vehicle_card(self, plate, model="-", status="Active", expiry="-", color="-"):
        card = QFrame()
        card.setFixedSize(280, 140)
        apply_shadow(card)
        card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #eff6ff, stop:1 #dbeafe);
                border: 1px solid #bfdbfe;
                border-radius: 12px;
            }
            QFrame:hover { border: 2px solid #3b82f6; }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        
        top = QHBoxLayout()
        icon = QLabel("🚗")
        icon.setFont(QFont("Arial", 30))
        icon.setStyleSheet("background: transparent; border: none;")
        
        text_box = QVBoxLayout()
        p = QLabel(plate)
        p.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        p.setStyleSheet("color: #1e40af; background: transparent; border: none;")
        t = QLabel(model)
        t.setStyleSheet("color: #64748b; background: transparent; border: none;")
        text_box.addWidget(p)
        text_box.addWidget(t)
        
        top.addWidget(icon)
        top.addLayout(text_box)
        top.addStretch()
        
        # Status label with color coding
        status_text = status.upper()
        if status_text == "EXPIRED":
            status_icon = "✗"
            status_style = "background-color: #fee2e2; color: #991b1b; padding: 4px 8px; border-radius: 5px;"
        elif status_text == "EXPIRING":
            status_icon = "⚠"
            status_style = "background-color: #fef3c7; color: #92400e; padding: 4px 8px; border-radius: 5px;"
        else:  # ACTIVE
            status_icon = "✓"
            status_style = "background-color: #dcfce7; color: #166534; padding: 4px 8px; border-radius: 5px;"
        
        status_lbl = QLabel(f"{status_icon} {status_text}")
        status_lbl.setStyleSheet(status_style)
        status_lbl.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_lbl.setFixedWidth(100)
        
        detail = QLabel(f"Expiry: {expiry}  •  Color: {color}")
        detail.setStyleSheet("color: #475569;")

        layout.addLayout(top)
        layout.addWidget(detail)
        layout.addStretch()
        layout.addWidget(status_lbl)
        
        card.setLayout(layout)
        return card

    def setup_table(self, table):
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["ID", "PLATE NO.", "VIOLATION", "DATE", "STATUS", "PAYMENT DATE"])
        table.verticalHeader().setVisible(False)
        table.setMinimumHeight(400)
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: transparent;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 12px;
                border: none;
                border-bottom: 1px solid #e2e8f0;
                font-weight: bold;
                color: #475569;
            }
            QTableWidget::item {
                border-bottom: 1px solid #f1f5f9;
                padding: 10px;
                color: #334155;
            }
        """)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def toggle_section(self, section_name):
        # Update styling
        for key, btn in self.sidebar_buttons.items():
            btn.setStyleSheet(self.sidebar_btn_style(key == section_name))
            
        # Logic
        if section_name == "🚗 My Vehicles":
            self.violations_container.setVisible(False)
            self.my_vehicles_section.setVisible(True)
            if hasattr(self, "qa_panel"):
                self.qa_panel.setVisible(False)
            self.populate_vehicles_list()
        else:
            # Default to dashboard/violations view
            self.violations_container.setVisible(True)
            self.my_vehicles_section.setVisible(False)
            if hasattr(self, "qa_panel"):
                self.qa_panel.setVisible(True)
            self.update_dashboard()

    def refresh_plates(self):
        if not self.db_manager: return
        vehicles = self.db_manager.get_all_vehicles()
        uid = self.user_data.get('user_id')
        self.plate_numbers = [v['plate_number'] for v in vehicles if v['owner_id'] == uid]

    def update_dashboard(self):
        if not self.db_manager: return
        self.refresh_plates()
        
        uid = self.user_data.get('user_id')
        violations = self.db_manager.get_violations_by_owner(uid)
        
        # Update Cards
        self.card_vehicles.update_value(len(self.plate_numbers))
        self.card_violations.update_value(len(violations))
        
        pending_fine = sum(v['fine_amount'] for v in violations if v['status'] == 'pending')
        self.card_fines.update_value(f"₱{pending_fine:,.0f}")
        
        # Populate Table
        self.violations_table.setRowCount(0)
        for row, v in enumerate(violations):
            self.violations_table.insertRow(row)
            self.violations_table.setItem(row, 0, QTableWidgetItem(v['citation_number']))
            self.violations_table.setItem(row, 1, QTableWidgetItem(v['plate_number']))
            self.violations_table.setItem(row, 2, QTableWidgetItem(v['violation_name']))
            self.violations_table.setItem(row, 3, QTableWidgetItem(str(v['violation_date'])))
            
            status = v['status'].upper()
            status_item = QTableWidgetItem(status)
            if status == "PAID":
                status_item.setForeground(QColor("#16a34a"))
            else:
                status_item.setForeground(QColor("#dc2626"))
            self.violations_table.setItem(row, 4, status_item)
            
            pay_date = v.get('payment_date', '-') if v.get('payment_date') else '-'
            self.violations_table.setItem(row, 5, QTableWidgetItem(str(pay_date)))

    def populate_vehicles_list(self):
        # Clear existing
        while self.vehicles_layout.count():
            item = self.vehicles_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        if not self.db_manager: return
        
        # Check and update expiration status first
        self.db_manager.check_and_update_vehicle_expiration()
        
        vehicles = self.db_manager.get_all_vehicles()
        my_vehicles = [v for v in vehicles if v['owner_id'] == self.user_data.get('user_id')]
        
        if not my_vehicles:
            lbl = QLabel("No registered vehicles found.")
            lbl.setStyleSheet("color: #64748b; font-style: italic;")
            self.vehicles_layout.addWidget(lbl)
            
        for v in my_vehicles:
            # Get status from database
            status = v.get('status', 'active').upper()
            card = self.create_vehicle_card(
                v['plate_number'],
                f"{v['make']} {v['model']}",
                status,
                str(v.get('expiry_date', 'N/A')),
                v.get('color', '-')
            )
            self.vehicles_layout.addWidget(card)
            
        self.vehicles_layout.addStretch()