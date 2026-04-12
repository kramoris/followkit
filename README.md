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
git clone https://github.com/kramoris/followkit.git
cd followkit
```

### 2. Create and activate a virtual environment

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your local `.env` file

Copy the example environment file:

#### Linux / macOS

```bash
cp .env.example .env
```

#### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Then edit `.env` if needed.

The values in `.env.example` are for local development.  
Use a strong unique `SECRET_KEY` in production.

### 5. Set up the database

```bash
flask --app run.py db upgrade
```

### 6. Run the app

```bash
flask --app run.py run
```

Open `http://127.0.0.1:5000` in your browser.
