# Infra-beta

This repository contains a Python backend built with FastAPI and a Next.js frontend.

## Setup

Run `setup.sh` to install Python and Node.js dependencies:

```bash
./setup.sh
```

## Backend

The backend code resides in the `backend/` directory. Start the server using:

```bash
uvicorn app.main:app --reload
```

## Frontend

Navigate to `frontend/infra-beta` and run the development server:

```bash
npm run dev
```

## Linting

To lint the frontend code, run:

```bash
npm run lint --prefix frontend/infra-beta
```

Make sure dependencies are installed beforehand.
