# DAZ MY CAR!

A local used-car matching application by **DAZzle Bros**.

## Current status

The React frontend and FastAPI backend run locally. The frontend checks the
backend health endpoint automatically and shows its connection status.
Dataset preparation, B-tree indexing and car matching are not implemented yet.
A connected backend does not mean the dataset is loaded.

## Stack

- Frontend: React, TypeScript, Vite and Tailwind CSS
- Backend: Python and FastAPI
- Planned data layer: local files, NumPy storage, custom B-tree and heap

## Requirements

- Node.js 24.x and npm (the setup used Node 24.20.0)
- Python 3.12 (the current environment uses 3.12.16)
- Git

The root backend npm command is written for macOS/Linux. Windows instructions
are included below. A dataset download is not needed to run the starter app.

## First-time installation

Clone this repository using its GitHub URL, then open a terminal at the
repository root, `daz-my-car`.

### Frontend

From the repository root:

```bash
npm --prefix frontend ci
```

This installs the versions in `frontend/package-lock.json`. There are currently
no root npm dependencies, so a root `npm install` is unnecessary.

### Backend: macOS/Linux

From the repository root:

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
cd ..
```

If `python3 --version` already reports Python 3.12, it can replace `python3.12`
when creating the environment. Create your own `.venv`; do not copy another
teammate's environment.

### Backend: Windows PowerShell

From the repository root:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock
cd ..
```

In VS Code, run **Python: Select Interpreter** and select
`backend/.venv/bin/python` on macOS/Linux, or
`backend/.venv/Scripts/python.exe` on Windows. This makes the editor use the
same environment as the backend.

## Run locally

Open **two terminals at the repository root**.

Terminal 1 starts the backend:

```bash
npm run backend
```

Terminal 2 starts the frontend:

```bash
npm run frontend
```

Both scripts enter their application's directory automatically. The backend
script uses `.venv` directly, so manual activation is unnecessary when running it.
Stop each server with **Ctrl+C**. Save file changes for automatic reloading.

On Windows, replace `npm run backend` with this command from the repository root:

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

| Service | Address |
| --- | --- |
| Website | http://127.0.0.1:5173 |
| Backend health | http://127.0.0.1:8000/api/v1/health |
| Interactive API documentation | http://127.0.0.1:8000/docs |

The website should show **Backend connected** when both servers are running.
The health endpoint currently returns:

```json
{"status":"ok","dataset_status":"not_loaded"}
```

The frontend requests `/api/v1/health`; Vite forwards `/api` requests to port
8000. This proxy is for development. Production hosting is not configured.

## Repository structure

```text
daz-my-car/
  package.json              # commands to run each application
  frontend/
    src/App.tsx             # starter page and backend status indicator
    src/index.css           # Tailwind entry point and global styles
    vite.config.ts          # frontend server and API proxy
    package-lock.json       # exact frontend dependency versions
  backend/
    app/
      main.py               # FastAPI application and health route
      api/                  # request/response schemas and routes
      services/             # search coordination
      core/                 # matching rules and ranking
      structures/           # custom B-tree and heap
      data/                 # data access and normalization
    tools/                  # future dataset preparation commands
    tests/                  # backend tests
    benchmarks/             # performance experiments
    requirements.in         # direct runtime dependencies
    requirements-dev.in     # test/lint dependencies
    requirements.lock       # installed runtime and development versions
  data/
    raw/                    # original CSV; local only
    prepared/               # derived data and indexes; local only
    cache/                  # temporary search results; local only
  docs/                     # PID, decisions and project documentation
```

## Dataset and matching plan

Target the complete source dataset of approximately three million listings.
Place the original CSV in `data/raw/`. The source dataset is referenced in the
[US used cars dataset on Kaggle](https://www.kaggle.com/datasets/ananaymital/us-used-cars-dataset).
Verify the actual download, schema and license before preparing it.

- Budget is strict and never relaxed.
- Eight required preferences count equally: year, mileage, body type, fuel,
  transmission, drivetrain, seating and exterior color.
- Show 8/8 matches first, followed by 7/8 and 6/8; exclude lower scores.
- Display ten results per page.
- Refine by make/model after matching.

Dataset preparation instructions will be added when those tools exist.
The assessed pair of comparable algorithms is still an open team decision.

## Development checks

From the repository root:

```bash
npm --prefix frontend run lint
npm --prefix frontend run build
```

For Python, from `backend/` with `.venv` activated:

```bash
python -m ruff check app tools tests benchmarks
python -m pytest tests
```

No backend test suite exists yet; pytest reporting no tests is not a passing
verification of the application. Ruff may flag starter formatting to clean up.

## Dependency changes

Commit package manifests and lockfiles. For frontend dependency changes, run
`npm install <package>` inside `frontend/` and commit its updated lockfile.

For Python, update the relevant `.in` file, install in the project environment,
and regenerate the lockfile from `backend/`:

```bash
python -m pip install -r requirements-dev.in
python -m pip freeze > requirements.lock
```

The lock records the current macOS environment. If a platform-specific package
fails on a teammate's OS, resolve it explicitly and document the change rather
than dropping version tracking.

## Troubleshooting

- **FastAPI import warning:** select the project `.venv` in VS Code.
- **Attribute `app` not found:** save `backend/app/main.py` before running.
- **Backend disconnected:** check the backend terminal and port 8000.
- **Port already in use:** stop the previous server before starting another.
- **Vite configuration changes:** restart the frontend server.

## Team and contributions

- Zachary Zaslau: frontend and integration
- Anthony Toscano: B-tree and dataset preparation
- Daniel De La Torre: priority queue and matching

Use a short branch and a reviewed pull request for each change. Keep the README,
API contract and tests aligned with implementation changes.

Never commit virtual environments, `node_modules`, build output, `.env` files,
or the raw/prepared datasets. The root `.gitignore` excludes these; small
synthetic test fixtures can live under `backend/tests/`.
