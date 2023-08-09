
FROM python:3.10
RUN mkdir /app
# set work directory
WORKDIR /app

# install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# copy project
COPY . .
EXPOSE 8000
# CMD ["python", "manage.py", "migrate"]
# ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi"]