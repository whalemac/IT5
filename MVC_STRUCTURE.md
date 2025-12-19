# MVC Architecture Structure

This document describes the MVC (Model-View-Controller) architecture of the Nexus Monitor System.

## Folder Structure

```
python_proj/
├── main.py                 # Main application entry point
├── views/                  # View Layer (UI Components)
│   ├── __init__.py
│   ├── ui_login.py         # Login window UI
│   ├── ui_admin.py         # Admin dashboard UI
│   ├── ui_enforcer.py      # Enforcer dashboard UI
│   └── ui_citizen.py       # Citizen dashboard UI
├── controllers/            # Controller Layer (Dialog Controllers)
│   ├── __init__.py
│   ├── admin_dialogs.py    # Admin dialog controllers
│   ├── enforcer_dialogs.py  # Enforcer dialog controllers
│   └── citizen_dialogs.py  # Citizen dialog controllers
├── models/                 # Model Layer (Database)
│   ├── __init__.py
│   └── database.py         # Database manager and models
└── images/                 # Static Assets
    ├── BAGONG-PILIPINAS-LOGO-1-1-150x150.png
    ├── cropped_circle_image.png
    ├── cropped_circle_image(1).png
    └── UM davao.png
```

## Architecture Components

### Views (UI Layer)
- **Location**: `views/`
- **Purpose**: Contains all user interface components
- **Files**:
  - `ui_login.py` - Login window
  - `ui_admin.py` - Admin dashboard interface
  - `ui_enforcer.py` - Enforcer dashboard interface
  - `ui_citizen.py` - Citizen dashboard interface

### Controllers (Business Logic Layer)
- **Location**: `controllers/`
- **Purpose**: Contains dialog controllers that handle user interactions
- **Files**:
  - `admin_dialogs.py` - Admin-related dialogs (Add User, Add Vehicle, etc.)
  - `enforcer_dialogs.py` - Enforcer-related dialogs (Record Violation, Search Vehicle, etc.)
  - `citizen_dialogs.py` - Citizen-related dialogs (Payment, Help, Check Status, etc.)

### Models (Data Layer)
- **Location**: `models/`
- **Purpose**: Contains database models and data access logic
- **Files**:
  - `database.py` - Database manager with all database operations

### Images (Static Assets)
- **Location**: `images/`
- **Purpose**: Contains all image assets used by the UI

## Import Examples

### In main.py:
```python
from views.ui_login import LoginWindow
from views.ui_admin import AdminDashboard
from models.database import DatabaseManager
from controllers.admin_dialogs import AddUserDialog
```

### Image Paths:
All image paths in UI files are relative to the project root:
```python
QPixmap("images/cropped_circle_image(1).png")
```

## Running the Application

Run the application from the project root:
```bash
python main.py
```

The system will automatically:
1. Import all views from the `views/` folder
2. Import all controllers from the `controllers/` folder
3. Import the database model from the `models/` folder
4. Load images from the `images/` folder

## Notes

- All imports have been updated to reflect the new MVC structure
- Image paths have been updated to point to the `images/` folder
- The system maintains full functionality after the refactoring
- No code logic was changed, only file organization

