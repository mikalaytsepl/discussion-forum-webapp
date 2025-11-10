FROM python:3.14 

RUN mkdir /forum

WORKDIR /forum

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# freqently comes with outdated pip so this is a must
RUN pip install --upgrade pip

COPY . /forum/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# RUN ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# at run time
