import mysql.connector
import hashlib
from datetime import datetime
from typing import Optional, Dict, List, Tuple

class DatabaseManager:
    def __init__(self, host="localhost", user="root", password="", database="nexus_db"):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.create_tables()
        self.seed_initial_data()

    def connect(self):
        try:
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as e:
            if e.errno == 1049: # Unknown database
                print(f"  - Database '{self.config['database']}' not found, creating...")
                # Create database
                temp_config = self.config.copy()
                del temp_config["database"]
                try:
                    conn = mysql.connector.connect(**temp_config)
                    cursor = conn.cursor()
                    cursor.execute(f"CREATE DATABASE {self.config['database']}")
                    cursor.close()
                    conn.close()
                    print(f"  ✓ Database '{self.config['database']}' created")
                    return mysql.connector.connect(**self.config)
                except Exception as create_err:
                    print(f"  ✗ Error creating database: {create_err}")
                    return None
            elif e.errno == 2003:  # Can't connect to MySQL server
                print(f"  ✗ Cannot connect to MySQL server. Is MySQL running?")
                print(f"     Error: {e}")
                return None
            else:
                print(f"  ✗ Error connecting to database: {e}")
                return None
        except Exception as e:
            print(f"  ✗ Unexpected database error: {e}")
            return None

    def create_tables(self):
        print("  - Creating database tables...")
        conn = self.connect()
        if not conn: 
            print("  ⚠ Could not connect to database")
            return
        cursor = conn.cursor()
        
        try:
            # 1. USERS TABLE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    role ENUM('admin', 'enforcer', 'citizen') NOT NULL,
                    department VARCHAR(100),
                    office_location VARCHAR(100),
                    status VARCHAR(20) DEFAULT 'active',
                    last_login DATETIME,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 2. VEHICLES TABLE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vehicles (
                    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
                    plate_number VARCHAR(20) UNIQUE NOT NULL,
                    owner_id INT NOT NULL,
                    make VARCHAR(50),
                    model VARCHAR(50),
                    year INT,
                    color VARCHAR(30),
                    chassis_number VARCHAR(50) UNIQUE,
                    registration_date DATE,
                    expiry_date DATE,
                    or_cr_number VARCHAR(50) UNIQUE,
                    status ENUM('active', 'expired', 'expiring') DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (owner_id) REFERENCES users(user_id)
                )
            """)
            
            # Add status column if it doesn't exist (for existing databases)
            try:
                cursor.execute("ALTER TABLE vehicles ADD COLUMN status ENUM('active', 'expired', 'expiring') DEFAULT 'active'")
                print("  - Added status column to vehicles table")
            except mysql.connector.Error:
                pass  # Column already exists

            # 3. VIOLATION TYPES TABLE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS violation_types (
                    type_id INT AUTO_INCREMENT PRIMARY KEY,
                    violation_name VARCHAR(100) UNIQUE NOT NULL,
                    fine_amount DECIMAL(10, 2) NOT NULL,
                    description TEXT,
                    penalty_points INT DEFAULT 0,
                    status VARCHAR(20) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 4. VIOLATIONS TABLE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS violations (
                    violation_id INT AUTO_INCREMENT PRIMARY KEY,
                    citation_number VARCHAR(50) UNIQUE,
                    plate_number VARCHAR(20) NOT NULL,
                    vehicle_id INT,
                    violation_type_id INT NOT NULL,
                    enforcer_id INT NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    violation_date DATETIME NOT NULL,
                    fine_amount DECIMAL(10, 2) NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    notes TEXT,
                    photo_evidence TEXT,
                    payment_date TIMESTAMP NULL,
                    payment_method VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
                    FOREIGN KEY (violation_type_id) REFERENCES violation_types(type_id),
                    FOREIGN KEY (enforcer_id) REFERENCES users(user_id)
                )
            """)

            # 5. OFFICERS TABLE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS officers (
                    officer_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT UNIQUE NOT NULL,
                    badge_number VARCHAR(50) UNIQUE NOT NULL,
                    assigned_area VARCHAR(100),
                    duty_status VARCHAR(20) DEFAULT 'off-duty',
                    shift_start TIME,
                    shift_end TIME,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)

            # 6. PAYMENTS TABLE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    payment_id INT AUTO_INCREMENT PRIMARY KEY,
                    violation_id INT NOT NULL,
                    user_id INT NOT NULL,
                    amount DECIMAL(10, 2) NOT NULL,
                    payment_method VARCHAR(50) NOT NULL,
                    payment_details TEXT,
                    transaction_reference VARCHAR(100),
                    status VARCHAR(20) DEFAULT 'completed',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (violation_id) REFERENCES violations(violation_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)

            conn.commit()
            print("  ✓ Tables verified")
        except Exception as e:
            print(f"  ⚠ Error creating tables: {e}")
        finally:
            cursor.close()
            conn.close()

    def seed_initial_data(self):
        """Insert initial data - with better error handling"""
        print("  - Checking initial data...")
        conn = self.connect()
        if not conn: 
            print("  ⚠ Cannot seed data - no connection")
            return
        
        cursor = conn.cursor(dictionary=True)

        try:
            def get_user_id(username: str) -> Optional[int]:
                cursor.execute("SELECT user_id FROM users WHERE username=%s", (username,))
                row = cursor.fetchone()
                return row['user_id'] if row else None

            print("  - Seeding initial data...")

            # USERS
            admin_id = get_user_id("admin")
            if not admin_id:
                admin_pass = self.hash_password("admin123")
                cursor.execute("""
                    INSERT INTO users (username, password, full_name, email, role, department, office_location) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, ("admin", admin_pass, "System Administrator", "admin@lto.gov.ph", "admin", "IT Department", "Davao District Office"))
                admin_id = cursor.lastrowid

            enforcer_id = get_user_id("enforcer01")
            if not enforcer_id:
                enf_pass = self.hash_password("enforcer123")
                cursor.execute("""
                    INSERT INTO users (username, password, full_name, email, phone, role, department, office_location) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, ("enforcer01", enf_pass, "Officer Juan Santos", "juan@lto.gov.ph", "09171234567", "enforcer", "Traffic Enforcement", "Davao District Office"))
                enforcer_id = cursor.lastrowid

            # OFFICER RECORD (only if missing)
            if enforcer_id:
                cursor.execute("SELECT officer_id FROM officers WHERE user_id=%s", (enforcer_id,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO officers (user_id, badge_number, assigned_area, duty_status) 
                        VALUES (%s, %s, %s, %s)
                    """, (enforcer_id, "OFF-2024-001", "EDSA-Shaw", "on-duty"))

            citizen_id = get_user_id("juandelacruz")
            if not citizen_id:
                cit_pass = self.hash_password("citizen123")
                cursor.execute("""
                    INSERT INTO users (username, password, full_name, email, phone, role, office_location) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, ("juandelacruz", cit_pass, "Juan Dela Cruz", "juan@email.com", "09181234567", "citizen", "Davao District Office"))
                citizen_id = cursor.lastrowid

            # VEHICLE (only if missing)
            if citizen_id:
                cursor.execute("SELECT vehicle_id FROM vehicles WHERE plate_number=%s", ("ABC 1234",))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO vehicles (plate_number, owner_id, make, model, year, color, chassis_number, registration_date, expiry_date, or_cr_number)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, ("ABC 1234", citizen_id, "Toyota", "Vios", 2022, "White", "ABC123XYZ", "2022-01-15", "2025-01-15", "OR-2022-123"))
                    vehicle_id = cursor.lastrowid
                else:
                    vehicle_id = cursor.fetchone()
                    vehicle_id = vehicle_id['vehicle_id'] if isinstance(vehicle_id, dict) else vehicle_id
            else:
                vehicle_id = None

            # VIOLATION TYPES (insert missing only)
            cursor.execute("SELECT violation_name FROM violation_types")
            existing_types = {row['violation_name'] for row in cursor.fetchall()}
            v_types = [
                ("Overspeeding", 3500.00, "Exceeding speed limit", 3),
                ("No Helmet", 1500.00, "Riding without helmet", 2),
                ("Illegal Parking", 500.00, "No parking zone", 1),
                ("Red Light Violation", 5000.00, "Running red light", 3),
                ("Drunk Driving", 10000.00, "Driving under influence", 5)
            ]
            for v in v_types:
                if v[0] not in existing_types:
                    cursor.execute("""
                        INSERT INTO violation_types (violation_name, fine_amount, description, penalty_points) 
                        VALUES (%s, %s, %s, %s)
                    """, v)

            # Sample Violation (only if data exists and citation missing)
            if vehicle_id and enforcer_id:
                cursor.execute("SELECT violation_id FROM violations WHERE citation_number=%s", ("CIT-2024-001",))
                if not cursor.fetchone():
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute("""
                        INSERT INTO violations (plate_number, vehicle_id, violation_type_id, enforcer_id, location, violation_date, fine_amount, status, citation_number)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, ("ABC 1234", vehicle_id, 2, enforcer_id, "EDSA", now, 1500.00, "pending", "CIT-2024-001"))

            conn.commit()
            print("  ✓ Initial data seeded/verified")

        except Exception as e:
            print(f"  ⚠ Error seeding data: {e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    # ==================== AUTHENTICATION ====================
    def authenticate_user(self, username, password) -> Optional[Dict]:
        conn = self.connect()
        if not conn: return None
        cursor = conn.cursor(dictionary=True)
        
        hashed = self.hash_password(password)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s AND status='active'", (username, hashed))
        user = cursor.fetchone()
        
        if user:
            cursor.execute("UPDATE users SET last_login=NOW() WHERE user_id=%s", (user['user_id'],))
            conn.commit()
            
        cursor.close()
        conn.close()
        return user

    # ==================== USER MANAGEMENT ====================
    def add_user(self, username, password, full_name, email, phone, role, department=None, office_location=None) -> int:
        conn = self.connect()
        if not conn: return -1
        cursor = conn.cursor()
        hashed = self.hash_password(password)
        try:
            cursor.execute("""
                INSERT INTO users (username, password, full_name, email, phone, role, department, office_location)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (username, hashed, full_name, email, phone, role, department, office_location))
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as e:
            print(f"Error adding user: {e}")
            return -1
        finally:
            cursor.close()
            conn.close()

    def get_all_users(self, role=None) -> List[Dict]:
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            if role:
                cursor.execute("SELECT * FROM users WHERE role=%s ORDER BY created_at DESC", (role,))
            else:
                cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
            return cursor.fetchall()
        except:
            return []
        finally:
            cursor.close()
            conn.close()

    # ==================== VEHICLE MANAGEMENT ====================
    def add_vehicle(self, plate_number, owner_id, make, model, year, color, chassis_number, registration_date, expiry_date, or_cr_number) -> int:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            from datetime import date, timedelta
            today = date.today()
            expiring_threshold = today + timedelta(days=30)
            
            # Determine initial status based on expiry_date
            if expiry_date and expiry_date < today:
                initial_status = 'expired'
            elif expiry_date and expiry_date <= expiring_threshold:
                initial_status = 'expiring'
            else:
                initial_status = 'active'
            
            cursor.execute("""
                INSERT INTO vehicles (plate_number, owner_id, make, model, year, color, chassis_number, registration_date, expiry_date, or_cr_number, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (plate_number, owner_id, make, model, year, color, chassis_number, registration_date, expiry_date, or_cr_number, initial_status))
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as e:
            print(f"Error adding vehicle: {e}")
            return -1
        finally:
            cursor.close()
            conn.close()

    def search_vehicle(self, plate_number) -> Optional[Dict]:
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT v.*, u.full_name as owner_name, u.phone as owner_phone 
                FROM vehicles v 
                JOIN users u ON v.owner_id = u.user_id 
                WHERE v.plate_number = %s
            """, (plate_number,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_vehicles_by_owner(self, owner_id) -> List[Dict]:
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM vehicles WHERE owner_id=%s ORDER BY created_at DESC", (owner_id,))
            return cursor.fetchall()
        except:
            return []
        finally:
            cursor.close()
            conn.close()

    # ==================== VIOLATION MANAGEMENT ====================
    def add_violation_type(self, name, fine, description, points) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO violation_types (violation_name, fine_amount, description, penalty_points)
                VALUES (%s, %s, %s, %s)
            """, (name, fine, description, points))
            conn.commit()
            return True
        except:
            return False
        finally:
            cursor.close()
            conn.close()

    def get_all_violation_types(self) -> List[Dict]:
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM violation_types WHERE status='active'")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def add_violation(self, plate_number, violation_type_id, enforcer_id, location, violation_date, notes=None) -> int:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            # Get vehicle info
            vehicle = self.search_vehicle(plate_number)
            vehicle_id = vehicle['vehicle_id'] if vehicle else None
            
            # Get violation type info
            cursor.execute("SELECT fine_amount FROM violation_types WHERE type_id=%s", (violation_type_id,))
            res = cursor.fetchone()
            fine = res[0] if res else 0
            
            # Generate Citation
            citation = f"CIT-{datetime.now().strftime('%Y%m%d')}-{int(datetime.now().timestamp())}"
            
            cursor.execute("""
                INSERT INTO violations (citation_number, plate_number, vehicle_id, violation_type_id, enforcer_id, location, violation_date, fine_amount, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (citation, plate_number, vehicle_id, violation_type_id, enforcer_id, location, violation_date, fine, notes))
            
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding violation: {e}")
            return -1
        finally:
            cursor.close()
            conn.close()

    def get_all_violations(self) -> List[Dict]:
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT v.*, vt.violation_name, vt.penalty_points, u.full_name as enforcer_name 
                FROM violations v
                JOIN violation_types vt ON v.violation_type_id = vt.type_id
                JOIN users u ON v.enforcer_id = u.user_id
                ORDER BY v.violation_date DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_violations_by_owner(self, owner_id) -> List[Dict]:
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT v.*, vt.violation_name 
                FROM violations v
                JOIN vehicles veh ON v.vehicle_id = veh.vehicle_id
                JOIN violation_types vt ON v.violation_type_id = vt.type_id
                WHERE veh.owner_id = %s
                ORDER BY v.violation_date DESC
            """, (owner_id,))
            return cursor.fetchall()
        except:
            return []
        finally:
            cursor.close()
            conn.close()

    def update_violation_status(self, violation_id, status) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            if status == 'paid':
                cursor.execute("UPDATE violations SET status=%s, payment_date=NOW() WHERE violation_id=%s", (status, violation_id))
            else:
                cursor.execute("UPDATE violations SET status=%s WHERE violation_id=%s", (status, violation_id))
            conn.commit()
            return True
        except:
            return False
        finally:
            cursor.close()
            conn.close()

    def update_violation_details(self, citation, location, notes) -> bool:
        """Allow Enforcer to update location or notes"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE violations SET location=%s, notes=%s WHERE citation_number=%s", (location, notes, citation))
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
        except: return False
        finally:
            cursor.close()
            conn.close()

    # ==================== ANALYTICS & DASHBOARD ====================
    def get_dashboard_stats(self) -> Dict:
        """Get counts for dashboard display"""
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        stats = {
            "users": 0,
            "enforcers": 0,
            "vehicles": 0,
            "violations": 0,
            "fines": 0.0,
            "pending_violations": 0
        }
        try:
            # Users
            cursor.execute("SELECT COUNT(*) as c FROM users")
            stats["users"] = cursor.fetchone()['c']

            cursor.execute("SELECT COUNT(*) as c FROM users WHERE role='enforcer'")
            stats["enforcers"] = cursor.fetchone()['c']
            
            # Vehicles
            cursor.execute("SELECT COUNT(*) as c FROM vehicles")
            stats["vehicles"] = cursor.fetchone()['c']
            
            # Violations
            cursor.execute("SELECT COUNT(*) as c FROM violations")
            stats["violations"] = cursor.fetchone()['c']
            
            # Pending Violations
            cursor.execute("SELECT COUNT(*) as c FROM violations WHERE status='pending'")
            stats["pending_violations"] = cursor.fetchone()['c']
            
            # Collected Fines (Paid)
            cursor.execute("SELECT SUM(fine_amount) as s FROM violations WHERE status='paid'")
            res = cursor.fetchone()
            stats["fines"] = float(res['s']) if res['s'] else 0.0
            
            return stats
        except Exception as e:
            print(f"Error getting stats: {e}")
            return stats
        finally:
            cursor.close()
            conn.close()

    # ==================== EXTENDED USER MANAGEMENT ====================
    def update_user(self, user_id, full_name, email, phone, department, office) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE users 
                SET full_name=%s, email=%s, phone=%s, department=%s, office_location=%s 
                WHERE user_id=%s
            """, (full_name, email, phone, department, office, user_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def update_user_password(self, user_id, password) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            hashed = self.hash_password(password)
            cursor.execute("UPDATE users SET password=%s WHERE user_id=%s", (hashed, user_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_user(self, user_id) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            # First delete related records or handle constraints if necessary
            # For simplicity, assuming cascade or we just delete user
            cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    # ==================== EXTENDED VEHICLE MANAGEMENT ====================
    def get_all_vehicles(self) -> List[Dict]:
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT v.*, u.full_name as owner_name 
                FROM vehicles v
                JOIN users u ON v.owner_id = u.user_id 
                ORDER BY v.created_at DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def update_vehicle(self, vehicle_id, make, model, year, color, reg_date, exp_date) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            from datetime import date, datetime, timedelta
            today = date.today()
            expiring_threshold = today + timedelta(days=30)
            
            # Helper to ensure date object
            def to_date(d):
                if isinstance(d, str):
                    try:
                        return datetime.strptime(d, '%Y-%m-%d').date()
                    except:
                        return None
                return d

            exp_date_obj = to_date(exp_date)
            # reg_date_obj = to_date(reg_date) # If needed

            # Determine status based on expiry_date
            if exp_date_obj and exp_date_obj < today:
                new_status = 'expired'
            elif exp_date_obj and exp_date_obj <= expiring_threshold:
                new_status = 'expiring'
            else:
                new_status = 'active'
            
            cursor.execute("""
                UPDATE vehicles 
                SET make=%s, model=%s, year=%s, color=%s, registration_date=%s, expiry_date=%s, status=%s
                WHERE vehicle_id=%s
            """, (make, model, year, color, reg_date, exp_date, new_status, vehicle_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating vehicle: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_vehicle(self, vehicle_id) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM vehicles WHERE vehicle_id=%s", (vehicle_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting vehicle: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    # ==================== VEHICLE EXPIRATION MANAGEMENT ====================
    def check_and_update_vehicle_expiration(self):
        """Check all vehicles and update their status based on expiry_date"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            from datetime import date, timedelta
            today = date.today()
            expiring_threshold = today + timedelta(days=30)
            
            # Update expired vehicles
            cursor.execute("""
                UPDATE vehicles 
                SET status = 'expired' 
                WHERE expiry_date < %s AND status != 'expired'
            """, (today,))
            
            # Update expiring vehicles (within 30 days)
            cursor.execute("""
                UPDATE vehicles 
                SET status = 'expiring' 
                WHERE expiry_date >= %s AND expiry_date <= %s AND status = 'active'
            """, (today, expiring_threshold))
            
            # Update active vehicles (not expired and not expiring soon)
            cursor.execute("""
                UPDATE vehicles 
                SET status = 'active' 
                WHERE expiry_date > %s AND status IN ('expired', 'expiring')
            """, (expiring_threshold,))
            
            conn.commit()
            expired_count = cursor.rowcount
            return expired_count
        except Exception as e:
            print(f"Error checking vehicle expiration: {e}")
            return 0
        finally:
            cursor.close()
            conn.close()
    
    def get_expired_vehicles(self) -> List[Dict]:
        """Get all expired vehicles"""
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            from datetime import date
            today = date.today()
            cursor.execute("""
                SELECT v.*, u.full_name as owner_name, u.email, u.phone
                FROM vehicles v
                JOIN users u ON v.owner_id = u.user_id
                WHERE v.expiry_date < %s
                ORDER BY v.expiry_date DESC
            """, (today,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    def get_expiring_vehicles(self, days=30) -> List[Dict]:
        """Get vehicles expiring within specified days"""
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            from datetime import date, timedelta
            today = date.today()
            threshold = today + timedelta(days=days)
            cursor.execute("""
                SELECT v.*, u.full_name as owner_name, u.email, u.phone
                FROM vehicles v
                JOIN users u ON v.owner_id = u.user_id
                WHERE v.expiry_date >= %s AND v.expiry_date <= %s
                ORDER BY v.expiry_date ASC
            """, (today, threshold))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    def update_vehicle_status(self, vehicle_id, status, expiry_date=None) -> bool:
        """Manually update vehicle status (active, expired, expiring) and optionally expiry date"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            if expiry_date:
                cursor.execute("""
                    UPDATE vehicles 
                    SET status = %s, expiry_date = %s 
                    WHERE vehicle_id = %s
                """, (status, expiry_date, vehicle_id))
            else:
                cursor.execute("""
                    UPDATE vehicles 
                    SET status = %s 
                    WHERE vehicle_id = %s
                """, (status, vehicle_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating vehicle status: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def update_violation(self, violation_id, location, notes, status, violation_type_id=None) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            if violation_type_id:
                cursor.execute("""
                    UPDATE violations 
                    SET location=%s, notes=%s, status=%s, violation_type_id=%s
                    WHERE violation_id=%s
                """, (location, notes, status, violation_type_id, violation_id))
            else:
                cursor.execute("""
                    UPDATE violations 
                    SET location=%s, notes=%s, status=%s
                    WHERE violation_id=%s
                """, (location, notes, status, violation_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating violation: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_violation(self, violation_id) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM violations WHERE violation_id=%s", (violation_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting violation: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    # ==================== PAYMENT & SEARCH ====================
    def search_vehicle_full(self, plate_number) -> Dict:
        """Search vehicle and include violations"""
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        result = {"vehicle": None, "violations": []}
        try:
            # Vehicle Info
            cursor.execute("""
                SELECT v.*, u.full_name as owner_name, u.phone as owner_phone, u.user_id as owner_id
                FROM vehicles v 
                JOIN users u ON v.owner_id = u.user_id 
                WHERE v.plate_number = %s
            """, (plate_number,))
            vehicle = cursor.fetchone()
            
            if vehicle:
                result["vehicle"] = vehicle
                # Violations
                cursor.execute("""
                    SELECT v.*, vt.violation_name, vt.fine_amount
                    FROM violations v
                    JOIN violation_types vt ON v.violation_type_id = vt.type_id
                    WHERE v.plate_number = %s
                    ORDER BY v.violation_date DESC
                """, (plate_number,))
                result["violations"] = cursor.fetchall()
                
            return result
        finally:
            cursor.close()
            conn.close()

    def record_payment(self, violation_id, amount=None, method="e-wallet", user_id=None, payment_details=None, transaction_ref=None) -> bool:
        """
        Record a payment in the payments table and update violation status
        """
        conn = self.connect()
        if not conn: return False
        cursor = conn.cursor()
        try:
            # Get violation info to determine amount and user if not provided
            cursor.execute("SELECT fine_amount, plate_number FROM violations WHERE violation_id=%s", (violation_id,))
            violation = cursor.fetchone()
            if not violation:
                return False
            
            fine_amount = amount if amount else violation[0]
            
            # Get user_id from vehicle owner if not provided
            if not user_id:
                cursor.execute("""
                    SELECT owner_id FROM vehicles 
                    WHERE plate_number = (SELECT plate_number FROM violations WHERE violation_id=%s)
                """, (violation_id,))
                owner_result = cursor.fetchone()
                if owner_result:
                    user_id = owner_result[0]
                else:
                    return False
            
            # Insert into payments table
            cursor.execute("""
                INSERT INTO payments (violation_id, user_id, amount, payment_method, payment_details, transaction_reference, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'completed')
            """, (violation_id, user_id, fine_amount, method, payment_details, transaction_ref))
            
            # Update violation status
            cursor.execute("""
                UPDATE violations 
                SET status='paid', payment_date=NOW(), payment_method=%s 
                WHERE violation_id=%s AND status != 'paid'
            """, (method, violation_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
        except Exception as e:
            print(f"Error recording payment: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def get_payment_history(self, user_id=None, violation_id=None) -> List[Dict]:
        """Get payment history for a user or violation"""
        conn = self.connect()
        if not conn: return []
        cursor = conn.cursor(dictionary=True)
        try:
            if violation_id:
                cursor.execute("""
                    SELECT p.*, v.citation_number, v.plate_number, vt.violation_name
                    FROM payments p
                    JOIN violations v ON p.violation_id = v.violation_id
                    JOIN violation_types vt ON v.violation_type_id = vt.type_id
                    WHERE p.violation_id = %s
                    ORDER BY p.created_at DESC
                """, (violation_id,))
            elif user_id:
                cursor.execute("""
                    SELECT p.*, v.citation_number, v.plate_number, vt.violation_name
                    FROM payments p
                    JOIN violations v ON p.violation_id = v.violation_id
                    JOIN violation_types vt ON v.violation_type_id = vt.type_id
                    WHERE p.user_id = %s
                    ORDER BY p.created_at DESC
                """, (user_id,))
            else:
                cursor.execute("""
                    SELECT p.*, v.citation_number, v.plate_number, vt.violation_name, u.full_name as payer_name
                    FROM payments p
                    JOIN violations v ON p.violation_id = v.violation_id
                    JOIN violation_types vt ON v.violation_type_id = vt.type_id
                    JOIN users u ON p.user_id = u.user_id
                    ORDER BY p.created_at DESC
                """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()