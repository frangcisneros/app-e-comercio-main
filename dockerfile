FROM python:3.12.7

ENV FLASK_CONTEXT=development
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/flaskapp/.local/bin

RUN useradd --create-home --home-dir /home/flaskapp flaskapp \
    && apt-get update \
    && apt-get install -y python3-dev build-essential libpq-dev python3-psycopg2 \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/flaskapp

RUN mkdir app

COPY . .


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN chmod +x ./gunicorn.sh

USER flaskapp

CMD ["bash", "gunicorn.sh"]