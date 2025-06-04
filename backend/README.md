# Backend Setup

This project relies on several Python packages such as FastAPI and SQLAlchemy.
If you are behind a proxy or do not have internet access, you can install these
packages from pre-downloaded wheels.

1. Download all required wheels on a machine with internet access:
   ```bash
   pip download -r requirements.txt -d vendor
   ```
   Copy the `vendor` directory into this project's `backend` folder.

2. Install the packages offline:
   ```bash
   pip install --no-index --find-links=vendor -r requirements.txt
   ```

Ensure your `OPENAI_API_KEY` is available in the environment or in a `.env`
file before starting the FastAPI server.
