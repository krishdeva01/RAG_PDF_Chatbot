# RAGBOT - Setup Guide

## Prerequisites
Ensure you have the following installed:
- Python (>=3.8)
- Node.js (>=16.x)
- PostgreSQL (if using a database other than SQLite)
- pip & virtualenv (for managing Python dependencies)
- yarn or npm (for managing React dependencies)

---

## Backend (Flask)

### Setup and Run
1. Navigate to the backend folder:
   ```sh
   cd RAG_BOT/backend
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up the environment variables:
   - Create a `.env` file in `backend/` and add necessary configurations (e.g., database settings, secret keys).
5. to start the server
   python3 run.py
   ```

---

## Frontend (React)

### Setup and Run
1. Navigate to the frontend folder:
   ```sh
   cd RAG_BOT/frontend
   ```
2. Install dependencies:
   ```sh
   npm install  # or yarn install
   ```
3. Start the development server:
   ```sh
   npm start  # or yarn start
   ```
4. The React app should be available at:
   ```
   http://localhost:3000
   ```

---

## Running the Full Project
- Start the backend (`Flask`):
  ```sh
  cd RAG_BOT/backend
  source venv/bin/activate  # Activate virtualenv
  python3 run.py
  ```
- Start the frontend (`React`):
  ```sh
  cd RAG_BOT/frontend
  npm start  # or yarn start
  ```

---
