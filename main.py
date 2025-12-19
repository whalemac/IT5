import sys
import traceback
from datetime import datetime
import mysql.connector
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox, QLabel, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
from PyQt6.QtCore import Qt

# Import UIs
from views.ui_login import LoginWindow       
from views.ui_admin import AdminDashboard
from views.ui_enforcer import EnforcerDashboard
from views.ui_citizen import CitizenDashboard

# Import Database
from models.database import DatabaseManager

# Import Dialogs
from controllers.admin_dialogs import (AddUserDialog, AddViolationDialog, AddVehicleDialog, 
                          UpdateStatusDialog, ManageViolationTypesDialog, 
                          AddViolationTypeDialog, GenerateReportsDialog)
from controllers.enforcer_dialogs import RecordViolationDialog, SearchVehicleDialog, UpdateDetailsDialog
from controllers.citizen_dialogs import PaymentDialog, HelpSupportDialog, CheckStatusDialog, EditProfileDialog

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nexus Monitor System")
        self.setGeometry(100, 50, 1300, 750)
        
        # Initialize database
        print("  - Connecting to database...")
        try:
            self.db = DatabaseManager()
            print("✓ Database initialized successfully")
        except mysql.connector.Error as e:
            print(f"✗ Database connection error: {e}")
            print("  Please ensure MySQL server is running and credentials are correct.")
            traceback.print_exc()
            # Continue anyway - user can still see the error
            self.db = None
        except Exception as e:
            print(f"✗ Database initialization error: {e}")
            traceback.print_exc()
            self.db = None
        
        self.current_user = None
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Show Login
        print("  - Initializing login window...")
        try:
            self.login_screen = LoginWindow()
            self.stack.addWidget(self.login_screen)
            self.stack.setCurrentWidget(self.login_screen)
            self.login_screen.login_btn.clicked.connect(self.handle_login)
            print("✓ Login window initialized")
        except Exception as e:
            print(f"✗ Error initializing login window: {e}")
            traceback.print_exc()
            # Create a simple error message widget
            error_label = QLabel(f"Error initializing application:\n{e}")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stack.addWidget(error_label)
    
    def handle_login(self):
        try:
            username = self.login_screen.username_input.text().strip()
            password = self.login_screen.password_input.text().strip()
            role = self.login_screen.role_combo.currentText()
            
            if not username or not password:
                QMessageBox.warning(self, "Login Failed", "Please enter username and password!")
                return
            
            if not self.db:
                QMessageBox.critical(self, "Database Error", 
                    "Database connection failed!\n\nPlease ensure:\n"
                    "1. MySQL server is running\n"
                    "2. Database credentials are correct\n"
                    "3. Check console for error details")
                return
            
            role_mapping = {"Admin": "admin", "Traffic Enforcer": "enforcer", "Citizen": "citizen"}
            db_role = role_mapping.get(role, role.lower())
            
            print(f"  - Attempting login for: {username} ({db_role})")
            user = self.db.authenticate_user(username, password)
            
            if user:
                if user['role'] == db_role:
                    self.current_user = user
                    print(f"✓ Login successful: {user['full_name']} ({user['role']})")
                    
                    try:
                        if db_role == "admin": 
                            self.open_admin_dashboard()
                        elif db_role == "enforcer": 
                            self.open_enforcer_dashboard()
                        elif db_role == "citizen": 
                            self.open_citizen_dashboard()
                        else:
                            QMessageBox.warning(self, "Error", f"Unknown role: {db_role}")
                    except Exception as dash_error:
                        print(f"✗ Error opening dashboard: {dash_error}")
                        traceback.print_exc()
                        QMessageBox.critical(self, "Dashboard Error", 
                            f"Failed to open dashboard:\n{dash_error}\n\nCheck console for details.")
                else:
                    QMessageBox.warning(self, "Login Failed", 
                        f"Role mismatch! Selected: {role}\nAccount role: {user['role']}")
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password!")
        except Exception as e:
            print(f"✗ Login error: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Login Error", f"An error occurred during login:\n{e}")

    # =========================================================
    #  ENFORCER DASHBOARD LOGIC
    # =========================================================
    def open_enforcer_dashboard(self):
        try:
            print("  - Opening Enforcer Dashboard...")
            if not self.db:
                raise Exception("Database connection not available")
            
            self.enforcer_dashboard = EnforcerDashboard(
                user_name=self.current_user.get('full_name', 'Officer'),
                user_dept=self.current_user.get('department') or "Traffic Div",
                user_office=self.current_user.get('office_location') or "Davao District Office"
            )
            self.enforcer_dashboard.db_manager = self.db
            self.enforcer_dashboard.current_user = self.current_user
            
            # Connect Buttons
            self.connect_enforcer_buttons()

            # Wire callbacks for manage table
            self.enforcer_dashboard.edit_violation_callback = self.handle_edit_violation
            self.enforcer_dashboard.delete_violation_callback = self.handle_delete_violation
            
            # Load Data
            self.refresh_enforcer_data()
            
            self.stack.addWidget(self.enforcer_dashboard)
            self.stack.setCurrentWidget(self.enforcer_dashboard)
            print("✓ Enforcer Dashboard opened successfully")
            
        except Exception as e:
            print(f"✗ Error opening enforcer dashboard: {e}")
            traceback.print_exc()
            raise  # Re-raise to be caught by handle_login

    def connect_enforcer_buttons(self):
        try:
            # Sidebar
            if hasattr(self.enforcer_dashboard, 'logout_btn'):
                self.enforcer_dashboard.logout_btn.clicked.connect(self.handle_logout)
            if hasattr(self.enforcer_dashboard, 'btn_record'):
                self.enforcer_dashboard.btn_record.clicked.connect(self.open_record_violation)
            if hasattr(self.enforcer_dashboard, 'btn_search'):
                self.enforcer_dashboard.btn_search.clicked.connect(self.open_search_vehicle)
            if hasattr(self.enforcer_dashboard, 'btn_manage'):
                self.enforcer_dashboard.btn_manage.clicked.connect(self.enforcer_dashboard.show_manage)
            
            # Dashboard Actions (Quick Actions)
            if hasattr(self.enforcer_dashboard, 'qa_record'):
                self.enforcer_dashboard.qa_record.clicked.connect(self.open_record_violation)
            if hasattr(self.enforcer_dashboard, 'qa_search'):
                self.enforcer_dashboard.qa_search.clicked.connect(self.open_search_vehicle)
            if hasattr(self.enforcer_dashboard, 'qa_update'):
                self.enforcer_dashboard.qa_update.clicked.connect(self.open_update_details)
        except Exception as e:
            print(f"  ⚠ Error connecting enforcer buttons: {e}")

    def refresh_enforcer_data(self):
        if not hasattr(self, 'enforcer_dashboard'): return
        if not self.db: return
        
        try:
            # Update Dashboard Stats and Tables
            if hasattr(self.enforcer_dashboard, 'update_stats'):
                self.enforcer_dashboard.update_stats()
            
            all_violations = self.db.get_all_violations()
            # Filter recent 20 for the dashboard table
            recent = sorted(all_violations, key=lambda x: str(x.get('violation_date', '')), reverse=True)[:20]
            if hasattr(self.enforcer_dashboard, 'populate_recent_table'):
                self.enforcer_dashboard.populate_recent_table(recent)
            
            # Refresh Manage Table if on that page
            if hasattr(self.enforcer_dashboard, 'refresh_manage_table'):
                self.enforcer_dashboard.refresh_manage_table()
        except Exception as e:
            print(f"  ⚠ Error refreshing enforcer data: {e}")

    # --- ENFORCER DIALOGS ---
    def open_record_violation(self):
        dialog = RecordViolationDialog(self.db, self.current_user['user_id'], self.enforcer_dashboard)
        if dialog.exec():
            self.refresh_enforcer_data()

    def open_search_vehicle(self):
        dialog = SearchVehicleDialog(self.db, self.enforcer_dashboard)
        dialog.exec()

    def open_update_details(self):
        dialog = UpdateDetailsDialog(self.db, self.enforcer_dashboard)
        if dialog.exec():
            self.refresh_enforcer_data()

    def open_generate_reports(self):
        # Determine which dashboard is active
        parent = None
        if hasattr(self, 'admin_dashboard'):
            parent = self.admin_dashboard
        elif hasattr(self, 'enforcer_dashboard'):
            parent = self.enforcer_dashboard
        
        dialog = GenerateReportsDialog(self.db, parent if parent else self)
        dialog.exec()

    def handle_edit_violation(self, violation_data):
        dialog = RecordViolationDialog(self.db, self.current_user['user_id'], self.enforcer_dashboard, violation_data)
        if dialog.exec():
            self.refresh_enforcer_data()

    def handle_delete_violation(self, violation_id):
        reply = QMessageBox.question(self.enforcer_dashboard, "Confirm Delete", 
                                   "Are you sure you want to delete this violation record?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.db.delete_violation(violation_id):
                self.refresh_enforcer_data()
            else:
                QMessageBox.warning(self.enforcer_dashboard, "Error", "Failed to delete violation.")

    # =========================================================
    #  ADMIN DASHBOARD LOGIC
    # =========================================================
    def open_admin_dashboard(self):
        try:
            print("  - Opening Admin Dashboard...")
            if not self.db:
                raise Exception("Database connection not available")
            
            self.admin_dashboard = AdminDashboard(
                user_name=self.current_user.get('full_name', 'Administrator'),
                user_dept=self.current_user.get('department') or "Administration",
                user_office=self.current_user.get('office_location') or "Davao District Office"
            )
            self.admin_dashboard.db_manager = self.db
            self.admin_dashboard.current_user = self.current_user
            
            self.connect_admin_buttons()
            
            # Override Callbacks
            self.admin_dashboard.edit_user_callback = self.handle_edit_user
            self.admin_dashboard.delete_user_callback = self.handle_delete_user
            self.admin_dashboard.edit_vehicle_callback = self.handle_edit_vehicle
            self.admin_dashboard.delete_vehicle_callback = self.handle_delete_vehicle
            
            self.refresh_admin_dashboard()
            
            self.stack.addWidget(self.admin_dashboard)
            self.stack.setCurrentWidget(self.admin_dashboard)
            print("✓ Admin Dashboard opened successfully")
        except Exception as e:
            print(f"✗ Error opening admin dashboard: {e}")
            traceback.print_exc()
            raise  # Re-raise to be caught by handle_login

    def connect_admin_buttons(self):
        try:
            # Connect ALL logout buttons from all pages
            if hasattr(self.admin_dashboard, 'logout_buttons'):
                for logout_btn in self.admin_dashboard.logout_buttons:
                    logout_btn.clicked.connect(self.handle_logout)
            elif hasattr(self.admin_dashboard, 'logout_btn'):
                self.admin_dashboard.logout_btn.clicked.connect(self.handle_logout)
            
            # Navigation
            if hasattr(self.admin_dashboard, 'btn_dashboard'):
                self.admin_dashboard.btn_dashboard.clicked.connect(self.admin_dashboard.show_dashboard)
            if hasattr(self.admin_dashboard, 'btn_manage_users'):
                self.admin_dashboard.btn_manage_users.clicked.connect(self.admin_dashboard.show_users)
            if hasattr(self.admin_dashboard, 'btn_manage_vehicles'):
                self.admin_dashboard.btn_manage_vehicles.clicked.connect(self.admin_dashboard.show_vehicles)
            
            # Page Specific Actions
            # Dashboard Shortcuts
            if hasattr(self.admin_dashboard, 'btn_add_user'):
                self.admin_dashboard.btn_add_user.clicked.connect(self.open_add_user_dialog)
            if hasattr(self.admin_dashboard, 'btn_add_vehicle'):
                self.admin_dashboard.btn_add_vehicle.clicked.connect(self.open_add_vehicle_dialog)
            
            # User Page Add Button
            if hasattr(self.admin_dashboard, 'btn_add_user_page'):
                self.admin_dashboard.btn_add_user_page.clicked.connect(self.open_add_user_dialog)
            
            if hasattr(self.admin_dashboard, 'btn_view_all_violations'):
                self.admin_dashboard.btn_view_all_violations.clicked.connect(self.open_view_all_violations_dialog)
            
            # Page Specific Actions
            if hasattr(self.admin_dashboard, 'btn_add_vehicle_page'):
                self.admin_dashboard.btn_add_vehicle_page.clicked.connect(self.open_add_vehicle_dialog)
            
            if hasattr(self.admin_dashboard, 'btn_update_status_table'):
                self.admin_dashboard.btn_update_status_table.clicked.connect(self.open_update_status_dialog)
            if hasattr(self.admin_dashboard, 'btn_manage_types'):
                self.admin_dashboard.btn_manage_types.clicked.connect(self.open_manage_types_dialog)
            if hasattr(self.admin_dashboard, 'btn_add_type'):
                self.admin_dashboard.btn_add_type.clicked.connect(self.open_add_type_dialog)
            if hasattr(self.admin_dashboard, 'btn_reports'):
                self.admin_dashboard.btn_reports.clicked.connect(self.open_generate_reports)
            if hasattr(self.admin_dashboard, 'btn_refresh_expiration'):
                self.admin_dashboard.btn_refresh_expiration.clicked.connect(self.refresh_vehicle_expiration)
            if hasattr(self.admin_dashboard, 'btn_refresh_exp_dashboard'):
                self.admin_dashboard.btn_refresh_exp_dashboard.clicked.connect(self.refresh_vehicle_expiration)
        except Exception as e:
            print(f"  ⚠ Error connecting admin buttons: {e}")
            traceback.print_exc()
    
    def refresh_vehicle_expiration(self):
        """Refresh vehicle expiration status and update dashboard"""
        if hasattr(self, 'admin_dashboard') and self.admin_dashboard:
            self.admin_dashboard.refresh_expiration_tracking()
            self.admin_dashboard.refresh_vehicle_table()

    def open_add_user_dialog(self):
        dialog = AddUserDialog(self.db, self.admin_dashboard)
        if dialog.exec(): 
            self.admin_dashboard.refresh_user_table()
            self.admin_dashboard.update_stats()

    def handle_edit_user(self, user_data):
        dialog = AddUserDialog(self.db, self.admin_dashboard, user_data)
        if dialog.exec():
            self.admin_dashboard.refresh_user_table()

    def handle_delete_user(self, user_id):
        reply = QMessageBox.question(self.admin_dashboard, "Confirm Delete", 
                                   "Are you sure you want to delete this user?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.db.delete_user(user_id):
                self.admin_dashboard.refresh_user_table()
                self.admin_dashboard.update_stats()
            else:
                QMessageBox.warning(self.admin_dashboard, "Error", "Failed to delete user.")

    def open_add_vehicle_dialog(self):
        dialog = AddVehicleDialog(self.db, self.admin_dashboard)
        if dialog.exec(): 
            self.admin_dashboard.refresh_vehicle_table()
            self.admin_dashboard.update_stats()

    def handle_edit_vehicle(self, vehicle_data):
        dialog = AddVehicleDialog(self.db, self.admin_dashboard, vehicle_data)
        if dialog.exec():
            self.admin_dashboard.refresh_vehicle_table()

    def handle_delete_vehicle(self, vehicle_id):
        reply = QMessageBox.question(self.admin_dashboard, "Confirm Delete", 
                                   "Are you sure you want to delete this vehicle?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.db.delete_vehicle(vehicle_id):
                self.admin_dashboard.refresh_vehicle_table()
                self.admin_dashboard.update_stats()
            else:
                QMessageBox.warning(self.admin_dashboard, "Error", "Failed to delete vehicle.")
    

    def open_update_status_dialog(self):
        dialog = UpdateStatusDialog(self.db, self.admin_dashboard)
        if dialog.exec(): self.refresh_violation_tables()

    def open_manage_types_dialog(self):
        dialog = ManageViolationTypesDialog(self.db, self.admin_dashboard)
        dialog.exec()

    def open_add_type_dialog(self):
        dialog = AddViolationTypeDialog(self.db, self.admin_dashboard)
        dialog.exec()
        
    def open_view_all_violations_dialog(self):
        dialog = QDialog(self.admin_dashboard)
        dialog.setWindowTitle("All Violations")
        dialog.setFixedSize(900, 600)
        layout = QVBoxLayout()
        
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Plate", "Violation", "Date", "Status"])
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        violations = self.db.get_all_violations()
        table.setRowCount(len(violations))
        
        for row, v in enumerate(violations):
            table.setItem(row, 0, QTableWidgetItem(str(v.get('citation_number', ''))))
            table.setItem(row, 1, QTableWidgetItem(v['plate_number']))
            table.setItem(row, 2, QTableWidgetItem(v['violation_name']))
            table.setItem(row, 3, QTableWidgetItem(str(v['violation_date'])))
            
            status = v['status'].upper()
            status_item = QTableWidgetItem(status)
            if status == "PAID": status_item.setForeground(Qt.GlobalColor.green)
            else: status_item.setForeground(Qt.GlobalColor.red)
            table.setItem(row, 4, status_item)
            
        layout.addWidget(table)
        
        cls_btn = QPushButton("CLOSE")
        cls_btn.setFixedSize(100, 40)
        cls_btn.clicked.connect(dialog.accept)
        layout.addWidget(cls_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        dialog.setLayout(layout)
        dialog.exec()

    def refresh_admin_dashboard(self):
        if not self.db or not hasattr(self, 'admin_dashboard'):
            return
        try:
            if hasattr(self.admin_dashboard, 'update_stats'):
                self.admin_dashboard.update_stats()
            self.refresh_violation_tables()
            if hasattr(self.admin_dashboard, 'refresh_user_table'):
                self.admin_dashboard.refresh_user_table()
            if hasattr(self.admin_dashboard, 'refresh_vehicle_table'):
                self.admin_dashboard.refresh_vehicle_table()
        except Exception as e:
            print(f"  ⚠ Error refreshing admin dashboard: {e}")

    def refresh_violation_tables(self):
        if not self.db:
            return
        try:
            violations = self.db.get_all_violations()
            if hasattr(self.admin_dashboard, 'populate_violation_table'):
                self.admin_dashboard.populate_violation_table(violations)
        except Exception as e:
            print(f"  ⚠ Error refreshing violation tables: {e}")

    # =========================================================
    #  CITIZEN / SHARED
    # =========================================================
    # =========================================================
    #  CITIZEN / SHARED
    # =========================================================
    def open_citizen_dashboard(self):
        try:
            print("  - Opening Citizen Dashboard...")
            if not self.db:
                raise Exception("Database connection not available")
            
            # New Signature: user_data, db_manager
            self.citizen_dashboard = CitizenDashboard(self.current_user, self.db)
            self.citizen_dashboard.logout_btn.clicked.connect(self.handle_logout)
            
            # Connect Quick Actions
            if hasattr(self.citizen_dashboard, 'btn_qa_payment'):
                self.citizen_dashboard.btn_qa_payment.clicked.connect(self.open_citizen_payment)
            if hasattr(self.citizen_dashboard, 'btn_qa_help'):
                self.citizen_dashboard.btn_qa_help.clicked.connect(self.open_citizen_help)
            if hasattr(self.citizen_dashboard, 'btn_qa_check'):
                self.citizen_dashboard.btn_qa_check.clicked.connect(self.open_citizen_check_status)
            if hasattr(self.citizen_dashboard, 'btn_qa_edit'):
                self.citizen_dashboard.btn_qa_edit.clicked.connect(self.open_citizen_edit_profile)
            
            if hasattr(self.citizen_dashboard, 'btn_refresh'):
                self.citizen_dashboard.btn_refresh.clicked.connect(self.citizen_dashboard.update_dashboard)

            self.stack.addWidget(self.citizen_dashboard)
            self.stack.setCurrentWidget(self.citizen_dashboard)
            print("✓ Citizen Dashboard opened successfully")
            
        except Exception as e:
            print(f"✗ Error opening citizen dashboard: {e}")
            traceback.print_exc()
            raise  # Re-raise to be caught by handle_login

    def open_citizen_payment(self):
        # We need the user_id. Citizen Dashboard has user_data, but accessing from Main is safer/direct
        dialog = PaymentDialog(self.db, self.current_user['user_id'], self.citizen_dashboard)
        if dialog.exec():
            self.citizen_dashboard.update_dashboard()

    def open_citizen_help(self):
        dialog = HelpSupportDialog(self.citizen_dashboard)
        dialog.exec()
        
    def open_citizen_check_status(self):
        dialog = CheckStatusDialog(self.db, self.current_user['user_id'], self.citizen_dashboard)
        dialog.exec()
        
    def open_citizen_edit_profile(self):
        dialog = EditProfileDialog(self.db, self.current_user, self.citizen_dashboard)
        if dialog.exec():
            # Update current user data from DB to reflect changes immediately in UI
            try:
                conn = self.db.connect()
                if conn:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("SELECT * FROM users WHERE user_id=%s", (self.current_user['user_id'],))
                    updated_user = cursor.fetchone()
                    cursor.close()
                    conn.close()
                    
                    if updated_user:
                        self.current_user = updated_user
                        # Update dashboard UI elements without recreating
                        if hasattr(self, 'citizen_dashboard'):
                            self.citizen_dashboard.user_data = updated_user
                            self.citizen_dashboard.user_name = updated_user.get('full_name', 'GUEST')
                            # Refresh welcome message and header
                            self.citizen_dashboard.update_dashboard()
            except Exception as e:
                print(f"Error refreshing user data: {e}")
                traceback.print_exc()
        
    def open_view_all_violations_dialog(self):
        # reuse ReportsDialog or create a simple table dialog
        # For now, let's use the Dashboard's violation table by showing dashboard and ensuring it's populated?
        # No, user wants specific action. Let's make a quick dialog here or import one.
        # Check if we have one. We don't. Let's make a simple one or just show a message if not critical.
        # BETTER: Re-use GenerateReportsDialog but that's for reports. 
        # Actually, let's just make a QDialog with a QTableWidget on the fly.
        dialog = QDialog(self.admin_dashboard)
        dialog.setWindowTitle("All Violations")
        dialog.setFixedSize(900, 600)
        layout = QVBoxLayout()
        
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Plate", "Violation", "Date", "Status"])
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        violations = self.db.get_all_violations()
        table.setRowCount(len(violations))
        for row, v in enumerate(violations):
            table.setItem(row, 0, QTableWidgetItem(str(v['citation_number'])))
            table.setItem(row, 1, QTableWidgetItem(v['plate_number']))
            table.setItem(row, 2, QTableWidgetItem(v['violation_name']))
            table.setItem(row, 3, QTableWidgetItem(str(v['violation_date'])))
            table.setItem(row, 4, QTableWidgetItem(v['status'].upper()))
            
        layout.addWidget(table)
        cls_btn = QPushButton("CLOSE")
        cls_btn.clicked.connect(dialog.accept)
        layout.addWidget(cls_btn)
        dialog.setLayout(layout)
        dialog.exec()

    def refresh_citizen_dashboard(self):
        # Deprecated logic, sticking to internal update_dashboard
        if hasattr(self, 'citizen_dashboard'):
            self.citizen_dashboard.update_dashboard()



    def handle_logout(self):
        reply = QMessageBox.question(self, 'Logout', "Are you sure you want to logout?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.current_user = None
            self.login_screen.password_input.clear()
            self.login_screen.username_input.clear()
            while self.stack.count() > 1:
                widget = self.stack.widget(1)
                self.stack.removeWidget(widget)
                widget.deleteLater()
            self.stack.setCurrentWidget(self.login_screen)

if __name__ == '__main__':
    try:
        print("=" * 50)
        print("Nexus Monitor System - Starting...")
        print("=" * 50)
        
        app = QApplication(sys.argv)
        print("✓ QApplication created")
        
        window = MainApp()
        print("✓ Main window initialized")
        
        window.show()
        print("✓ Application window displayed")
        print("=" * 50)
        print("Application is running. Close the window to exit.")
        print("=" * 50)
        
        sys.exit(app.exec())
    except Exception as e:
        print(f"\n✗ ERROR: Application failed to start!")
        print(f"Error: {e}")
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)