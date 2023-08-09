
FROM python:3.10-alpine
RUN mkdir /app
# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev

# install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# copy project
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "migrate"]
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi"]