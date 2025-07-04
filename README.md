# Django Expense & Income Tracker API

## Overview
A RESTful API for tracking personal expenses and income with JWT authentication, tax calculation, and user access control. Built with Django, Django REST Framework, and SQLite for development. Suitable for internship/portfolio demonstration.

## Features
- User registration and JWT login
- CRUD for expense/income records
- Flat and percentage tax calculation
- Paginated responses
- Superuser can access all records

## Authentication
All endpoints (except registration and login) require a valid JWT access token in the `Authorization` header:
```
Authorization: Bearer <access_token>
```
Obtain your token via the login endpoint and include it in all protected requests.

## Permissions
- **Regular users:** Can only access and manage their own expense/income records.
- **Superusers:** Can access and manage all users' records.


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
  "username": "ramesh",
  "password": "ramesh@222",
  "password2": "ramesh@222",
  "email": "ramesh@gmail.com",
  "first_name": "Ramesh",
  "last_name": "Rawat"
}
Response: {
    "username": "ramesh",
    "email": "ramesh@gmail.com",
    "first_name": "Ramesh",
    "last_name": "Rawat"
}

```

### Login
```json
POST /api/auth/login/
{
  "username": "ramesh",
  "password": "ramesh@222"
}
Response: {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MTc0MjAwMywiaWF0IjoxNzUxNjU1NjAzLCJqdGkiOiI2OGQ2N2ZmNzI5YzE0NDY4OWU3ZWI3YjU3Y2Q4ZmJiNyIsInVzZXJfaWQiOjR9.cSBFCZj-PdQX17cUIct2K2oz7ksHkNwoorU92zFLneM",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNjU1OTAzLCJpYXQiOjE3NTE2NTU2MDMsImp0aSI6IjNhNjc4MGM0Nzk5YjQ2ZDU4OTgxNTdhMmVmMjRkNTkzIiwidXNlcl9pZCI6NH0.gyTG1avJXlhCId0BTgu2sVZImG6_z7liw4QuTIs75io"
}
```

### Create Expense
```json
POST /api/expenses/
{
  "title": "Zero Tax Test",
  "amount": 100,
  "transaction_type": "debit",
  "tax": 0,
  "tax_type": "flat"
}
```

### Single Record Response
```json
{
    "id": 8,
    "title": "Zero Tax Test",
    "description": null,
    "amount": "100.00",
    "transaction_type": "debit",
    "tax": "0.00",
    "tax_type": "flat",
    "total": 100.0,
    "created_at": "2025-07-04T18:57:41.742228Z",
    "updated_at": "2025-07-04T18:57:41.742252Z"
}
```

### List Response (Paginated)
```json
{
    "count": 6,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 8,
            "title": "Zero Tax Test",
            "description": null,
            "amount": "100.00",
            "transaction_type": "debit",
            "tax": "0.00",
            "tax_type": "flat",
            "total": 100.0,
            "created_at": "2025-07-04T18:57:41.742228Z",
            "updated_at": "2025-07-04T18:57:41.742252Z"
        },
        {
            "id": 7,
            "title": "Percentage Tax Test",
            "description": null,
            "amount": "100.00",
            "transaction_type": "debit",
            "tax": "10.00",
            "tax_type": "percentage",
            "total": 110.0,
            "created_at": "2025-07-04T18:57:23.275353Z",
            "updated_at": "2025-07-04T18:57:23.275379Z"
        },
        {
            "id": 6,
            "title": "Flat Tax Test",
            "description": null,
            "amount": "1000.00",
            "transaction_type": "debit",
            "tax": "100.00",
            "tax_type": "flat",
            "total": 1100.0,
            "created_at": "2025-07-04T18:56:19.641018Z",
            "updated_at": "2025-07-04T18:56:19.641052Z"
        },
        {
            "id": 4,
            "title": "Zero Tax Test",
            "description": null,
            "amount": "100.00",
            "transaction_type": "debit",
            "tax": "0.00",
            "tax_type": "flat",
            "total": 100.0,
            "created_at": "2025-07-04T17:38:16.891910Z",
            "updated_at": "2025-07-04T17:38:16.891942Z"
        },
        {
            "id": 3,
            "title": "Percentage Tax Test",
            "description": null,
            "amount": "100.00",
            "transaction_type": "debit",
            "tax": "10.00",
            "tax_type": "percentage",
            "total": 110.0,
            "created_at": "2025-07-04T17:37:59.465476Z",
            "updated_at": "2025-07-04T17:37:59.465512Z"
        },
        {
            "id": 1,
            "title": "Grocery Shopping",
            "description": "Weekly groceries",
            "amount": "100.00",
            "transaction_type": "debit",
            "tax": "10.00",
            "tax_type": "flat",
            "total": 110.0,
            "created_at": "2025-07-04T12:30:03.218911Z",
            "updated_at": "2025-07-04T12:30:03.218947Z"
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

## Contribution
Contributions are welcome! Please fork the repo and submit a pull request.

## Contact
For questions or feedback, contact [your.email@example.com] or [LinkedIn profile].

## License
MIT 