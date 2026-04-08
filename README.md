# FollowKit

FollowKit helps home service businesses track quotes and keep follow-ups organized.

## Features

- User registration and login
- Create, view, and edit quotes
- Track quote status
- Set next follow-up dates
- Add follow-up notes
- Dashboard with due today, overdue, total quotes, open quote value, and status breakdown
- Create and edit follow-up templates

## Tech stack

- Python
- Flask
- SQLAlchemy
- Flask-Login
- Flask-WTF / WTForms
- Jinja templates
- Bootstrap 5
- SQLite

## Local setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd followkit
```

### 2. Create and activate a virtual environment

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a local `.env` file

```env
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///app.db
FLASK_ENV=development
FLASK_DEBUG=1
```

### 5. Set up the database

```bash
flask --app run.py db upgrade
```

### 6. Run the app

```bash
flask --app run.py run
```

Open `http://127.0.0.1:5000` in your browser.
