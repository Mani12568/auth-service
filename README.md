# Auth Service

A backend service that handles user signup, login, and authentication using JWT tokens. Built this to understand how real login systems work under the hood — password hashing, tokens, protected routes.

## What it does

- Users can sign up with an email and password
- Passwords are hashed with bcrypt before being stored (never saved as plain text)
- On login, the user gets back two tokens: an access token (short-lived, 15 min) and a refresh token (longer-lived, 7 days)
- A protected `/me` route only works if you send a valid access token — this proves the whole auth flow actually works

## Built with

- Python + FastAPI
- PostgreSQL (Railway)
- SQLModel for the ORM
- python-jose for JWT
- passlib + bcrypt for password hashing

## API

| Method | Route | What it does |
|--------|-------|---------------|
| POST | `/signup` | create a new user account |
| POST | `/login` | verify credentials, returns access + refresh tokens |
| GET | `/me` | returns the logged-in user's info (needs a valid token) |

## Running it locally

```bash
git clone https://github.com/Mani12568/auth-service.git
cd auth-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Add a `.env` file:

Then run:
```bash
uvicorn main:app --reload
```

Go to `http://127.0.0.1:8000/docs` to test it.

## Notes

The tricky part here wasn't the API itself, it was understanding why JWT works the way it does — two tokens instead of one, why passwords get hashed instead of encrypted, why the token has an expiry baked into it instead of the server tracking sessions. Also ran into a weird bcrypt version bug that took some digging to fix — turned out to be a compatibility issue between passlib and a newer bcrypt release.