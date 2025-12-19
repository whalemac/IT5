from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QComboBox, QMessageBox, 
                             QFrame, QTextEdit, QDateEdit, QTableWidget,
                             QTableWidgetItem, QSpinBox, QDoubleSpinBox,
                             QFormLayout, QHeaderView, QFileDialog)
from PyQt6.QtCore import Qt, QDate
import csv
from PyQt6.QtGui import QFont
from datetime import datetime


# ==================== ADD USER DIALOG ====================
class AddUserDialog(QDialog):
    def __init__(self, db_manager, parent=None, user_data=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user_data = user_data
        self.setWindowTitle("Edit User" if user_data else "Add New User")
        self.setFixedSize(520, 680)
        self.setModal(True)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(0)
        
        # Title Section
        title_frame = QFrame()
        title_frame.setStyleSheet("QFrame { background-color: transparent; }")
        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 15)
        
        title_icon = QLabel("👤" if not self.user_data else "✏️")
        title_icon.setFont(QFont("Arial", 28))
        title_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_text = "EDIT USER" if self.user_data else "ADD NEW USER"
        title = QLabel(title_text)
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e40af;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title)
        title_frame.setLayout(title_layout)
        layout.addWidget(title_frame)
        
        # Form Container with white background
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame { 
                background-color: white; 
                border-radius: 12px; 
                border: 1px solid #e2e8f0;
            }
        """)
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(12)
        
        # Account Credentials Section
        cred_label = QLabel("📋 Account Credentials")
        cred_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        cred_label.setStyleSheet("color: #1e40af; background: transparent; border: none;")
        form_layout.addWidget(cred_label)
        
        # Username & Password Row
        cred_row = QHBoxLayout()
        cred_row.setSpacing(15)
        
        username_col = QVBoxLayout()
        username_col.setSpacing(5)
        username_lbl = QLabel("Username")
        username_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setFixedHeight(42)
        self.username_input.setStyleSheet(self._input_style())
        username_col.addWidget(username_lbl)
        username_col.addWidget(self.username_input)
        
        password_col = QVBoxLayout()
        password_col.setSpacing(5)
        password_lbl = QLabel("Password")
        password_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(42)
        self.password_input.setStyleSheet(self._input_style())
        password_col.addWidget(password_lbl)
        password_col.addWidget(self.password_input)
        
        cred_row.addLayout(username_col)
        cred_row.addLayout(password_col)
        form_layout.addLayout(cred_row)
        
        # Personal Information Section
        personal_label = QLabel("👤 Personal Information")
        personal_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        personal_label.setStyleSheet("color: #1e40af; margin-top: 10px; background: transparent; border: none;")
        form_layout.addWidget(personal_label)
        
        # Full Name
        fullname_col = QVBoxLayout()
        fullname_col.setSpacing(5)
        fullname_lbl = QLabel("Full Name")
        fullname_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Enter full name")
        self.fullname_input.setFixedHeight(42)
        self.fullname_input.setStyleSheet(self._input_style())
        fullname_col.addWidget(fullname_lbl)
        fullname_col.addWidget(self.fullname_input)
        form_layout.addLayout(fullname_col)
        
        # Email & Phone Row
        contact_row = QHBoxLayout()
        contact_row.setSpacing(15)
        
        email_col = QVBoxLayout()
        email_col.setSpacing(5)
        email_lbl = QLabel("Email Address")
        email_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@email.com")
        self.email_input.setFixedHeight(42)
        self.email_input.setStyleSheet(self._input_style())
        email_col.addWidget(email_lbl)
        email_col.addWidget(self.email_input)
        
        phone_col = QVBoxLayout()
        phone_col.setSpacing(5)
        phone_lbl = QLabel("Phone Number")
        phone_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("09XX-XXX-XXXX")
        self.phone_input.setFixedHeight(42)
        self.phone_input.setStyleSheet(self._input_style())
        phone_col.addWidget(phone_lbl)
        phone_col.addWidget(self.phone_input)
        
        contact_row.addLayout(email_col)
        contact_row.addLayout(phone_col)
        form_layout.addLayout(contact_row)
        
        # Work Information Section
        work_label = QLabel("🏢 Work Information")
        work_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        work_label.setStyleSheet("color: #1e40af; margin-top: 10px; background: transparent; border: none;")
        form_layout.addWidget(work_label)
        
        # Role & Department Row
        work_row = QHBoxLayout()
        work_row.setSpacing(15)
        
        role_col = QVBoxLayout()
        role_col.setSpacing(5)
        role_lbl = QLabel("Role")
        role_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.role_combo = QComboBox()
        self.role_combo.addItems(["admin", "enforcer", "citizen"])
        self.role_combo.setFixedHeight(42)
        self.role_combo.setStyleSheet(self._combo_style())
        role_col.addWidget(role_lbl)
        role_col.addWidget(self.role_combo)
        
        dept_col = QVBoxLayout()
        dept_col.setSpacing(5)
        dept_lbl = QLabel("Department")
        dept_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.department_input = QLineEdit()
        self.department_input.setPlaceholderText("Optional")
        self.department_input.setFixedHeight(42)
        self.department_input.setStyleSheet(self._input_style())
        dept_col.addWidget(dept_lbl)
        dept_col.addWidget(self.department_input)
        
        work_row.addLayout(role_col)
        work_row.addLayout(dept_col)
        form_layout.addLayout(work_row)
        
        # Office Location
        office_col = QVBoxLayout()
        office_col.setSpacing(5)
        office_lbl = QLabel("Office Location")
        office_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.office_input = QLineEdit()
        self.office_input.setPlaceholderText("Davao District Office")
        self.office_input.setText("Davao District Office")
        self.office_input.setFixedHeight(42)
        self.office_input.setStyleSheet(self._input_style())
        office_col.addWidget(office_lbl)
        office_col.addWidget(self.office_input)
        form_layout.addLayout(office_col)
        
        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        layout.addSpacing(15)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setFixedSize(130, 45)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #64748b;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #f1f5f9; border-color: #94a3b8; }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("UPDATE USER" if self.user_data else "SAVE USER")
        save_btn.setFixedSize(160, 45)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e40af;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #1e3a8a; }
        """)
        save_btn.clicked.connect(self.save_user)
        
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Pre-fill data if editing
        if self.user_data:
            self.username_input.setText(self.user_data.get('username', ''))
            self.username_input.setReadOnly(True)
            self.fullname_input.setText(self.user_data.get('full_name', ''))
            self.email_input.setText(self.user_data.get('email', ''))
            self.phone_input.setText(self.user_data.get('phone', ''))
            self.role_combo.setCurrentText(self.user_data.get('role', 'citizen'))
            self.department_input.setText(self.user_data.get('department', ''))
            self.office_input.setText(self.user_data.get('office_location', ''))
            self.password_input.setPlaceholderText("Leave blank to keep current")
    
    def _input_style(self):
        return """
            QLineEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus { 
                border: 2px solid #1e40af; 
                background-color: white;
            }
        """
    
    def _combo_style(self):
        return """
            QComboBox {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox:focus { border: 2px solid #1e40af; }
            QComboBox::drop-down { border: none; width: 30px; }
        """
    
    def save_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        full_name = self.fullname_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        role = self.role_combo.currentText()
        department = self.department_input.text().strip()
        office = self.office_input.text().strip()
        
        if not all([username, password, full_name, role]):
            QMessageBox.warning(self, "Validation Error", 
                              "Please fill in all required fields!")
            return
        
        if self.user_data:
            # Update Logic
            if password: # Change password if provided
                # Only hash if it's a new password (simple check, ideally handled in backend)
                pass_hash = self.db_manager.hash_password(password)
                # We need a update_user_password method or just update it manually via query if allowed
                # For now let's skip password update in this simple refactor or do it if we had the method
                pass 
                
            success = self.db_manager.update_user(
                self.user_data['user_id'],
                full_name, email, phone, department if department else None, office if office else "Davao District Office"
            )
            
            if success:
                QMessageBox.information(self, "Success", "User updated successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to update user!")
        else:
            # Add Logic
            if len(password) < 6:
                QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters!")
                return
                
            user_id = self.db_manager.add_user(
                username=username,
                password=password,
                full_name=full_name,
                email=email,
                phone=phone,
                role=role,
                department=department if department else None,
                office_location=office if office else "Davao District Office"
            )
            
            if user_id > 0:
                QMessageBox.information(self, "Success", f"User '{full_name}' added successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Username already exists!")


# ==================== ADD VIOLATION DIALOG ====================
class AddViolationDialog(QDialog):
    def __init__(self, db_manager, enforcer_id, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.enforcer_id = enforcer_id
        self.setWindowTitle("Record New Violation")
        self.setFixedSize(550, 550)
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("⚠️ RECORD VIOLATION")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #dc2626;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Plate Number
        self.plate_input = self.create_input_field("Plate Number:", "e.g., ABC 1234")
        
        # Violation Type
        vtype_label = QLabel("Violation Type:")
        vtype_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        self.violation_type_combo = QComboBox()
        self.violation_type_combo.setFixedHeight(40)
        self.violation_type_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
        """)
        
        # Load violation types
        self.load_violation_types()
        
        # Location
        self.location_input = self.create_input_field("Location:", "e.g., EDSA-Shaw")
        
        # Date & Time
        date_label = QLabel("Violation Date & Time:")
        date_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        date_time_layout = QHBoxLayout()
        
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setFixedHeight(40)
        self.date_input.setStyleSheet("""
            QDateEdit {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
        """)
        
        self.time_input = self.create_input_field("Time:", "14:30")
        
        date_time_layout.addWidget(self.date_input, stretch=2)
        date_time_layout.addWidget(self.time_input["input"], stretch=1)
        
        # Notes
        notes_label = QLabel("Notes (Optional):")
        notes_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Additional details about the violation...")
        self.notes_input.setFixedHeight(80)
        self.notes_input.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
        """)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setFixedSize(120, 45)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #64748b;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #f1f5f9; }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("RECORD VIOLATION")
        save_btn.setFixedSize(180, 45)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #b91c1c; }
        """)
        save_btn.clicked.connect(self.save_violation)
        
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        
        # Add to layout
        layout.addWidget(title)
        layout.addWidget(self.plate_input["label"])
        layout.addWidget(self.plate_input["input"])
        layout.addWidget(vtype_label)
        layout.addWidget(self.violation_type_combo)
        layout.addWidget(self.location_input["label"])
        layout.addWidget(self.location_input["input"])
        layout.addWidget(date_label)
        layout.addLayout(date_time_layout)
        layout.addWidget(notes_label)
        layout.addWidget(self.notes_input)
        layout.addSpacing(10)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def create_input_field(self, label_text, placeholder):
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setFixedHeight(40)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus { border: 2px solid #1e40af; }
        """)
        
        return {"label": label, "input": input_field}
    
    def load_violation_types(self):
        """Load violation types from database"""
        types = self.db_manager.get_all_violation_types()
        for vtype in types:
            display_text = f"{vtype['violation_name']} (₱{vtype['fine_amount']:,.2f})"
            self.violation_type_combo.addItem(display_text, vtype['type_id'])
    
    def save_violation(self):
        plate = self.plate_input["input"].text().strip().upper()
        violation_type_id = self.violation_type_combo.currentData()
        location = self.location_input["input"].text().strip()
        date_str = self.date_input.date().toString("yyyy-MM-dd")
        time_str = self.time_input["input"].text().strip()
        notes = self.notes_input.toPlainText().strip()
        
        if not all([plate, location, time_str]):
            QMessageBox.warning(self, "Validation Error",
                              "Please fill in all required fields!")
            return
        
        # Combine date and time
        try:
            violation_datetime = f"{date_str} {time_str}:00"
            datetime.strptime(violation_datetime, "%Y-%m-%d %H:%M:%S")
        except:
            QMessageBox.warning(self, "Invalid Time",
                              "Please enter time in HH:MM format (e.g., 14:30)")
            return
        
        violation_id = self.db_manager.add_violation(
            plate_number=plate,
            violation_type_id=violation_type_id,
            enforcer_id=self.enforcer_id,
            location=location,
            violation_date=violation_datetime,
            notes=notes if notes else None
        )
        
        if violation_id > 0:
            QMessageBox.information(self, "Success",
                                  f"Violation recorded successfully!\nPlate: {plate}")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to record violation!")


# ==================== ADD VEHICLE DIALOG ====================
class AddVehicleDialog(QDialog):
    def __init__(self, db_manager, parent=None, vehicle_data=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.vehicle_data = vehicle_data
        self.setWindowTitle("Edit Vehicle" if vehicle_data else "Register New Vehicle")
        self.setFixedSize(560, 720)
        self.setModal(True)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(0)
        
        # Title Section
        title_frame = QFrame()
        title_frame.setStyleSheet("QFrame { background-color: transparent; }")
        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 15)
        
        title_icon = QLabel("🚗" if not self.vehicle_data else "✏️")
        title_icon.setFont(QFont("Arial", 28))
        title_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_text = "EDIT VEHICLE" if self.vehicle_data else "REGISTER VEHICLE"
        title = QLabel(title_text)
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e40af;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title)
        title_frame.setLayout(title_layout)
        layout.addWidget(title_frame)
        
        # Form Container
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame { 
                background-color: white; 
                border-radius: 12px; 
                border: 1px solid #e2e8f0;
            }
        """)
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(10)
        
        # Owner Section
        owner_label = QLabel("👤 Vehicle Owner")
        owner_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        owner_label.setStyleSheet("color: #1e40af; background: transparent; border: none;")
        form_layout.addWidget(owner_label)
        
        owner_col = QVBoxLayout()
        owner_col.setSpacing(5)
        owner_lbl = QLabel("Select Owner")
        owner_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.owner_combo = QComboBox()
        self.owner_combo.setFixedHeight(42)
        self.owner_combo.setStyleSheet(self._combo_style())
        owner_col.addWidget(owner_lbl)
        owner_col.addWidget(self.owner_combo)
        form_layout.addLayout(owner_col)
        
        # Vehicle Info Section
        vehicle_label = QLabel("🚘 Vehicle Information")
        vehicle_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        vehicle_label.setStyleSheet("color: #1e40af; margin-top: 8px; background: transparent; border: none;")
        form_layout.addWidget(vehicle_label)
        
        # Plate Number
        plate_col = QVBoxLayout()
        plate_col.setSpacing(5)
        plate_lbl = QLabel("Plate Number")
        plate_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.plate_input = QLineEdit()
        self.plate_input.setPlaceholderText("e.g., ABC 1234")
        self.plate_input.setFixedHeight(42)
        self.plate_input.setStyleSheet(self._input_style())
        plate_col.addWidget(plate_lbl)
        plate_col.addWidget(self.plate_input)
        form_layout.addLayout(plate_col)
        
        # Make & Model Row
        make_model_row = QHBoxLayout()
        make_model_row.setSpacing(15)
        
        make_col = QVBoxLayout()
        make_col.setSpacing(5)
        make_lbl = QLabel("Make")
        make_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.make_input = QLineEdit()
        self.make_input.setPlaceholderText("e.g., Toyota")
        self.make_input.setFixedHeight(42)
        self.make_input.setStyleSheet(self._input_style())
        make_col.addWidget(make_lbl)
        make_col.addWidget(self.make_input)
        
        model_col = QVBoxLayout()
        model_col.setSpacing(5)
        model_lbl = QLabel("Model")
        model_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("e.g., Vios")
        self.model_input.setFixedHeight(42)
        self.model_input.setStyleSheet(self._input_style())
        model_col.addWidget(model_lbl)
        model_col.addWidget(self.model_input)
        
        make_model_row.addLayout(make_col)
        make_model_row.addLayout(model_col)
        form_layout.addLayout(make_model_row)
        
        # Year & Color Row
        year_color_row = QHBoxLayout()
        year_color_row.setSpacing(15)
        
        year_col = QVBoxLayout()
        year_col.setSpacing(5)
        year_lbl = QLabel("Year")
        year_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.year_input = QSpinBox()
        self.year_input.setRange(1990, 2030)
        self.year_input.setValue(2024)
        self.year_input.setFixedHeight(42)
        self.year_input.setStyleSheet(self._spin_style())
        year_col.addWidget(year_lbl)
        year_col.addWidget(self.year_input)
        
        color_col = QVBoxLayout()
        color_col.setSpacing(5)
        color_lbl = QLabel("Color")
        color_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText("e.g., White")
        self.color_input.setFixedHeight(42)
        self.color_input.setStyleSheet(self._input_style())
        color_col.addWidget(color_lbl)
        color_col.addWidget(self.color_input)
        
        year_color_row.addLayout(year_col)
        year_color_row.addLayout(color_col)
        form_layout.addLayout(year_color_row)
        
        # Registration Section
        reg_label = QLabel("📄 Registration Details")
        reg_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        reg_label.setStyleSheet("color: #1e40af; margin-top: 8px; background: transparent; border: none;")
        form_layout.addWidget(reg_label)
        
        # Chassis & OR/CR Row
        docs_row = QHBoxLayout()
        docs_row.setSpacing(15)
        
        chassis_col = QVBoxLayout()
        chassis_col.setSpacing(5)
        chassis_lbl = QLabel("Chassis Number")
        chassis_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.chassis_input = QLineEdit()
        self.chassis_input.setPlaceholderText("Vehicle chassis no.")
        self.chassis_input.setFixedHeight(42)
        self.chassis_input.setStyleSheet(self._input_style())
        chassis_col.addWidget(chassis_lbl)
        chassis_col.addWidget(self.chassis_input)
        
        or_cr_col = QVBoxLayout()
        or_cr_col.setSpacing(5)
        or_cr_lbl = QLabel("OR/CR Number")
        or_cr_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.or_cr_input = QLineEdit()
        self.or_cr_input.setPlaceholderText("OR-2024-XXXXXX")
        self.or_cr_input.setFixedHeight(42)
        self.or_cr_input.setStyleSheet(self._input_style())
        or_cr_col.addWidget(or_cr_lbl)
        or_cr_col.addWidget(self.or_cr_input)
        
        docs_row.addLayout(chassis_col)
        docs_row.addLayout(or_cr_col)
        form_layout.addLayout(docs_row)
        
        # Registration & Expiry Dates Row
        dates_row = QHBoxLayout()
        dates_row.setSpacing(15)
        
        reg_date_col = QVBoxLayout()
        reg_date_col.setSpacing(5)
        reg_date_lbl = QLabel("Registration Date")
        reg_date_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.reg_date = QDateEdit()
        self.reg_date.setDate(QDate.currentDate())
        self.reg_date.setCalendarPopup(True)
        self.reg_date.setFixedHeight(42)
        self.reg_date.setStyleSheet(self._date_style())
        reg_date_col.addWidget(reg_date_lbl)
        reg_date_col.addWidget(self.reg_date)
        
        exp_date_col = QVBoxLayout()
        exp_date_col.setSpacing(5)
        exp_date_lbl = QLabel("Expiry Date")
        exp_date_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.exp_date = QDateEdit()
        self.exp_date.setDate(QDate.currentDate().addYears(3))
        self.exp_date.setCalendarPopup(True)
        self.exp_date.setFixedHeight(42)
        self.exp_date.setStyleSheet(self._date_style())
        exp_date_col.addWidget(exp_date_lbl)
        exp_date_col.addWidget(self.exp_date)
        
        dates_row.addLayout(reg_date_col)
        dates_row.addLayout(exp_date_col)
        form_layout.addLayout(dates_row)
        
        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        layout.addSpacing(15)
        
        # Load owners now
        self.load_owners()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setFixedSize(130, 45)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #64748b;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #f1f5f9; border-color: #94a3b8; }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("UPDATE VEHICLE" if self.vehicle_data else "REGISTER VEHICLE")
        save_btn.setFixedSize(180, 45)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e40af;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #1e3a8a; }
        """)
        save_btn.clicked.connect(self.save_vehicle)
        
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def _input_style(self):
        return """
            QLineEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus { border: 2px solid #1e40af; background-color: white; }
        """
    
    def _combo_style(self):
        return """
            QComboBox {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox:focus { border: 2px solid #1e40af; }
            QComboBox::drop-down { border: none; width: 30px; }
        """
    
    def _spin_style(self):
        return """
            QSpinBox {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QSpinBox:focus { border: 2px solid #1e40af; background-color: white; }
        """
    
    def _date_style(self):
        return """
            QDateEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QDateEdit:focus { border: 2px solid #1e40af; background-color: white; }
        """
    
    def load_owners(self):
        citizens = self.db_manager.get_all_users(role="citizen")
        for citizen in citizens:
            self.owner_combo.addItem(citizen['full_name'], citizen['user_id'])
            
        if self.vehicle_data:
            # Pre-fill
            self.plate_input.setText(self.vehicle_data.get('plate_number', ''))
            self.plate_input.setReadOnly(True)
            self.make_input.setText(self.vehicle_data.get('make', ''))
            self.model_input.setText(self.vehicle_data.get('model', ''))
            self.year_input.setValue(self.vehicle_data.get('year', 2022))
            self.color_input.setText(self.vehicle_data.get('color', ''))
            self.chassis_input.setText(self.vehicle_data.get('chassis_number', ''))
            self.or_cr_input.setText(self.vehicle_data.get('or_cr_number', ''))
            
            # Dates
            reg = self.vehicle_data.get('registration_date')
            if reg: self.reg_date.setDate(QDate.fromString(str(reg), "yyyy-MM-dd"))
            
            exp = self.vehicle_data.get('expiry_date')
            if exp: self.exp_date.setDate(QDate.fromString(str(exp), "yyyy-MM-dd"))
            
            # Set Owner
            owner_id = self.vehicle_data.get('owner_id')
            idx = self.owner_combo.findData(owner_id)
            if idx >= 0: self.owner_combo.setCurrentIndex(idx)
            self.owner_combo.setEnabled(False)
    
    def save_vehicle(self):
        owner_id = self.owner_combo.currentData()
        plate = self.plate_input.text().strip().upper()
        make = self.make_input.text().strip()
        model = self.model_input.text().strip()
        year = self.year_input.value()
        color = self.color_input.text().strip()
        chassis = self.chassis_input.text().strip()
        or_cr = self.or_cr_input.text().strip()
        reg_date = self.reg_date.date().toString("yyyy-MM-dd")
        exp_date = self.exp_date.date().toString("yyyy-MM-dd")
        
        if not all([plate, make, model, color, chassis, or_cr]):
            QMessageBox.warning(self, "Validation Error",
                              "Please fill in all required fields!")
            return
        
        if self.vehicle_data:
            if self.db_manager.update_vehicle(self.vehicle_data['vehicle_id'], make, model, year, color, reg_date, exp_date):
                QMessageBox.information(self, "Success", "Vehicle updated successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to update vehicle!")
        else:
            vehicle_id = self.db_manager.add_vehicle(
                plate_number=plate,
                owner_id=owner_id,
                make=make,
                model=model,
                year=year,
                color=color,
                chassis_number=chassis,
                registration_date=reg_date,
                expiry_date=exp_date,
                or_cr_number=or_cr
            )
            
            if vehicle_id > 0:
                QMessageBox.information(self, "Success",
                                      f"Vehicle {plate} registered successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error",
                                   "Plate number already exists!")
# ... (keep your existing AddUserDialog, AddViolationDialog, AddVehicleDialog) ...

# ==================== UPDATE STATUS DIALOG ====================
class UpdateStatusDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Update Violation Status")
        self.setFixedSize(450, 380)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(30, 25, 30, 25)
        
        # Title Section
        title_frame = QFrame()
        title_frame.setStyleSheet("QFrame { background-color: transparent; }")
        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 20)
        
        title_icon = QLabel("📝")
        title_icon.setFont(QFont("Arial", 28))
        title_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("UPDATE VIOLATION STATUS")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e40af;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Change the status of a violation record")
        subtitle.setStyleSheet("color: #64748b; font-size: 11px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        title_frame.setLayout(title_layout)
        layout.addWidget(title_frame)
        
        # Form Container
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame { 
                background-color: white; 
                border-radius: 12px; 
                border: 1px solid #e2e8f0;
            }
        """)
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)
        
        # Violation ID Input
        id_col = QVBoxLayout()
        id_col.setSpacing(5)
        id_lbl = QLabel("Violation ID or Citation Number")
        id_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter ID (e.g., 1) or Citation Number")
        self.id_input.setFixedHeight(45)
        self.id_input.setStyleSheet("""
            QLineEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus { border: 2px solid #1e40af; background-color: white; }
        """)
        id_col.addWidget(id_lbl)
        id_col.addWidget(self.id_input)
        form_layout.addLayout(id_col)
        
        # Status Selection
        status_col = QVBoxLayout()
        status_col.setSpacing(5)
        status_lbl = QLabel("New Status")
        status_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["paid", "pending", "cancelled", "overdue"])
        self.status_combo.setFixedHeight(45)
        self.status_combo.setStyleSheet("""
            QComboBox {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox:focus { border: 2px solid #1e40af; }
            QComboBox::drop-down { border: none; width: 30px; }
        """)
        status_col.addWidget(status_lbl)
        status_col.addWidget(self.status_combo)
        form_layout.addLayout(status_col)
        
        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        layout.addSpacing(15)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setFixedSize(120, 45)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #64748b;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #f1f5f9; border-color: #94a3b8; }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("UPDATE STATUS")
        save_btn.setFixedSize(160, 45)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #16a34a;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #15803d; }
        """)
        save_btn.clicked.connect(self.save_status)
        
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
    def save_status(self):
        v_id = self.id_input.text().strip()
        status = self.status_combo.currentText()
        
        if not v_id:
            QMessageBox.warning(self, "Error", "Please enter a Violation ID or Citation Number.")
            return
        
        if not v_id.isdigit():
            QMessageBox.warning(self, "Error", "Please enter a numeric Violation ID for now.")
            return

        if self.db_manager.update_violation_status(int(v_id), status):
            QMessageBox.information(self, "Success", f"Violation #{v_id} status updated to '{status.upper()}'")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to update status. Please check the ID.")

class AddViolationTypeDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Add New Violation Type")
        self.setFixedSize(480, 480)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(30, 25, 30, 25)
        
        # Title Section
        title_frame = QFrame()
        title_frame.setStyleSheet("QFrame { background-color: transparent; }")
        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 20)
        
        title_icon = QLabel("⚠️")
        title_icon.setFont(QFont("Arial", 28))
        title_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("ADD VIOLATION TYPE")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #f59e0b;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Create a new violation category")
        subtitle.setStyleSheet("color: #64748b; font-size: 11px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        title_frame.setLayout(title_layout)
        layout.addWidget(title_frame)
        
        # Form Container
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame { 
                background-color: white; 
                border-radius: 12px; 
                border: 1px solid #e2e8f0;
            }
        """)
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(12)
        
        # Violation Name
        name_col = QVBoxLayout()
        name_col.setSpacing(5)
        name_lbl = QLabel("Violation Name *")
        name_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Over Speeding")
        self.name_input.setFixedHeight(42)
        self.name_input.setStyleSheet(self._input_style())
        name_col.addWidget(name_lbl)
        name_col.addWidget(self.name_input)
        form_layout.addLayout(name_col)
        
        # Fine & Points Row
        fine_points_row = QHBoxLayout()
        fine_points_row.setSpacing(15)
        
        fine_col = QVBoxLayout()
        fine_col.setSpacing(5)
        fine_lbl = QLabel("Fine Amount (₱) *")
        fine_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.fine_input = QLineEdit()
        self.fine_input.setPlaceholderText("e.g., 500.00")
        self.fine_input.setFixedHeight(42)
        self.fine_input.setStyleSheet(self._input_style())
        fine_col.addWidget(fine_lbl)
        fine_col.addWidget(self.fine_input)
        
        points_col = QVBoxLayout()
        points_col.setSpacing(5)
        points_lbl = QLabel("Penalty Points")
        points_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.points_input = QSpinBox()
        self.points_input.setRange(0, 20)
        self.points_input.setValue(1)
        self.points_input.setFixedHeight(42)
        self.points_input.setStyleSheet("""
            QSpinBox {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QSpinBox:focus { border: 2px solid #f59e0b; background-color: white; }
        """)
        points_col.addWidget(points_lbl)
        points_col.addWidget(self.points_input)
        
        fine_points_row.addLayout(fine_col, stretch=2)
        fine_points_row.addLayout(points_col, stretch=1)
        form_layout.addLayout(fine_points_row)
        
        # Description
        desc_col = QVBoxLayout()
        desc_col.setSpacing(5)
        desc_lbl = QLabel("Description")
        desc_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; background: transparent; border: none;")
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Brief description of the violation...")
        self.desc_input.setFixedHeight(80)
        self.desc_input.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QTextEdit:focus { border: 2px solid #f59e0b; background-color: white; }
        """)
        desc_col.addWidget(desc_lbl)
        desc_col.addWidget(self.desc_input)
        form_layout.addLayout(desc_col)
        
        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        layout.addSpacing(15)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setFixedSize(120, 45)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #64748b;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #f1f5f9; border-color: #94a3b8; }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("SAVE VIOLATION TYPE")
        save_btn.setFixedSize(180, 45)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #f59e0b;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #d97706; }
        """)
        save_btn.clicked.connect(self.save_type)
        
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def _input_style(self):
        return """
            QLineEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus { border: 2px solid #f59e0b; background-color: white; }
        """

    def save_type(self):
        name = self.name_input.text().strip()
        fine = self.fine_input.text().strip()
        desc = self.desc_input.toPlainText().strip()
        points = self.points_input.value()
        
        if not name or not fine:
            QMessageBox.warning(self, "Validation Error", "Violation Name and Fine Amount are required!")
            return
            
        try:
            fine_val = float(fine)
            if fine_val <= 0:
                raise ValueError("Fine must be positive")
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Fine Amount must be a valid positive number!")
            return
            
        if self.db_manager.add_violation_type(name, fine_val, desc, points):
            QMessageBox.information(self, "Success", f"Violation Type '{name}' added successfully!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to add violation type. Name might already exist.")

class ManageViolationTypesDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Manage Violation Types")
        self.setFixedSize(600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Existing Violation Types")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        add_btn = QPushButton("+ Add New Type")
        add_btn.clicked.connect(self.open_add_dialog)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Fine", "Points", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        self.load_types()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)


    def load_types(self):
        types = self.db_manager.get_all_violation_types()
        self.table.setRowCount(len(types))
        for row, t in enumerate(types):
            self.table.setItem(row, 0, QTableWidgetItem(t['violation_name']))
            self.table.setItem(row, 1, QTableWidgetItem(f"₱{t['fine_amount']:,.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(str(t['penalty_points'])))
            self.table.setItem(row, 3, QTableWidgetItem(t['description']))

    def open_add_dialog(self):
        dialog = AddViolationTypeDialog(self.db_manager, self)
        if dialog.exec():
            self.load_types()

class GenerateReportsDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Generate Reports")
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Date Range
        layout.addWidget(QLabel("Date Range:"))
        date_layout = QHBoxLayout()
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        
        date_layout.addWidget(QLabel("From:"))
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(QLabel("To:"))
        date_layout.addWidget(self.end_date)
        layout.addLayout(date_layout)
        
        # Status Filter
        layout.addWidget(QLabel("Filter by Status:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["All", "Paid", "Pending", "Cancelled"])
        layout.addWidget(self.status_combo)
        
        # Export Button
        export_btn = QPushButton("📄 Export to CSV")
        export_btn.setFixedHeight(45)
        export_btn.setStyleSheet("background-color: #16a34a; color: white; font-weight: bold; border-radius: 5px;")
        export_btn.clicked.connect(self.export_csv)
        layout.addWidget(export_btn)
        
        self.setLayout(layout)

    def export_csv(self):
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.end_date.date().toString("yyyy-MM-dd")
        status = self.status_combo.currentText().lower()
        
        # Fetch data (we might need a new method in db_manager or filter here)
        # For simplicity, let's fetch all and filter here
        violations = self.db_manager.get_all_violations()
        
        filtered = []
        for v in violations:
            v_date = str(v['violation_date']).split()[0]
            if start <= v_date <= end:
                if status == "all" or v['status'].lower() == status:
                    filtered.append(v)
        
        if not filtered:
            QMessageBox.information(self, "No Data", "No records found for the selected criteria.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "CSV Files (*.csv)")
        if filename:
            try:
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    # Header
                    writer.writerow(["Citation", "Plate", "Violation", "Location", "Date", "Fine", "Status", "Enforcer"])
                    # Rows
                    for row in filtered:
                        writer.writerow([
                            row.get('citation_number', ''),
                            row['plate_number'],
                            row.get('violation_name', ''),
                            row['location'],
                            row['violation_date'],
                            row['fine_amount'],
                            row['status'],
                            row.get('enforcer_name', '')
                        ])
                QMessageBox.information(self, "Success", f"Report saved to {filename}")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")




