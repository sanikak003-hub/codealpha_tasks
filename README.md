# Mini Social Media Platform

A mini social media application built with HTML, CSS, JavaScript, Django and SQLite.

## Features
- User registration, login and logout
- User profiles with editable name, bio and profile image URL
- Create text posts
- View the latest posts in a feed
- Comment on posts
- Like and unlike posts
- Follow and unfollow other users
- Followers and following counts

## Requirements
- Python 3.10 or newer (Python 3.13 is supported by Django 5.2)
- VS Code or another code editor
- A modern browser such as Google Chrome

## Run on Windows

Open this project folder in VS Code. Open Terminal > New Terminal and run:

```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py makemigrations social
python manage.py migrate
python manage.py runserver
```

Open this address in Chrome:

http://127.0.0.1:8000/

Register a new account to start using the app.

## Optional: Django admin
Create an administrator account:

```powershell
python manage.py createsuperuser
```

Then visit:

http://127.0.0.1:8000/admin/

## Database
The project uses SQLite. Django creates `db.sqlite3` automatically when you run migrations.

## Notes
- Profile images are added using an image URL, so no image-upload package is required.
- This is a local development project. Before public deployment, set a secure secret key, turn off DEBUG, configure ALLOWED_HOSTS, and use HTTPS.
