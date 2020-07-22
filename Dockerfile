FROM python:3.8-slim
RUN apt-get update && apt-get install
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT ["gunicorn", "project.resource.check_container_resource:app"]
