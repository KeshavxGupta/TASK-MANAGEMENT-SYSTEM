# TaskMaster

TaskMaster is a comprehensive task management and e-commerce platform built with Django. It combines task management features with an integrated online shop, providing users with a unified experience for both productivity and shopping needs.

## Features

### Task Management
- User authentication and authorization
- Custom user profiles with extended information
- Task creation and management
- Priority and status tracking
- Task categorization
- Due date management
- Automatic status updates (pending, completed, overdue)
- Task filtering and sorting

### E-commerce Integration
- Product catalog with categories
- Shopping cart functionality
- Order management system
- Multiple payment methods
- Shipping address management
- Order status tracking
- Product stock management

## Technology Stack

- **Backend Framework**: Django 5.1.7
- **Database**: SQLite3
- **Authentication**: Django's built-in authentication system with custom user model
- **Frontend**: Django Templates
- **Additional Features**:
  - Image handling with Pillow
  - Form processing
  - URL routing
  - Template inheritance
  - Static and media file management

## Project Structure

```
taskmasternew/
├── TASKMASTER/              # Main project configuration
├── TASKMASTERAPP/           # Core task management application
├── shop/                    # E-commerce application
├── templates/               # HTML templates
├── media/                   # User-uploaded files
├── manage.py               # Django management script
├── db.sqlite3              # Database file
└── requirements.txt        # Project dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/KeshavxGupta/TASK-MANAGEMENT-SYSTEM
cd taskmasternew
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage

1. Access the application at `http://localhost:8000`
2. Register a new account or log in with existing credentials
3. Create and manage tasks through the task management interface
4. Browse and purchase products through the integrated shop

## Models

### Task Management
- `CustomUser`: Extended user model with profile information
- `Task`: Core task management model
- `Feedback`: User feedback system

### E-commerce
- `Category`: Product categories
- `Product`: Product information and inventory
- `Order`: Order management
- `OrderItem`: Individual items in orders
- `ShippingAddress`: User shipping information

## Security Features

- Custom user authentication
- Password validation
- CSRF protection
- Secure file uploads
- Session management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 