# Build stage
FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libfftw3-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.8.2
RUN pip install poetry==${POETRY_VERSION:-1.8.2}

# Set workdir
WORKDIR /app

# Copy pyproject and lockfile first (leverage Docker cache)
COPY pyproject.toml poetry.lock ./

# Install dependencies in isolated poetry venv
RUN poetry config virtualenvs.in-project true && \
    poetry install --only=main

# Add spectrum_api files
COPY . .

# Activate venv as default Python
ENV PATH="/app/.venv/bin:$PATH"
RUN chmod +x docker-entrypoint.sh

# Set entry point
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["main"]
