# Fast Starter API

A starter template for a FastAPI backend with Domain-Driven Design (DDD) architecture.

## Stack

- **Language**: Python 3.12
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Query Builder**: SQLAlchemy 2.0 + asyncpg
- **Auth**: JWT (python-jose) + bcrypt (passlib)
- **Validation**: Pydantic v2
- **Reverse Proxy**: NGINX

## Project Structure

```
src/
	main.py              # App entry point, router registration
	config.py            # Settings from environment variables
	database.py          # SQLAlchemy async engine, Base, get_db
	shared/
		errors/          # AppError, exception handlers
		middleware/      # JWT auth dependency, role guards
	auth/                # Login use case, JWT adapter, password adapter
		domain/
		application/
		infrastructure/
		presentation/
		tests/
	users/               # User CRUD — domain
```

## DDD Layer Convention (per module)

- `domain/` — entities, value objects, port interfaces, domain errors
- `application/` — use cases (one file per use case)
- `infrastructure/` — SQLAlchemy models, mappers, repository implementations
- `presentation/` — FastAPI routers, DTOs (request), RDTOs (response)

## API Endpoints

| Method | Path | Access |
|--------|------|--------|
| POST | /api/v1/auth/login | Public |
| POST | /api/v1/auth/register | Public (creates client) |
| POST | /api/v1/auth/refresh | Authenticated |
| GET | /api/v1/users | Admin |
| GET | /api/v1/users/{id} | Own profile or Admin |
| PUT | /api/v1/users/{id} | Own profile (no role change) or Admin |
| DELETE | /api/v1/users/{id} | Admin only |
| GET | /api/v1/healthz | Public |
| GET | /api/v1/docs | Public (Swagger UI) |
| GET | /api/v1/redoc | Public (ReDoc) |
| GET | /api/v1/openapi.json | Public |

## Environment Variables

- `DATABASE_URL` — PostgreSQL connection string
- `SESSION_SECRET` — Used as JWT signing secret
- `JWT_ALGORITHM` — Default: HS256
- `JWT_EXPIRY_DAYS` — Default: 7
- `DEBUG` — Default: false

## Running

### Development Environment

```bash
make build:dev
make start:dev
```

### Production Environment

```bash
make build:prod
make start:prod
```

## License

This project is licensed under the GPL v3 License.
