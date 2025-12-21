# TrustMess Backend - AI Coding Agent Instructions

## Project Overview
FastAPI-based REST API + WebSocket server for real-time messaging. PostgreSQL database with SQLAlchemy ORM. JWT authentication with password hashing.

## Architecture

### Core Components
- **FastAPI app** ([main.py](../main.py)) - entry point with CORS, routes registration
- **Database layer** ([src/db/](../src/db/)) - SQLAlchemy models, async PostgreSQL connection
- **Routes** ([src/routes/](../src/routes/)) - auth, users, websocket endpoints, dev utilities
- **WebSocket manager** ([src/websocket/managed.py](../src/websocket/managed.py)) - real-time message handling
- **Security** ([src/secure/](../src/secure/)) - JWT tokens, password hashing, auth middleware

### Database Management
- Models: `User`, `Message`, `Contact`, `Request` ([src/db/models.py](../src/db/models.py))
- Async engine with `asyncpg` driver
- Utilities in `src/db/db_utils/`: `init_db.py`, `seed_data.py`, `clear_data.py`, `drop_db.py`
- Reset scripts in `utils/`: `reset_data_db.py`, `testing_data_db.py`

### Authentication Flow
1. JWT tokens generated in [src/secure/jwt_handler.py](../src/secure/jwt_handler.py)
2. Passwords hashed with bcrypt ([src/secure/passhashing.py](../src/secure/passhashing.py))
3. Middleware validates tokens ([src/secure/auth_middleware.py](../src/secure/auth_middleware.py))
4. User context passed via `request.state.user`

## Key Patterns

### Async Everywhere
```python
# All DB operations are async
async with get_session() as session:
    result = await session.execute(select(User))
```

### Pydantic Schemas
- Request/response validation in [src/schemas/](../src/schemas/)
- Separate from SQLAlchemy models
- Example: `UserSignUp`, `UserLogin`, `UserResponse`

### WebSocket Communication
- Single manager instance handles all connections
- User-to-user messaging via `manager.send_personal_message()`
- Connection stored in dict: `active_connections[user_id]`

## Developer Workflows

### Database Reset
```bash
python utils/reset_data_db.py      # Full reset
python utils/testing_data_db.py    # Add test data
```

### Running Server
```bash
uvicorn main:app --reload           # Development
```

### Environment
- Requires `.env` file (not in repo) with `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`
- Uses `python-dotenv` for config

## Project Conventions

### Code Style
- Ukrainian comments/documentation required (per base_instruction.instructions.md)
- Never modify code without explicit user instruction
- Follow Ukrainian language in all communications

### Route Organization
- `/auth` - signup, login, logout ([src/routes/auth.py](../src/routes/auth.py))
- `/users` - user management ([src/routes/users.py](../src/routes/users.py))
- `/ws` - WebSocket endpoints ([src/routes/websocket.py](../src/routes/websocket.py))
- `/dev` - development utilities ([src/routes/dev_routes.py](../src/routes/dev_routes.py))

### Error Handling
- Use `HTTPException` with appropriate status codes
- WebSocket errors logged, connection closed gracefully

## External Integration
- **Frontend repo**: Separate repository, communicates via REST API + WebSocket
- **CORS**: Configured in [main.py](../main.py) for frontend origin
- **API contracts**: Defined by Pydantic schemas in [src/schemas/](../src/schemas/)

## Dependencies
- FastAPI, Uvicorn, SQLAlchemy, asyncpg
- python-jose (JWT), passlib (bcrypt)
- python-dotenv, pydantic
- See [pyproject.toml](../pyproject.toml) for full list
