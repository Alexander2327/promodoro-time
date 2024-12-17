FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry lock --no-update
RUN poetry install


COPY . /app

RUN chmod +x /app/run

# CMD ["poetry", "run", "uvicorn", "main:main_app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
CMD ["poetry", "run", "gunicorn", "main:main_app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8001"]
# CMD ["./run"]