# Setup and Run Guide

## Requirements
- Python 3.10+
- Node.js
- npm
- Git
- Visual Studio Code

## Backend Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv httpx pytest
```

## Environment

Create `.env` from `.env.example`:

```env
API_URL=http://127.0.0.1:8000
DEVICE_ID=PLANT-001
SIMULATOR_INTERVAL=5
OFFLINE_MODE=false
REQUEST_TIMEOUT=5
MAX_RETRIES=3
```

Do not commit `.env`.

## Frontend

```powershell
cd frontend
npm install
```

## Terminal 1 - Backend

From the project root:

```powershell
python -m uvicorn backend.app:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Terminal 2 - Frontend

```powershell
cd frontend
npm run dev
```

Dashboard:

```text
http://localhost:5173
```

## Terminal 3 - Simulator

From the project root:

```powershell
python -m sensor_simulator.simulator
```

## Troubleshooting

If the dashboard is offline, verify that FastAPI is running and that the frontend uses the correct API URL.

If the simulator cannot connect, verify `API_URL`, `DEVICE_ID`, and backend availability.
