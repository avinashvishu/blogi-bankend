# FastAPI Blog Backend Developer Notes

## 1. Getting Started

Make sure you have the following installed:
- Python 3.10+
- pip (Python package manager)
- virtualenv (for creating virtual environments)

### **Setup Instructions**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo/backend
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv myenv
   ```

   - **Windows**:
     ```bash
     myenv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source myenv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**
   - If using **SQLite**, the database will be automatically created.
   - If using **PostgreSQL or MySQL**, update the `DATABASE_URL` in `app/config.py`:
     ```python
     DATABASE_URL = "postgresql://user:password@localhost/dbname"
     ```
   - Apply migrations (if using Alembic):
     ```bash
     alembic upgrade head
     ```

5. **Run the FastAPI Server**
   ```bash
   uvicorn app.main:app --reload
   ```

   The server should now be running at:  
   👉 **http://127.0.0.1:8000**

6. **Access API Documentation**
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 2. Backend Structure

```
backend/
│── app/
│   ├── main.py            # Main FastAPI app
│   ├── models.py          # Database models (SQLAlchemy)
│   ├── schemas.py         # Pydantic schemas
│   ├── database.py        # Database setup
│   ├── config.py          # Configuration settings
│   ├── routes/
│   │   ├── auth.py        # Authentication routes
│   │   ├── blog.py        # Blog routes
│   ├── utils.py           # Utility functions (password hashing, JWT)
│── myenv/                 # Virtual environment
│── requirements.txt        # Dependencies
│── README.md               # Instructions
```

## 3. Authentication

This project uses **JWT authentication**.

1. **Register a user**:  
   ```
   POST /auth/register
   ```

2. **Login to get a token**:  
   ```
   POST /auth/login
   ```

3. **Use the token for protected routes**  
   - Copy the token from the login response.
   - In Swagger UI, click **Authorize** and enter:
     ```
     Bearer YOUR_ACCESS_TOKEN
     ```

## 4. Deployment

To deploy, consider using **Docker**, **Gunicorn**, and **NGINX**.

Example deployment command using Gunicorn:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## 5. Troubleshooting

- **"ModuleNotFoundError" when running FastAPI?**  
  👉 Ensure the virtual environment is activated:  
  ```bash
  myenv\Scripts\activate  # Windows
  source myenv/bin/activate  # Mac/Linux
  ```

- **Database errors?**  
  👉 Check if your database is running and your `DATABASE_URL` is correct.

## 6. Contributing

Feel free to fork this project and submit a pull request! 😊

## 7. License

MIT License - Use this project freely!

