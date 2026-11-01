# TaskFlow Authenticated Flask Backend
TaskFlow is a productivity API where registered users securely manage their own tasks.
It demonstrates Flask authentication, bcrypt password hashing, SQLAlchemy relationships,
sessions, protected routes, validation, pagination, seed data, and automated tests.
## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m server.seed
python -m server.app
```
The API runs at `http://127.0.0.1:5555`. Run tests with `pytest -q`.
## Endpoints
- `POST /signup`: create a user and start a session.
- `POST /login`: authenticate credentials and start a session.
- `GET /check_session`: return the logged-in user.
- `POST /logout`: clear the current session.
- `GET /tasks?page=1&per_page=5`: paginated tasks owned by the current user.
- `POST /tasks`: create a task for the current user.
- `GET /tasks/<id>`: view an owned task.
- `PATCH /tasks/<id>`: update an owned task.
- `DELETE /tasks/<id>`: delete an owned task.
- `GET /health`: service check.
Passwords are stored as bcrypt hashes. Every task query includes the current
user ID, so users cannot read or modify another user's tasks.
## Intentional Git commits
```bash
git checkout -b feature/project-foundation
git commit -m "chore: establish TaskFlow Flask project foundation" -m "Create the backend structure and reproducible dependency configuration."
git commit -m "chore: configure database sessions and security extensions" -m "Prepare SQLAlchemy, bcrypt, migrations, and session support."
git commit -m "feat: define validated user account model with protected passwords" -m "Add unique users, password hashes, timestamps, and task ownership."
git commit -m "feat: implement login logout and current-user session checks" -m "Provide signup, login, logout, and session-check behavior."
git commit -m "feat: add user-owned task resource and database relationship" -m "Create task fields and connect every task to its owner."
git commit -m "feat: provide authenticated paginated task listing" -m "Return only the current user's tasks with pagination metadata."
git commit -m "feat: complete ownership-aware task update and deletion" -m "Implement protected task CRUD with validation and ownership checks."
git commit -m "feat: add repeatable seed data for users and tasks" -m "Create development users and example tasks safely."
git commit -m "test: verify authentication task CRUD pagination and ownership" -m "Cover security boundaries, validation, and resource behavior."
git commit -m "docs: document TaskFlow setup authentication and API usage" -m "Explain installation, endpoints, testing, and security behavior."
```
Push the final branch with `git push -u origin main`.
