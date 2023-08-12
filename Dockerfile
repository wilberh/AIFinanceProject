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
RUN python manage.py migrate --noinput
# RUN python manage.py createsuperuser --noinput --username wilber --email wilberhdez@gmail.com
# ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "CoreRoot.wsgi"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "CoreRoot.wsgi"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]