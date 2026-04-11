# Server Authentication Module

This directory implements user authentication for MediGuide.

## Files

- `routes.py` – HTTP Basic login and signup routes
- `hash_utils.py` – password hashing and verification
- `models.py` – Pydantic request models

## How it works

1. A user signs up with a username, password, and role.
2. The password is hashed before storing in MongoDB.
3. Login verifies credentials using HTTP Basic authentication.
4. Authenticated routes use `Depends(authentication)` to protect access.

## Endpoints

- `POST /signup` – create a new user
- `POST /login` – authenticate an existing user

## Note

- The authentication flow is used by the client to securely access document upload and chat endpoints.
