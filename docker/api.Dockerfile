FROM python:3.12

WORKDIR /app

COPY ./api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api .

EXPOSE 9025

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9025"]
