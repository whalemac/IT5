import sys
import json
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QLineEdit, QMessageBox, QFrame, QScrollArea,
                             QWidget)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor

class PaymentDialog(QDialog):
    def __init__(self, db_manager, user_id, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user_id = user_id
        self.setWindowTitle("Make Payment")
        self.setFixedSize(500, 500)
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("💳 SECURE PAYMENT")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e40af;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Select Violation
        self.violation_combo = QComboBox()
        self.violation_combo.setFixedHeight(40)
        self.violation_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
            }
        """)
        self.violation_combo.currentIndexChanged.connect(self.update_amount)
        
        # Payment Method
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GCash", "Maya", "Credit Card", "Bank Transfer"])
        self.method_combo.setFixedHeight(40)
        self.method_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
            }
        """)
        self.method_combo.currentIndexChanged.connect(self.build_extra_fields)
        
        # Amount
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter Amount")
        self.amount_input.setFixedHeight(40)
        self.amount_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
            }
        """)
        self.amount_input.setReadOnly(True)

        # Extra fields container (method-specific)
        from PyQt6.QtWidgets import QFormLayout
        self.extra_container = QFrame()
        self.extra_layout = QFormLayout()
        self.extra_layout.setContentsMargins(5, 10, 5, 10)
        self.extra_layout.setSpacing(15)
        self.extra_container.setLayout(self.extra_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        confirm_btn = QPushButton("PROCEED PAYMENT")
        confirm_btn.setFixedHeight(45)
        confirm_btn.setStyleSheet("background-color: #16a34a; color: white; font-weight: bold; border-radius: 8px;")
        confirm_btn.clicked.connect(self.process_payment)
        
        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setFixedHeight(45)
        cancel_btn.setStyleSheet("background-color: #cbd5e1; color: #475569; font-weight: bold; border-radius: 8px;")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(confirm_btn)
        
        layout.addWidget(title)
        layout.addWidget(QLabel("Select Violation:"))
        layout.addWidget(self.violation_combo)
        layout.addWidget(QLabel("Payment Method:"))
        layout.addWidget(self.method_combo)
        layout.addWidget(QLabel("Amount (PHP):"))
        layout.addWidget(self.amount_input)
        layout.addWidget(self.extra_container)
        layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Load violations and update amount after all widgets are created
        self.load_pending_violations()
        self.update_amount()
        self.build_extra_fields()
    
    def load_pending_violations(self):
        violations = self.db_manager.get_violations_by_owner(self.user_id)
        # Filter pending
        self.pending = [v for v in violations if v['status'].lower() == 'pending']
        
        if not self.pending:
            self.violation_combo.addItem("No pending violations", None)
            self.amount_input.setEnabled(False)
        else:
            for v in self.pending:
                self.violation_combo.addItem(f"{v['violation_name']} - ₱{v['fine_amount']:,.2f}", v)

    def update_amount(self):
        data = self.violation_combo.currentData()
        if data:
            self.amount_input.setText(str(data['fine_amount']))
        else:
            self.amount_input.clear()

    def clear_extra_fields(self):
        while self.extra_layout.count():
            item = self.extra_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def build_extra_fields(self):
        self.clear_extra_fields()
        self.extra_inputs = {}
        method = self.method_combo.currentText()
        
    def build_extra_fields(self):
        self.clear_extra_fields()
        self.extra_inputs = {}
        method = self.method_combo.currentText()
        
        # Helper to create styled input
        def create_input(placeholder):
            edit = QLineEdit()
            edit.setPlaceholderText(placeholder)
            edit.setFixedHeight(40)
            edit.setStyleSheet("""
                QLineEdit {
                    background: white; 
                    border: 2px solid #e2e8f0; 
                    border-radius: 6px; 
                    padding: 0 12px;
                    font-size: 14px;
                }
                QLineEdit:focus { border: 2px solid #3b82f6; }
            """)
            return edit

        def add_row(label_text, widget):
            lbl = QLabel(label_text)
            lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            lbl.setStyleSheet("color: #334155;")
            self.extra_layout.addRow(lbl, widget)
            return widget

        if method in ["GCash", "Maya"]:
            self.extra_inputs["mobile"] = add_row("Mobile Number:", create_input("09XXXXXXXXX"))
            self.extra_inputs["reference"] = add_row("Reference No.:", create_input("(Optional)"))
            
        elif method == "Credit Card":
            self.extra_inputs["card_number"] = add_row("Card Number:", create_input("#### #### #### ####"))
            self.extra_inputs["card_name"] = add_row("Cardholder Name:", create_input("As shown on card"))
            
            # Group Expiry and CVV
            row_widget = QWidget()
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(10)
            
            exp_input = create_input("MM/YY")
            cvv_input = create_input("CVV")
            
            row_layout.addWidget(exp_input)
            row_layout.addWidget(cvv_input)
            row_widget.setLayout(row_layout)
            
            # Add with a combined label
            lbl = QLabel("Expiry / CVV:")
            lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            lbl.setStyleSheet("color: #334155;")
            self.extra_layout.addRow(lbl, row_widget)
            
            self.extra_inputs["card_expiry"] = exp_input
            self.extra_inputs["card_cvv"] = cvv_input
            
        elif method == "Bank Transfer":
            self.extra_inputs["bank_name"] = add_row("Bank Name:", create_input("e.g., BPI / BDO"))
            self.extra_inputs["account_no"] = add_row("Account Number:", create_input("########"))
            self.extra_inputs["reference"] = add_row("Reference No.:", create_input(""))

    def process_payment(self):
        data = self.violation_combo.currentData()
        if not data:
            QMessageBox.warning(self, "Error", "No violation selected")
            return
            
        try:
            amount = float(self.amount_input.text().strip())
            if amount < data['fine_amount']:
                 QMessageBox.warning(self, "Error", "Amount cannot be less than the fine.")
                 return
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount!")
            return

        # Validate method-specific fields
        method = self.method_combo.currentText()
        if method in ["GCash", "Maya"]:
            mobile = self.extra_inputs.get("mobile").text().strip()
            if not mobile or len(mobile) < 10:
                QMessageBox.warning(self, "Error", "Please enter a valid mobile number.")
                return
        elif method == "Credit Card":
            for key in ["card_number", "card_name", "card_expiry", "card_cvv"]:
                if not self.extra_inputs.get(key).text().strip():
                    QMessageBox.warning(self, "Error", "Please fill in all card details.")
                    return
        elif method == "Bank Transfer":
            if not self.extra_inputs.get("bank_name").text().strip() or not self.extra_inputs.get("account_no").text().strip():
                QMessageBox.warning(self, "Error", "Please provide bank name and account number.")
                return

        # Collect payment details based on method
        payment_details = {}
        transaction_ref = None
        
        # Helper for safe text access
        def get_text(key):
            widget = self.extra_inputs.get(key)
            return widget.text().strip() if widget else ""

        if method in ["GCash", "Maya"]:
            payment_details = {
                "mobile_number": get_text("mobile"),
                "reference": get_text("reference") or None
            }
            transaction_ref = payment_details.get("reference")
        elif method == "Credit Card":
            payment_details = {
                "card_number": get_text("card_number")[-4:],
                "card_name": get_text("card_name"),
                "card_expiry": get_text("card_expiry")
            }
            # Only generate ref if we have a card number
            cn = payment_details['card_number']
            transaction_ref = f"CC-{cn}" if cn else f"CC-{QDate.currentDate().toString('yyyyMMdd')}"
            
        elif method == "Bank Transfer":
            payment_details = {
                "bank_name": get_text("bank_name"),
                "account_number": get_text("account_no")[-4:],
                "reference": get_text("reference") or None
            }
            transaction_ref = payment_details.get("reference")
        
        payment_details_json = json.dumps(payment_details) if payment_details else None
        
        success = self.db_manager.record_payment(
            violation_id=data['violation_id'],
            amount=amount,
            method=method,
            user_id=self.user_id,
            payment_details=payment_details_json,
            transaction_ref=transaction_ref
        )
        
        if success:
            QMessageBox.information(self, "Success", f"Payment of ₱{amount:,.2f} processed successfully!\nTransaction: {transaction_ref or 'Pending confirmation'}")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Payment failed. Please try again.")

class HelpSupportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help & Support")
        self.setFixedSize(400, 300)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        title = QLabel("Need Assistance?")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info = QLabel(
            "For inquiries and concerns, please contact our support team:\n\n"
            "📞 Hotline: (02) 8-123-4567\n"
            "📧 Email: support@nexus-monitor.gov.ph\n"
            "🏢 Office: LTO Main Office, SM Echoland, Davao City\n\n"
            "Office Hours: Mon-Fri, 8:00 AM - 5:00 PM"
        )
        info.setFont(QFont("Arial", 11))
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        close_btn = QPushButton("CLOSE")
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet("background-color: #1e40af; color: white; border-radius: 5px; font-weight: bold;")
        close_btn.clicked.connect(self.accept)
        
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addStretch()
        layout.addWidget(close_btn)
        self.setLayout(layout)

class CheckStatusDialog(QDialog):
    def __init__(self, db_manager, user_id, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user_id = user_id
        self.setWindowTitle("Violation Status Check")
        self.setFixedSize(560, 620)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        title = QLabel("MY VIOLATION STATUS")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #1e40af;")
        layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        content = QFrame()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)
        
        violations = self.db_manager.get_violations_by_owner(self.user_id)
        
        if not violations:
            lbl = QLabel("No violations found. Drive safely! 🚗")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #16a34a; font-size: 14px; margin-top: 50px;")
            content_layout.addWidget(lbl)
        else:
            for v in violations:
                card = QFrame()
                card.setStyleSheet("""
                    QFrame {
                        background-color: white;
                        border: 1px solid #e2e8f0;
                        border-radius: 12px;
                        padding: 14px;
                    }
                """)
                card_layout = QVBoxLayout()
                card_layout.setSpacing(6)
                
                h_top = QHBoxLayout()
                v_name = QLabel(v['violation_name'])
                v_name.setFont(QFont("Arial", 12, QFont.Weight.Bold))
                
                status_lbl = QLabel(v['status'].upper())
                status_lbl.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                if v['status'] == 'paid':
                    status_lbl.setStyleSheet("color: #16a34a; background: #dcfce7; padding: 4px 10px; border-radius: 8px;")
                elif v['status'] == 'pending':
                    status_lbl.setStyleSheet("color: #dc2626; background: #fee2e2; padding: 4px 10px; border-radius: 8px;")
                else:
                    status_lbl.setStyleSheet("color: #f59e0b; background: #fef3c7; padding: 4px 10px; border-radius: 8px;")
                     
                h_top.addWidget(v_name)
                h_top.addStretch()
                h_top.addWidget(status_lbl)
                
                details = QLabel(f"Plate: {v['plate_number']}  •  Date: {v['violation_date']}")
                details.setStyleSheet("color: #475569; font-size: 11px;")

                payment = v.get('payment_date')
                payment_txt = f"Payment Date: {payment}" if payment else "Payment Date: -"
                location_txt = f"Location: {v.get('location','-')}"
                extra = QLabel(f"{location_txt}  •  {payment_txt}")
                extra.setStyleSheet("color: #64748b; font-size: 10px;")
                
                card_layout.addLayout(h_top)
                card_layout.addWidget(details)
                card_layout.addWidget(extra)
                card.setLayout(card_layout)
                content_layout.addWidget(card)
                
        content_layout.addStretch()
        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        close_btn = QPushButton("CLOSE")
        close_btn.setFixedHeight(45)
        close_btn.setStyleSheet("background-color: #1e40af; color: white; border-radius: 8px; font-weight: bold;")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class EditProfileDialog(QDialog):
    def __init__(self, db_manager, user_data, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user_data = user_data
        self.setWindowTitle("Edit Profile")
        self.setFixedSize(450, 550)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("✏️ EDIT PROFILE")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e40af;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Full Name
        self.name_input = self.create_input("Full Name:", self.user_data.get('full_name', ''))
        layout.addWidget(self.name_input['label'])
        layout.addWidget(self.name_input['input'])

        # Email
        self.email_input = self.create_input("Email Address:", self.user_data.get('email', ''))
        layout.addWidget(self.email_input['label'])
        layout.addWidget(self.email_input['input'])

        # Phone
        self.phone_input = self.create_input("Phone Number:", self.user_data.get('phone', ''))
        layout.addWidget(self.phone_input['label'])
        layout.addWidget(self.phone_input['input'])

        # Password (Optional)
        self.pass_input = self.create_input("New Password (Optional):", "")
        self.pass_input['input'].setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input['input'].setPlaceholderText("Leave blank to keep current")
        layout.addWidget(self.pass_input['label'])
        layout.addWidget(self.pass_input['input'])

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("SAVE CHANGES")
        save_btn.setFixedHeight(45)
        save_btn.setStyleSheet("background-color: #1e40af; color: white; border-radius: 8px; font-weight: bold;")
        save_btn.clicked.connect(self.save_profile)

        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setFixedHeight(45)
        cancel_btn.setStyleSheet("background-color: #cbd5e1; color: #475569; border-radius: 8px; font-weight: bold;")
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def create_input(self, label_text, value):
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        label.setStyleSheet("color: #64748b;")
        
        inp = QLineEdit()
        inp.setText(str(value) if value else "")
        inp.setFixedHeight(40)
        inp.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 0 10px;
                background-color: white;
            }
            QLineEdit:focus { border-color: #1e40af; }
        """)
        return {'label': label, 'input': inp}

    def save_profile(self):
        full_name = self.name_input['input'].text().strip()
        email = self.email_input['input'].text().strip()
        phone = self.phone_input['input'].text().strip()
        password = self.pass_input['input'].text().strip()

        if not full_name:
            QMessageBox.warning(self, "Error", "Full Name is required!")
            return

        # Update Info
        dept = self.user_data.get('department')
        office = self.user_data.get('office_location')
        
        success = self.db_manager.update_user(self.user_data['user_id'], full_name, email, phone, dept, office)
        
        pass_success = True
        if password:
             pass_success = self.db_manager.update_user_password(self.user_data['user_id'], password)

        if success and pass_success:
            QMessageBox.information(self, "Success", "Profile updated successfully!")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to update profile.")
