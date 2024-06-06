FROM python:3.11.7-slim-bookworm

WORKDIR /app

COPY ./ ./

RUN apt update && apt install locales -y

RUN sed -i '/^# *uk_UA.UTF-8/s/^# *//' /etc/locale.gen
RUN sed -i '/^# *en_US.UTF-8/s/^# *//' /etc/locale.gen
RUN locale-gen

RUN pip install -r requirements.txt

ENTRYPOINT ["/app/tools/run.sh"]