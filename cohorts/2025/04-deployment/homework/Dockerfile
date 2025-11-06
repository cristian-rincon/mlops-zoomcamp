FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-dev
COPY model.bin predict.py /app/
ENTRYPOINT [ "uv", "run", "--", "typer", "predict.py", "run" ]