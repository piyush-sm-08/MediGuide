# Server Config Module

This directory contains database connection logic and server configuration.

## Files

- `db.py` – MongoDB connection logic and mock fallback

## How it works

- `db.py` loads MongoDB settings from `server/.env`.
- It attempts to connect to MongoDB using either a local URI or Atlas URI.
- If the connection succeeds, it initializes collections for:
  - `users`
  - `appointments`
  - `doctors`
  - `reports`
- If the connection fails, it creates mock in-memory collections for development.

## Notes

- `MONGODB_URI` may use `mongodb://localhost:27017` or an Atlas connection string.
- The server will still start with a mock database if MongoDB cannot be reached.
