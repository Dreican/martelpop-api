# MartelPop API

MartelPop API is a robust backend service built with FastAPI, designed for managing events, user registrations, and authentication. It features a scalable architecture with DTOs, factories, and a clean separation of concerns.

## 🚀 Tech Stack

- **Language:** Python 3.14
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** [PostgreSQL](https://www.postgresql.org/) with [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Migrations:** [Alembic](https://alembic.sqlalchemy.org/)
- **Authentication:** JWT (HS256), OAuth2 (Google, Facebook)
- **Containerization:** [Podman](https://podman.io/) / [Docker](https://www.docker.com/)
- **Validation:** [Pydantic v2](https://docs.pydantic.dev/)

## 📋 Requirements

- Python 3.14+
- Podman (or Docker) and Podman Compose (or Docker Compose)
- Make (optional, for using the Makefile)

## 🛠️ Setup & Run

### 1. Environment Configuration
Copy the `.env.example` (if it exists, otherwise create a `.env` file) and configure the environment variables:

```bash
# Example .env
APP__NAME="MartelPop API"
APP__ENV="DEV"
DB__HOST="db"
DB__NAME="martelpop"
DB__USER="martelpop"
DB__PASSWORD="your_password"
JWT__SECRET_KEY="your_jwt_secret"
```

### 2. Run with Podman/Docker (Recommended)
The project is configured to use `podman-compose` via the `Makefile`.

```bash
# Start the application in development mode
make up

# Run database migrations
make migrate
```
The API will be available at `http://localhost:8000`. 
Interactive API documentation (Swagger UI) is available at `http://localhost:8000/docs`.

### 3. Local Development
If you prefer to run it without containers:

```bash
# Install dependencies
make install

# Start the application
uvicorn app.main:app --reload
```

## 📜 Scripts & Makefile Commands

Commonly used commands defined in the `Makefile`:

| Command | Description |
|---------|-------------|
| `make up` | Start development environment (containers) |
| `make down` | Stop development environment |
| `make logs` | Follow container logs |
| `make migrate` | Run database migrations |
| `make revision m="message"` | Create a new migration revision |
| `make test` | Run tests with pytest |
| `make lint` | Run ruff linting |
| `make format` | Run ruff formatting |
| `make reset-db` | Reset database (removes volumes and restarts) |

## ⚙️ Environment Variables

The application uses nested environment variables prefixed by the module name and separated by `__`.

| Variable | Default | Description |
|----------|-------|-------------|
| **App** | | |
| `APP__NAME` | `MartelPop API` | Application name |
| `APP__VERSION` | `0.1.0` | Application version |
| `APP__ENV` | `DEV` | Environment (DEV, PROD) |
| `APP__HOST` | `localhost` | Application host |
| `APP__PORT` | `8000` | Application port |
| **Database** | | |
| `DB__HOST` | `db` | Database host |
| `DB__PORT` | `5432` | Database port |
| `DB__NAME` | `martelpop` | Database name |
| `DB__USER` | `martelpop` | Database user |
| `DB__PASSWORD` |  | Database password |
| **JWT** | | |
| `JWT__SECRET_KEY` | | **Required** Secret key for JWT |
| `JWT__ALGORITHM` | `HS256` | JWT algorithm |
| **OAuth** | | |
| `OAUTH__GOOGLE_CLIENT_ID` | | Google OAuth Client ID |
| `OAUTH__GOOGLE_CLIENT_SECRET` | | Google OAuth Client Secret |
| `OAUTH__FACEBOOK_CLIENT_ID` | | Facebook OAuth Client ID |
| `OAUTH__FACEBOOK_CLIENT_SECRET` | | Facebook OAuth Client Secret |
| **SMTP** | | |
| `SMTP__HOST` | | SMTP server host |
| `SMTP__PORT` | `587` | SMTP server port |
| `SMTP__USERNAME` | | SMTP username |
| `SMTP__PASSWORD` | | SMTP password |

*Note: For more details, see files in `app/core/config/`.*

## 📂 Project Structure

```text
├── alembic/              # Database migrations
├── app/                  # Application source code
│   ├── api/              # API routes (v1)
│   ├── core/             # Core configurations, database, security
│   ├── features/         # Domain-driven features (auth, events, etc.)
│   ├── middleware/       # Custom FastAPI middlewares
│   ├── shared/           # Shared utilities and helpers
│   └── static/           # Static files
├── docker/               # Docker configuration files
├── scripts/              # Shell scripts (entrypoint)
├── tests/                # Automated tests
├── Makefile              # Automation scripts
├── compose.yml           # Docker/Podman compose configuration
└── requirements.txt      # Python dependencies
```

## ✅ Tests

Run tests using pytest:

```bash
make test
```

## 📄 License

This project is licensed under the terms of the `LICENSE` file found in the root directory.

---
**TODO:**
- [ ] Add deployment guide for production.
- [ ] Document specific API endpoints or link to Swagger.
- [ ] Add instructions for setting up storage providers if applicable.
