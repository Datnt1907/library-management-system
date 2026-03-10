FROM --platform=$BUILDPLATFORM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_CACHE=1
ENV UV_NO_SYNC=1

WORKDIR /app/server

RUN --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  apt-get update \
  && apt-get install -y \
  git \
  build-essential \
  redis \
  libpq-dev \
  curl \
  && uv sync --no-group dev --frozen \
  && apt-get autoremove -y build-essential

ADD . /app/server/

ARG RELEASE_VERSION
ENV RELEASE_VERSION=${RELEASE_VERSION}

CMD ["uv", "run", "uvicorn", "source.app:app", "--host", "0.0.0.0", "--port", "10000"]
