from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QComboBox, QMessageBox, QTextEdit, QDateEdit)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont
from datetime import datetime

# --- 1. RECORD VIOLATION DIALOG ---
class RecordViolationDialog(QDialog):
    def __init__(self, db_manager, enforcer_id, parent=None, violation_data=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.enforcer_id = enforcer_id
        self.violation_data = violation_data
        self.setWindowTitle("Update Violation" if violation_data else "Record New Violation")
        self.setFixedSize(500, 650)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Header
        title = QLabel("📝 NEW VIOLATION REPORT" if not self.violation_data else "✏️ UPDATE VIOLATION")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #dc2626;")
        layout.addWidget(title)
        
        # Inputs
        layout.addWidget(self.label("Vehicle Plate Number:"))
        self.plate_input = QLineEdit()
        self.plate_input.setPlaceholderText("e.g. ABC 1234")
        self.plate_input.setFixedHeight(42)
        self.plate_input.setStyleSheet("padding: 10px; border: 2px solid #e2e8f0; border-radius: 8px; background: white;")
        layout.addWidget(self.plate_input)
        
        layout.addWidget(self.label("Violation Type:"))
        self.type_combo = QComboBox()
        self.type_combo.setFixedHeight(42)
        self.type_combo.setStyleSheet("padding: 10px; border: 2px solid #e2e8f0; border-radius: 8px; background: white;")
        self.load_violation_types()
        layout.addWidget(self.type_combo)
        
        layout.addWidget(self.label("Location of Incident:"))
        self.loc_input = QLineEdit()
        self.loc_input.setPlaceholderText("Street, City, Landmark")
        self.loc_input.setFixedHeight(42)
        self.loc_input.setStyleSheet("padding: 10px; border: 2px solid #e2e8f0; border-radius: 8px; background: white;")
        layout.addWidget(self.loc_input)
        
        layout.addWidget(self.label("Notes / Remarks:"))
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Driver behavior, weather conditions, etc.")
        self.notes_input.setStyleSheet("padding: 10px; border: 2px solid #e2e8f0; border-radius: 8px; background: white;")
        self.notes_input.setFixedHeight(90)
        layout.addWidget(self.notes_input)
        
        # Submit Button
        btn = QPushButton("SUBMIT REPORT")
        btn.setFixedHeight(48)
        btn.setStyleSheet("""
            QPushButton { background-color: #dc2626; color: white; font-weight: bold; border-radius: 8px; }
            QPushButton:hover { background-color: #b91c1c; }
        """)
        btn.clicked.connect(self.submit)
        layout.addWidget(btn)
        
        if self.violation_data:
             # Pre-fill for edit
             self.plate_input.setText(self.violation_data.get('plate_number', ''))
             self.plate_input.setReadOnly(True) # Prevent changing plate during edit usually
             
             # Set type
             # We need to find the index for the type_id
             # Helper lookup:
             index = self.type_combo.findData(self.violation_data.get('violation_type_id'))
             if index >= 0: self.type_combo.setCurrentIndex(index)
             
             self.loc_input.setText(self.violation_data.get('location', ''))
             self.notes_input.setText(self.violation_data.get('notes', ''))
             
             # Status Combo for editing
             layout.addWidget(self.label("Status:"))
             self.status_combo = QComboBox()
             self.status_combo.addItems(["PENDING", "PAID", "OVERDUE", "CONTESTED"])
             self.status_combo.setCurrentText(self.violation_data.get('status', 'PENDING').upper())
             self.status_combo.setFixedHeight(42)
             self.status_combo.setStyleSheet("padding: 10px; border: 2px solid #e2e8f0; border-radius: 8px; background: white;")
             layout.addWidget(self.status_combo)
             
             btn.setText("UPDATE VIOLATION")
        else:
             self.status_combo = None

        self.setLayout(layout)

    def label(self, text):
        l = QLabel(text)
        l.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        l.setStyleSheet("color: #334155;")
        return l

    def load_violation_types(self):
        types = self.db_manager.get_all_violation_types()
        for t in types:
            # Display: "No Helmet (₱1,500)"
            self.type_combo.addItem(f"{t['violation_name']} (₱{t['fine_amount']:,.2f})", t['type_id'])

    def submit(self):
        plate = self.plate_input.text().strip().upper()
        v_type_id = self.type_combo.currentData()
        location = self.loc_input.text().strip()
        notes = self.notes_input.toPlainText().strip()
        
        if not plate or not location:
            QMessageBox.warning(self, "Missing Info", "Plate Number and Location are required!")
            return

        if self.violation_data:
            # UPDATE LOGIC
            status = self.status_combo.currentText().lower()
            success = self.db_manager.update_violation(
                self.violation_data['violation_id'],
                location,
                notes,
                status,
                violation_type_id=v_type_id
            )
            if success:
                QMessageBox.information(self, "Success", "Violation updated successfully.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to update violation.")
        else:
            # INSERT LOGIC
            # 1. Validation: Check if vehicle exists
            vehicle = self.db_manager.search_vehicle(plate)
            if not vehicle:
                reply = QMessageBox.question(self, "Vehicle Not Found", 
                                           f"Vehicle with plate '{plate}' is not registered in the system.\nDo you want to proceed anyway?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.No:
                    return
    
            # Current Timestamp
            violation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save to Database
            result = self.db_manager.add_violation(
                plate_number=plate,
                violation_type_id=v_type_id,
                enforcer_id=self.enforcer_id,
                location=location,
                violation_date=violation_date,
                notes=notes
            )
            
            if result > 0:
                QMessageBox.information(self, "Success", "Violation has been recorded and sent to the system.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Database Error: Could not save violation.")

# --- 2. SEARCH VEHICLE DIALOG ---
class SearchVehicleDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Search Vehicle Database")
        self.setFixedSize(520, 520)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(25, 20, 25, 20)
        
        title = QLabel("🔍 SEARCH VEHICLE DATABASE")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e40af;")
        layout.addWidget(title)

        layout.addWidget(QLabel("ENTER PLATE NUMBER:"))
        
        self.input = QLineEdit()
        self.input.setPlaceholderText("ABC 123")
        self.input.setStyleSheet("font-size: 16px; padding: 10px; border: 2px solid #1e40af; border-radius: 8px; background: white;")
        layout.addWidget(self.input)
        
        btn = QPushButton("SEARCH DATABASE")
        btn.setFixedHeight(40)
        btn.setStyleSheet("background-color: #1e40af; color: white; font-weight: bold; border-radius: 8px;")
        btn.clicked.connect(self.search)
        layout.addWidget(btn)
        
        self.result_lbl = QLabel("Results will appear here...")
        self.result_lbl.setWordWrap(True)
        self.result_lbl.setStyleSheet("background-color: white; padding: 15px; border-radius: 10px; color: #333; border: 1px solid #e2e8f0;")
        self.result_lbl.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.result_lbl.setMinimumHeight(260)
        layout.addWidget(self.result_lbl)
        
        self.setLayout(layout)
        
    def search(self):
        plate = self.input.text().strip().upper()
        # Use new full search method
        data = self.db_manager.search_vehicle_full(plate)
        vehicle = data.get("vehicle")
        violations = data.get("violations", [])
        
        if vehicle:
            text = (f"✅ <b>VEHICLE FOUND</b><br>"
                    f"<b>Plate:</b> {vehicle['plate_number']}<br>"
                    f"<b>Owner:</b> {vehicle['owner_name']}<br>"
                    f"<b>Model:</b> {vehicle['color']} {vehicle['make']} {vehicle['model']}<br>"
                    f"<b>Expiry:</b> {vehicle['expiry_date']}<br>"
                    f"<b>Contact:</b> {vehicle.get('owner_phone','N/A')}<br><br>"
                    f"<b>⚠️ VIOLATION HISTORY:</b><br>")
            
            if violations:
                for v in violations:
                    status = v['status'].upper()
                    if status == "PAID":
                        status_color = "green"
                    elif status == "PENDING":
                        status_color = "#dc2626"
                    else:
                        status_color = "#f59e0b"
                    date_txt = v['violation_date'].strftime('%Y-%m-%d') if hasattr(v['violation_date'], 'strftime') else v['violation_date']
                    text += (f"• {v['violation_name']} @ {v['location']} "
                             f"({date_txt}) - <span style='color:{status_color}'>{status}</span><br>")
            else:
                text += "<i>No violations recorded.</i>"
                
            self.result_lbl.setText(text)
        else:
            self.result_lbl.setText(f"❌ No record found for <b>{plate}</b>")

# --- 3. UPDATE DETAILS DIALOG ---
class UpdateDetailsDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Update Violation Details")
        self.setFixedSize(520, 520)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(25, 20, 25, 20)

        title = QLabel("✏️ UPDATE VIOLATION DETAILS")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e40af;")
        layout.addWidget(title)

        layout.addWidget(QLabel("PLATE NUMBER:"))
        self.plate_input = QLineEdit()
        self.plate_input.setPlaceholderText("ABC 1234")
        self.plate_input.setFixedHeight(42)
        self.plate_input.setStyleSheet("padding: 10px; border: 2px solid #e2e8f0; border-radius: 8px; background: white;")
        layout.addWidget(self.plate_input)

        self.search_btn = QPushButton("LOAD VIOLATIONS")
        self.search_btn.setFixedHeight(40)
        self.search_btn.setStyleSheet("background-color: #1e40af; color: white; font-weight: bold; border-radius: 8px;")
        self.search_btn.clicked.connect(self.load_violations)
        layout.addWidget(self.search_btn)

        self.vio_combo = QComboBox()
        self.vio_combo.setFixedHeight(42)
        self.vio_combo.setStyleSheet("padding: 10px; border: 2px solid #e2e8f0; border-radius: 8px; background: white;")
        self.vio_combo.currentIndexChanged.connect(self.prefill_fields)
        layout.addWidget(QLabel("SELECT VIOLATION:"))
        layout.addWidget(self.vio_combo)

        layout.addWidget(QLabel("VIOLATION TYPE:"))
        self.type_combo = QComboBox()
        self.type_combo.setFixedHeight(42)
        self.type_combo.setStyleSheet("padding: 10px; border: 2px solid #e2e8f0; border-radius: 8px; background: white;")
        layout.addWidget(self.type_combo)

        layout.addWidget(QLabel("STATUS:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["PENDING", "PAID", "OVERDUE", "CONTESTED"])
        self.status_combo.setFixedHeight(42)
        self.status_combo.setStyleSheet("padding: 10px; border: 2px solid #e2e8f0; border-radius: 8px; background: white;")
        layout.addWidget(self.status_combo)

        layout.addWidget(QLabel("CORRECTED LOCATION:"))
        self.loc_input = QLineEdit()
        self.loc_input.setFixedHeight(42)
        self.loc_input.setStyleSheet("padding: 10px; border: 2px solid #e2e8f0; border-radius: 8px; background: white;")
        layout.addWidget(self.loc_input)

        layout.addWidget(QLabel("ADDITIONAL NOTES:"))
        self.note_input = QTextEdit()
        self.note_input.setStyleSheet("padding: 10px; border: 2px solid #e2e8f0; border-radius: 8px; background: white;")
        self.note_input.setFixedHeight(90)
        layout.addWidget(self.note_input)

        btn = QPushButton("UPDATE RECORD")
        btn.setFixedHeight(48)
        btn.setStyleSheet("background-color: #16a34a; color: white; font-weight: bold; border-radius: 8px;")
        btn.clicked.connect(self.update)
        layout.addWidget(btn)

        self.setLayout(layout)
        self.violations = []
        self.load_violation_types()

    def load_violation_types(self):
        self.type_combo.clear()
        types = self.db_manager.get_all_violation_types()
        for t in types:
            self.type_combo.addItem(f"{t['violation_name']} (₱{t['fine_amount']:,.0f})", t['type_id'])

    def load_violations(self):
        plate = self.plate_input.text().strip().upper()
        if not plate:
            QMessageBox.warning(self, "Required", "Please enter a plate number.")
            return
        data = self.db_manager.search_vehicle_full(plate)
        self.violations = data.get("violations", [])
        self.vio_combo.clear()
        if not self.violations:
            QMessageBox.information(self, "No Records", f"No violations found for {plate}.")
            return
        for v in self.violations:
            label = f"{v.get('citation_number','N/A')} - {v['violation_name']} ({v['status'].upper()})"
            self.vio_combo.addItem(label, v['violation_id'])
        self.prefill_fields()

    def prefill_fields(self):
        if not self.violations or self.vio_combo.currentIndex() < 0:
            return
        vid = self.vio_combo.currentData()
        current = next((v for v in self.violations if v.get('violation_id') == vid), None)
        if not current:
            return
        self.loc_input.setText(current.get('location', ''))
        self.note_input.setText(current.get('notes', ''))
        self.status_combo.setCurrentText(current.get('status', 'pending').upper())
        idx = self.type_combo.findData(current.get('violation_type_id'))
        if idx >= 0:
            self.type_combo.setCurrentIndex(idx)

    def update(self):
        if not self.violations or self.vio_combo.currentIndex() < 0:
            QMessageBox.warning(self, "Select Violation", "Please load and select a violation to update.")
            return
        violation_id = self.vio_combo.currentData()
        loc = self.loc_input.text().strip()
        note = self.note_input.toPlainText().strip()
        status = self.status_combo.currentText().lower()
        v_type_id = self.type_combo.currentData()

        if not loc:
            QMessageBox.warning(self, "Required", "Location cannot be empty.")
            return

        if self.db_manager.update_violation(violation_id, loc, note, status, violation_type_id=v_type_id):
            QMessageBox.information(self, "Success", "Record updated successfully.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Update failed.")