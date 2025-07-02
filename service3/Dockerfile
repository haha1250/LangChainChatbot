FROM python:3.10.18

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn langchain-community langchain[openai] openai pgvector postgres psycopg2-binary python-dotenv redis requests

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY ./wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

EXPOSE 80

CMD ["./wait-for-postgres.sh", "postgres", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]