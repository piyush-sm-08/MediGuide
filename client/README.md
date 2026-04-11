# Client / Streamlit UI

This folder contains the Streamlit user interface for MediGuide.

## What it does

- Presents a login/signup form for users.
- Allows admins to upload role-specific reference PDF documents.
- Allows patients to upload medical reports and receive summaries.
- Sends chat questions to the backend and displays answers with references.

## How it connects

- The client reads `BASE_URL` from the root `.env` file.
- It sends HTTP requests to the FastAPI server endpoints:
  - `POST /signup`
  - `POST /login`
  - `POST /docs`
  - `POST /docs/report`
  - `GET /docs/reports`
  - `POST /chat`
- Authentication uses HTTP Basic credentials stored in Streamlit session state.

## Run locally

```bash
pip install -r client/requirements.txt
streamlit run client/main.py
```

## Notes

- `BASE_URL` must match the backend server URL.
- The client currently uses the root `.env` file for configuration.
- If the server runs on port `8001`, set `BASE_URL=http://127.0.0.1:8001`.
