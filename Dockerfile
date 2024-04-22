FROM python:3.10-slim
LABEL Name=local_transforms_all Version=0.0.1

RUN apt-get update && apt-get upgrade --yes
RUN apt-get autoremove && apt-get clean

WORKDIR /home/osint/transforms

# Copy project files and assign them to www-data
COPY . .

# Install requirements, Gunicorn, GEvent
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install --no-cache-dir --upgrade gunicorn gevent


RUN groupadd -r maltego && useradd -r -g maltego maltego
RUN chown -R maltego:maltego /home/osint/transforms

USER maltego

EXPOSE 8080
ENTRYPOINT ["gunicorn"]
# For ssl, add "--bind=0.0.0.0:8443 --certfile=server.crt --keyfile=server.key"
CMD ["--bind=0.0.0.0:8080", "--workers", "3", "-k", "gevent", "project:application"]