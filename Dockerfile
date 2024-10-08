FROM python:3.11.7-slim-bookworm

WORKDIR /app

COPY ./ /app
RUN mkdir /app/db

RUN apt update && apt install locales -y

RUN sed -i '/^# *uk_UA.UTF-8/s/^# *//' /etc/locale.gen
RUN sed -i '/^# *en_US.UTF-8/s/^# *//' /etc/locale.gen
RUN locale-gen

RUN pip install -r requirements.txt

WORKDIR /app/backend
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
