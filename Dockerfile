# ─── build stage ──────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# gcc is required to compile asyncpg, bcrypt, cryptography wheels
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY pyproject.toml .

# Parse runtime deps from pyproject.toml and install into /deps prefix
RUN python3 - <<'EOF'
import tomllib, subprocess, sys
with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
deps = data["project"]["dependencies"]
subprocess.check_call([sys.executable, "-m", "pip", "install", "--prefix=/deps"] + deps)
EOF

# ─── runtime stage ────────────────────────────────────────────────────────────
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /deps /usr/local
COPY src ./src

RUN mkdir -p logs \
    && groupadd --system appgroup \
    && useradd --system --gid appgroup --no-create-home appuser \
    && chown -R appuser:appgroup /app

USER appuser

# PORT and WORKERS_NUMBER are supplied at runtime via docker-compose environment.
# Healthcheck is defined in docker-compose.yml so it can reference those vars.
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers ${WORKERS_NUMBER:-4} --no-access-log"]
