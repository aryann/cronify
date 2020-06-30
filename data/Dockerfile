FROM python:3.7-slim

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --requirement requirements.txt

CMD exec gunicorn \
    --bind=":$PORT" \
    --workers=1 \
    --threads=4 \
    --log-file=- \
    --access-logfile=- \
    cronify_entry:app
