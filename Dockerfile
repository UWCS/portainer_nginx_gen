FROM python:3.11

RUN pip install pipenv
RUN apt-get update && apt-get install -y nginx inotify-tools

COPY portainer_nginx_gen /app/
COPY Pipfile.lock /app/Pipfile.lock

WORKDIR /app

RUN pipenv sync


RUN chmod +x /app/docker-entrypoint.sh
RUN chmod +x /app/nginx_reloader.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["pipenv", "run", "python", "-u", "main.py"]