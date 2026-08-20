Local database setup

1. Create a `.env` file in the project root (see `.env.example`).

2. Install optional helper for loading `.env` in Python (optional but convenient):

```
pip install python-dotenv
```

3. Set environment variables (temporary session):

```bat
set DB_PASSWORD=your_password
set DB_NAME=transaction_pipeline_db
set DB_HOST=localhost
set DB_PORT=5432
set DB_USER=postgres
```

4. Create the database if it does not exist (use pgAdmin, psql, or the provided script):

```bat
python "scripts/create_db.py"
```

5. Run the connection test:

```bat
python "src/database_connection.py"
```

Security note: Never commit a real `.env` file with secrets. The repository already includes `.gitignore` to ignore `.env` files.