FROM python:3.9

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src /code/src

EXPOSE 8080

#CMD ["fastapi", "run", "/code/src/main.py", "--port", "8080"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "warning", "--workers", "5"]