FROM python:3.11-slim
WORKDIR /app/
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    pkg-config \
    clang \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --user pdm
ENV PATH="/root/.local/bin:$PATH"
COPY pyproject.toml pdm.lock ./
RUN pdm install --prod --no-lock --no-editable
COPY . .
EXPOSE 8080

#CMD ["pdm", "run", "python", "manager.py", "runserver"]