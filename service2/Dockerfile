FROM python:3.10.18

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn redis requests openai

EXPOSE 80

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]