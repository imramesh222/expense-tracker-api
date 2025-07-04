# Django Expense & Income Tracker API

## Overview
A RESTful API for tracking personal expenses and income with JWT authentication, tax calculation, and user access control.

## Features
- User registration and JWT login
- CRUD for expense/income records
- Flat and percentage tax calculation
- Paginated responses
- Superuser can access all records

## Setup
```bash
# Clone repo and cd into directory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser  # optional, for admin access
python3 manage.py runserver
```

## API Endpoints
### Auth
- POST `/api/auth/register/` — Register new user
- POST `/api/auth/login/` — Obtain JWT token
- POST `/api/auth/refresh/` — Refresh JWT token

### Expenses/Income
- GET `/api/expenses/` — List (paginated)
- POST `/api/expenses/` — Create
- GET `/api/expenses/{id}/` — Retrieve
- PUT `/api/expenses/{id}/` — Update
- DELETE `/api/expenses/{id}/` — Delete

## Example Request/Response
### Register
```json
POST /api/auth/register/
{
  "username": "testuser",
  "password": "Testpass123",
  "password2": "Testpass123",
  "email": "test@example.com"
}
```

### Login
```json
POST /api/auth/login/
{
  "username": "testuser",
  "password": "Testpass123"
}
Response: { "refresh": "...", "access": "..." }
```

### Create Expense
```json
POST /api/expenses/
{
  "title": "Grocery Shopping",
  "amount": 100.00,
  "transaction_type": "debit",
  "tax": 10.00,
  "tax_type": "flat"
}
```

### Single Record Response
```json
{
  "id": 1,
  "title": "Grocery Shopping",
  "description": "Weekly groceries",
  "amount": 100.00,
  "transaction_type": "debit",
  "tax": 10.00,
  "tax_type": "flat",
  "total": 110.00,
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z"
}
```

### List Response (Paginated)
```json
{
  "count": 25,
  "next": "http://api/expenses/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Grocery Shopping",
      "amount": 100.00,
      "transaction_type": "debit",
      "total": 110.00,
      "created_at": "2025-01-01T10:00:00Z"
    }
  ]
}
```

## Testing Checklist
- User registration/login/token refresh
- CRUD for expenses/income
- Tax calculation (flat/percentage)
- Permissions (user vs superuser)
- JWT required for all endpoints

## License
MIT
