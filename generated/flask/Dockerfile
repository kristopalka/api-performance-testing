FROM python:3-alpine3.19

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir gunicorn

COPY . /usr/src/app

EXPOSE 8080

# production
ENTRYPOINT ["gunicorn"]
CMD ["-b 0.0.0.0:8080", "openapi_server.wsgi_app:app"]