import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QFrame, QLineEdit, QScrollArea, 
                             QHeaderView, QGraphicsDropShadowEffect, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

# --- HELPER FUNCTIONS ---
def apply_shadow(widget, blur=15, y_offset=4, alpha=30):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setYOffset(y_offset)
    shadow.setColor(QColor(0, 0, 0, alpha)) 
    widget.setGraphicsEffect(shadow)

class StatCard(QFrame):
    def __init__(self, value, label, icon, color, subtext=""):
        super().__init__()
        self.setFixedSize(260, 140)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white; 
                border-radius: 12px; 
                border: 1px solid #e2e8f0;
            }}
        """)
        apply_shadow(self)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 15)
        
        # Top Row: Value + Icon
        top_row = QHBoxLayout()
        val_lbl = QLabel(value)
        val_lbl.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        val_lbl.setStyleSheet(f"color: {color}; border: none;")
        
        icon_lbl = QLabel(icon)
        icon_lbl.setFixedSize(50, 40)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setFont(QFont("Arial", 20))
        icon_lbl.setStyleSheet(f"background-color: {color}10; border-radius: 8px; color: {color};")
        
        top_row.addWidget(val_lbl)
        top_row.addStretch()
        top_row.addWidget(icon_lbl)
        
        lbl = QLabel(label)
        lbl.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        lbl.setStyleSheet("color: #64748b; border: none;")
        
        layout.addLayout(top_row)
        layout.addWidget(lbl)
        
        # Subtext pill
        if subtext:
            sub = QLabel(subtext)
            sub.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            if "+" in subtext:
                sub.setStyleSheet("background-color: #fef3c7; color: #92400e; border-radius: 10px; padding: 2px 10px;")
            elif "Pending" in subtext:
                sub.setStyleSheet("background-color: #fee2e2; color: #991b1b; border-radius: 10px; padding: 2px 10px;")
            else:
                sub.setStyleSheet("background-color: #e0f2fe; color: #075985; border-radius: 10px; padding: 2px 10px;")
            
            sub.setFixedSize(100, 24)
            sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(sub)
            
        self.setLayout(layout)

# CHANGED: Inherit from QWidget
class EnforcerDashboard(QWidget):
    def __init__(self, user_name="Officer Juan Santos", user_dept="Traffic Enforcement Division", user_office="Davao District Office"):
        super().__init__()
        self.user_name = user_name
        self.user_dept = user_dept
        self.user_office = user_office
        self.db_manager = None
        self.current_user = None
        self.init_ui()
        
    def init_ui(self):
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Sidebar
        main_layout.addWidget(self.create_sidebar())
        
        # 2. Main Content Area (Stacked Widget)
        self.stack = QStackedWidget()
        
        # Dashboard Page
        self.dashboard_page = self.create_dashboard_page()
        self.stack.addWidget(self.dashboard_page)
        
        # Manage Violations Page
        self.manage_page = self.create_manage_page()
        self.stack.addWidget(self.manage_page)
        
        main_layout.addWidget(self.stack, stretch=1)
        
        # Apply layout to self
        self.setLayout(main_layout)

        # Initial view
        self.show_dashboard()
        
    def show_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_page)
        self.btn_dashboard.setStyleSheet(self.get_sidebar_style(True))
        self.btn_record.setStyleSheet(self.get_sidebar_style(False))
        self.btn_search.setStyleSheet(self.get_sidebar_style(False))
        self.btn_manage.setStyleSheet(self.get_sidebar_style(False))
        
    def show_manage(self):
        self.stack.setCurrentWidget(self.manage_page)
        self.btn_dashboard.setStyleSheet(self.get_sidebar_style(False))
        self.btn_record.setStyleSheet(self.get_sidebar_style(False))
        self.btn_search.setStyleSheet(self.get_sidebar_style(False))
        self.btn_manage.setStyleSheet(self.get_sidebar_style(True))
        if hasattr(self, 'refresh_manage_table'): self.refresh_manage_table()

    def create_manage_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Manage Violations")
        header.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header.setStyleSheet("color: #1e3a8a;")
        
        # Table
        self.manage_table = QTableWidget()
        self.manage_table.setColumnCount(7)
        self.manage_table.setHorizontalHeaderLabels(["ID", "Plate", "Violation", "Date", "Location", "Status", "Actions"])
        self.manage_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.manage_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # ID
        self.manage_table.verticalHeader().setVisible(False)
        self.manage_table.setStyleSheet("""
            QTableWidget { background-color: white; border-radius: 10px; border: 1px solid #e2e8f0; gridline-color: #f1f5f9; }
            QHeaderView::section { background-color: #f8fafc; padding: 12px; border: none; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #475569; }
        """)
        
        layout.addWidget(header)
        layout.addWidget(self.manage_table)
        
        page.setLayout(layout)
        return page
        
    def refresh_manage_table(self):
        if not self.db_manager: return
        violations = self.db_manager.get_all_violations()
        self.manage_table.setRowCount(0)
        for row, v in enumerate(violations):
            self.manage_table.insertRow(row)
            self.manage_table.setItem(row, 0, QTableWidgetItem(str(v.get('violation_id', '')))) # Changed to violation_id
            self.manage_table.setItem(row, 1, QTableWidgetItem(v['plate_number']))
            self.manage_table.setItem(row, 2, QTableWidgetItem(v['violation_name']))
            self.manage_table.setItem(row, 3, QTableWidgetItem(str(v['violation_date'])))
            self.manage_table.setItem(row, 4, QTableWidgetItem(v['location']))
            self.manage_table.setItem(row, 5, QTableWidgetItem(v['status'].upper()))
            
            # Actions
            btn_widget = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setSpacing(5)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(30, 30)
            edit_btn.setStyleSheet("background-color: #f59e0b; color: white; border-radius: 4px;")
            edit_btn.clicked.connect(lambda checked, viol=v: self.edit_violation_callback(viol))
            
            del_btn = QPushButton("🗑️")
            del_btn.setFixedSize(30, 30)
            del_btn.setStyleSheet("background-color: #dc2626; color: white; border-radius: 4px;")
            del_btn.clicked.connect(lambda checked, vid=v['violation_id']: self.delete_violation_callback(vid))
            
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(del_btn)
            btn_layout.addStretch()
            btn_widget.setLayout(btn_layout)
            self.manage_table.setCellWidget(row, 6, btn_widget)

    def edit_violation_callback(self, data): pass
    def delete_violation_callback(self, vid): pass

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
        layout.setSpacing(5)
        
        # Logo Area
        logo_area = QFrame()
        logo_area.setFixedHeight(180)
        logo_area.setStyleSheet("background: transparent;")
        logo_lay = QVBoxLayout()
        logo_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_lay.setSpacing(8)
        logo_lay.setContentsMargins(0, 20, 0, 0)

        logo_img = QLabel()
        try:
            from PyQt6.QtGui import QPixmap
            pm = QPixmap("images/cropped_circle_image(1).png")
            logo_img.setPixmap(pm.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        except Exception:
            logo_img.setText("🔍")
            logo_img.setFont(QFont("Arial", 40))
        logo_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_img.setStyleSheet("background: transparent;")

        txt = QLabel("Nexus Monitor")
        txt.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        txt.setStyleSheet("color: #fbbf24; margin-top: 4px; background: transparent;")
        
        logo_lay.addWidget(logo_img, alignment=Qt.AlignmentFlag.AlignCenter)
        logo_lay.addWidget(txt, alignment=Qt.AlignmentFlag.AlignCenter)
        logo_area.setLayout(logo_lay)
        layout.addWidget(logo_area)
        
        # Menu Items
        layout.addWidget(self.create_section_label("MAIN"))
        self.btn_dashboard = self.create_sidebar_btn("🏠 DASHBOARD", True)
        self.btn_dashboard.clicked.connect(self.show_dashboard)
        layout.addWidget(self.btn_dashboard)
        
        layout.addWidget(self.create_section_label("VIOLATION MANAGEMENT"))
        self.btn_record = self.create_sidebar_btn("📝 Record Violation")
        self.btn_search = self.create_sidebar_btn("🔍 Search Records")
        self.btn_manage = self.create_sidebar_btn("⚠️ Manage Violations")
        self.btn_manage.clicked.connect(self.show_manage)
        
        layout.addWidget(self.btn_record)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.btn_manage)
        
        layout.addStretch()
        sidebar.setLayout(layout)
        return sidebar

    def create_dashboard_page(self): # Renamed from create_main_content
        content = QWidget()
        content.setStyleSheet("background-color: #f1f5f9;")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        layout.addWidget(self.create_header())
        
        # Scroll Area for Body
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        body = QWidget()
        body_layout = QVBoxLayout() 
        body_layout.setContentsMargins(25, 25, 25, 25)
        body_layout.setSpacing(25)
        
        # 1. Stats Row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(25)
        
        self.card_total = StatCard("...", "TOTAL VIOLATIONS", "🚗", "#dc2626", "+0 New")
        self.card_pending = StatCard("...", "PENDING CASES", "💰", "#f59e0b", "0 Pending")
        self.card_searched = StatCard("...", "ACTIVE OFFICERS", "👮", "#1e40af", "Live Count")
        
        stats_row.addWidget(self.card_total)
        stats_row.addWidget(self.card_pending)
        stats_row.addWidget(self.card_searched)
        stats_row.addStretch() 
        body_layout.addLayout(stats_row)
        
        # 2. Split Section
        split_layout = QHBoxLayout()
        split_layout.setSpacing(25)
        
        # --- LEFT COLUMN ---
        left_col = QVBoxLayout()
        left_col.setSpacing(25)
        
        # Recent Violations Panel
        recent_panel = self.create_blue_panel("RECENT VIOLATIONS RECORD", has_add_btn=True)
        self.recent_table = QTableWidget()
        self.setup_table(self.recent_table, ["CITATION", "PLATE", "VIOLATION", "DATE", "STATUS"])
        recent_panel.layout().addWidget(self.recent_table)
        left_col.addWidget(recent_panel)
        
        # REMOVED Search Results Panel as requested
        # Search is now handled via Dialog and "Search Records" button

        
        # --- RIGHT COLUMN ---
        right_col = QVBoxLayout()
        right_col.setSpacing(25)
        
        # Quick Actions Card
        qa_card = QFrame()
        qa_card.setFixedWidth(320)
        qa_card.setStyleSheet("background-color: white; border-radius: 12px;")
        apply_shadow(qa_card)
        qa_layout = QVBoxLayout()
        qa_layout.setContentsMargins(20, 20, 20, 20)
        
        qa_title = QLabel("QUICK ACTIONS")
        qa_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        qa_title.setStyleSheet("color: #1e40af; border: none;")
        qa_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qa_layout.addWidget(qa_title)
        qa_layout.addSpacing(10)
        
        self.qa_record = self.action_btn("🔥 RECORD VIOLATION", "#dc2626", solid=True)
        self.qa_search = self.action_btn("🔍 SEARCH VEHICLE", "#1e40af", outline=True)
        self.qa_update = self.action_btn("✏️ UPDATE DETAILS", "#16a34a", outline=True)
        
        qa_layout.addWidget(self.qa_record)
        qa_layout.addWidget(self.qa_search)
        qa_layout.addWidget(self.qa_update)
        qa_card.setLayout(qa_layout)
        
        # Alerts Card
        alert_card = QFrame()
        alert_card.setFixedWidth(320)
        alert_card.setStyleSheet("background-color: white; border-radius: 12px;")
        apply_shadow(alert_card)
        alert_layout = QVBoxLayout()
        alert_layout.setContentsMargins(15, 15, 15, 15)
        
        alert_header = QLabel("⚠️ ALERTS")
        alert_header.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        alert_header.setStyleSheet("background-color: #dc2626; color: white; border-radius: 5px; padding: 10px;")
        alert_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        alert_msg = QLabel("REMINDER:\nVerify details before submission.")
        alert_msg.setFont(QFont("Arial", 9))
        alert_msg.setStyleSheet("background-color: #fee2e2; color: #7f1d1d; border-radius: 5px; padding: 15px; margin-top: 10px;")
        alert_msg.setWordWrap(True)
        
        alert_layout.addWidget(alert_header)
        alert_layout.addWidget(alert_msg)
        alert_card.setLayout(alert_layout)
        
        right_col.addWidget(qa_card)
        right_col.addWidget(alert_card)
        right_col.addStretch()
        
        split_layout.addLayout(left_col, stretch=1)
        split_layout.addLayout(right_col, stretch=0)
        
        body_layout.addLayout(split_layout)
        body.setLayout(body_layout)
        
        scroll.setWidget(body)
        layout.addWidget(scroll)
        content.setLayout(layout)
        return content

    def create_header(self):
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #1e40af;")
        layout = QHBoxLayout()
        layout.setContentsMargins(25, 0, 30, 0)
        
        t_lay = QVBoxLayout()
        t_lay.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        t_lay.setSpacing(2)
        t1 = QLabel("LAND TRANSPORTATION OFFICE")
        t1.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        t1.setStyleSheet("color: white; border: none;")
        t2 = QLabel("Vehicle Violation Monitoring System")
        t2.setStyleSheet("color: #fbbf24; border: none; font-size: 11px;")
        t_lay.addWidget(t1)
        t_lay.addWidget(t2)
        
        u_lay = QVBoxLayout()
        u_lay.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        u_lay.setSpacing(2)
        u1 = QLabel(self.user_name)
        u1.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        u1.setStyleSheet("color: white; border: none;")
        u1.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        u2 = QLabel(f"{self.user_dept}\n{self.user_office}")
        u2.setStyleSheet("color: #93c5fd; border: none; font-size: 10px;")
        u2.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        u_lay.addWidget(u1)
        u_lay.addWidget(u2)
        
        self.logout_btn = QPushButton("LOGOUT")
        self.logout_btn.setFixedSize(90, 32)
        self.logout_btn.setStyleSheet("""
            QPushButton { background-color: #dc2626; color: white; font-weight: bold; border-radius: 5px; border: none; }
            QPushButton:hover { background-color: #b91c1c; }
        """)
        
        layout.addLayout(t_lay)
        layout.addStretch()
        layout.addLayout(u_lay)
        layout.addSpacing(20)
        layout.addWidget(self.logout_btn)
        
        header.setLayout(layout)
        return header

    def create_blue_panel(self, title, has_add_btn=False):
        panel = QFrame()
        apply_shadow(panel)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("background-color: #1e40af; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        h_lay = QHBoxLayout()
        h_lay.setContentsMargins(20, 0, 20, 0)
        
        lbl = QLabel(title)
        lbl.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        lbl.setStyleSheet("color: white; border: none;")
        h_lay.addWidget(lbl)
        
        if has_add_btn:
            h_lay.addStretch()
            self.btn_panel_add = QPushButton("+ ADD VIOLATION")
            self.btn_panel_add.setFixedSize(140, 30)
            self.btn_panel_add.setStyleSheet("""
                QPushButton { background-color: #dc2626; color: white; font-weight: bold; border-radius: 5px; border: none; }
                QPushButton:hover { background-color: #b91c1c; }
            """)
            h_lay.addWidget(self.btn_panel_add)
            
        header.setLayout(h_lay)
        
        body = QFrame()
        body.setStyleSheet("background-color: white; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        b_lay = QVBoxLayout()
        b_lay.setContentsMargins(10, 10, 10, 10)
        b_lay.setSpacing(0)
        body.setLayout(b_lay)
        
        layout.addWidget(header)
        layout.addWidget(body)
        panel.setLayout(layout)
        return panel
    def setup_table(self, table, headers):
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet("""
            QTableWidget { border: none; gridline-color: #f1f5f9; background-color: white; }
            QHeaderView::section { background-color: white; color: #64748b; font-weight: bold; border: none; padding: 12px; border-bottom: 2px solid #f1f5f9; }
            QTableWidget::item { padding: 12px; border-bottom: 1px solid #f1f5f9; color: #334155; }
        """)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def create_section_label(self, text): # Renamed from menu_label
        l = QLabel(text)
        l.setFont(QFont("Arial", 8, QFont.Weight.Bold))
        l.setStyleSheet("color: #93c5fd; padding: 15px 0 5px 25px; background: transparent; border: none;")
        return l

    def get_sidebar_style(self, active):
        style = "background-color: #dc2626;" if active else "background: transparent;"
        return f"""
            QPushButton {{ {style} color: white; border: none; text-align: left; padding-left: 25px; font-weight: bold; font-size: 13px; }} 
            QPushButton:hover {{ background-color: #1e40af; }}
        """

    def create_sidebar_btn(self, text, active=False): # Renamed from sidebar_btn
        btn = QPushButton(text)
        btn.setFixedHeight(45)
        btn.setStyleSheet(self.get_sidebar_style(active))
        return btn

    def action_btn(self, text, color, solid=False, outline=False):
        btn = QPushButton(text)
        btn.setFixedHeight(50)
        btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        if outline:
            btn.setStyleSheet(f"""
                QPushButton {{ background: white; color: {color}; border: 2px solid {color}; border-radius: 8px; }} 
                QPushButton:hover {{ background: {color}10; }}
            """)
        elif solid:
            btn.setStyleSheet(f"""
                QPushButton {{ background: {color}; color: white; border: none; border-radius: 8px; }} 
                QPushButton:hover {{ opacity: 0.9; }}
            """)
        return btn

    def populate_recent_table(self, violations):
        self.recent_table.setRowCount(0)
        for row, v in enumerate(violations):
            self.recent_table.insertRow(row)
            self.recent_table.setItem(row, 0, QTableWidgetItem(str(v.get('citation_number', ''))))
            self.recent_table.setItem(row, 1, QTableWidgetItem(v['plate_number']))
            self.recent_table.setItem(row, 2, QTableWidgetItem(v['violation_name']))
            self.recent_table.setItem(row, 3, QTableWidgetItem(str(v['violation_date'])))
            
            status_item = QTableWidgetItem(v['status'].upper())
            if v['status'] == 'paid': status_item.setForeground(Qt.GlobalColor.darkGreen)
            elif v['status'] == 'overdue': status_item.setForeground(Qt.GlobalColor.red)
            self.recent_table.setItem(row, 4, status_item)


    # Updated update_stats to use real data
    def update_stats(self):
        if not self.db_manager: return
        stats = self.db_manager.get_dashboard_stats()
        
        # stats keys: users, vehicles, violations, fines, pending_violations, paid_violations, overdue_violations
        
        # Card 1: Total Violations
        # Finding labels via findChild is fragile if structure varies, but let's assume standard StatCard
        # StatCard layout: QVBoxLayout -> TopRow(QHBoxLayout) -> ValueLabel(index 0)
        
        def update_card_value(card, value):
            try:
                # Value label is usually the first large font label
                labels = card.findChildren(QLabel)
                for lbl in labels:
                    if lbl.font().pointSize() >= 20: # Heuristic for value label
                         lbl.setText(str(value))
                         return
            except: pass

        update_card_value(self.card_total, stats['violations'])
        update_card_value(self.card_pending, stats['pending_violations'])
        
        # Active officers (real time count)
        update_card_value(self.card_searched, stats.get('enforcers', 0))