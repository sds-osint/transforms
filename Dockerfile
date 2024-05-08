FROM python:3.10-slim
LABEL Name=transforms Version=0.0.1

RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r maltego \
    && useradd -r -g maltego maltego

WORKDIR /home/osint/transforms

# Copy project files and assign them to www-data
COPY . .

# Install requirements, Gunicorn, GEvent
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install --no-cache-dir --upgrade gunicorn gevent

RUN pip install --no-cache-dir --upgrade -r requirements.txt gunicorn gevent \
    && chown -R maltego:maltego /home/osint/transforms

USER maltego

EXPOSE 8080
ENTRYPOINT ["gunicorn"]
# For ssl, add "--bind=0.0.0.0:8443 --certfile=server.crt --keyfile=server.key"
CMD ["--bind=0.0.0.0:8080", "--workers", "3", "-k", "gevent", "project:application"]