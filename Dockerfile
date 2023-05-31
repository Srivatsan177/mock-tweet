FROM python:3.11-slim-buster

WORKDIR /usr/app/backend

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$PATH:/${POETRY_HOME}/bin"

RUN apt update && \
apt install curl -y && \
apt install git -y && \
curl -sSL https://install.python-poetry.org | python3 - && \
poetry config virtualenvs.create false
COPY . .
RUN poetry install --no-root

EXPOSE 8080
# CMD ["uvicorn", "", "--reload", "--port", "8080"]