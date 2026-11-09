fastapi_auth_project/
├── app/
│   ├── __init__.py
│   ├── database.py       # SQLAlchemy engine & session dependency
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic data validation schemas
│   ├── security.py       # Password hashing & JWT token logic
│   ├── routers/
│   │   ├── auth.py       # Authentication endpoint (Login -> Token)
│   │   └── users.py      # Protected user management endpoints
│   └── main.py           # FastAPI app entry point
├── .env                  # Environment secrets & configuration
├── requirements.txt      # Project dependencies
└── README.md

