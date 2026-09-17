# Auth Service

This is a JWT-based authentication service I built to practice backend development with FastAPI and PostgreSQL. It handles signup, login, and a protected route — the core of how real login systems work.

## Live Link

https://auth-service-production-a98e.up.railway.app/docs
(Note: currently pointing to an old database after a migration — see Notes below)

## What it does

- Users can sign up with an email and password
- Passwords are hashed with bcrypt before being stored (never saved as plain text)
- On login, the user gets back two tokens: an access token (short-lived, 15 min) and a refresh token (longer-lived, 7 days)
- A protected `/me` route only works if you send a valid access token — this proves the whole auth flow actually works
- Login is rate-limited to 5 attempts per minute per IP, to slow down brute-force attempts

## Built with

- Python + FastAPI
- PostgreSQL (Neon)
- SQLModel for the ORM
- python-jose for JWT
- passlib + bcrypt for password hashing
- slowapi for rate limiting

## API

| Method | Route | What it does |
|--------|-------|---------------|
| POST | `/signup` | create a new user account |
| POST | `/login` | verify credentials, returns access + refresh tokens (rate limited: 5/min) |
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
 
DATABASE_URL=your_postgresql_connection_string 

Then run:
```bash
uvicorn main:app --reload
```

Go to `http://127.0.0.1:8000/docs` to test it.

## Notes

The tricky part here wasn't the API itself, it was understanding why JWT works the way it does — two tokens instead of one, why passwords get hashed instead of encrypted, why the token has an expiry baked into it instead of the server tracking sessions. Also ran into a weird bcrypt version bug that took some digging to fix — turned out to be a compatibility issue between passlib and a newer bcrypt release.

Later added rate limiting on the login endpoint using slowapi, capped at 5 attempts per minute per IP, to guard against brute-force login attempts. Tested it directly by triggering the 429 response after repeated rapid login attempts.

Also had to migrate the database from Railway to Neon mid-project after hitting Railway's free trial limit — a good reminder that free-tier infrastructure limits are a real, normal thing to plan around, not just a beginner problem.