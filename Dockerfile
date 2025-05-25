FROM python:3.9-alpine

COPY requirements.txt /temp/requirements.txt
COPY service /service/

WORKDIR /service
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt



ENV PYTHONPATH "${PYTHONPATH}:/service/products"
CMD ["python", "manage.py", "run_telegram_bot"]