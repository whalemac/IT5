# Nexus Monitor System - Setup Instructions

## Prerequisites
- Python 3.9 or higher
- MySQL Server installed and running
- Virtual environment (recommended)

## Installation Steps

### 1. Activate Virtual Environment
```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Or if you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Configure Database
Make sure MySQL is running and update database credentials in `database.py` if needed:
```python
DatabaseManager(host="localhost", user="root", password="", database="nexus_db")
```

### 4. Run the Application
```powershell
python main.py
```

## Default Login Credentials

### Admin
- Username: `admin`
- Password: `admin123`
- Role: Admin

### Enforcer
- Username: `enforcer01`
- Password: `enforcer123`
- Role: Traffic Enforcer

### Citizen
- Username: `juandelacruz`
- Password: `citizen123`
- Role: Citizen

## Troubleshooting

### ModuleNotFoundError: No module named 'PyQt6'
**Solution**: Make sure you're in the virtual environment and run:
```powershell
pip install -r requirements.txt
```

### MySQL Connection Error
**Solution**: 
1. Make sure MySQL server is running
2. Check database credentials in `database.py`
3. The system will auto-create the database if it doesn't exist

### Virtual Environment Issues
**Solution**: 
```powershell
# Create new virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Project Structure
```
python_proj/
├── main.py                 # Main application entry point
├── database.py             # Database manager and operations
├── ui_login.py             # Login window
├── ui_admin.py             # Admin dashboard
├── ui_enforcer.py          # Enforcer dashboard
├── ui_citizen.py           # Citizen dashboard
├── admin_dialogs.py        # Admin dialog windows
├── enforcer_dialogs.py     # Enforcer dialog windows
├── citizen_dialogs.py      # Citizen dialog windows
├── requirements.txt        # Python dependencies
└── USE_CASE_VERIFICATION.md # Use case documentation
```

## Features
- ✅ User authentication and role-based access
- ✅ Admin: Manage users, vehicles, violation types, view all violations
- ✅ Enforcer: Record violations, search vehicles, update details
- ✅ Citizen: Check violations, make payments, view status
- ✅ Payment processing with multiple payment methods
- ✅ Report generation and statistics

