# FROM ubuntu:latest
# LABEL authors="student"
# ENTRYPOINT ["top", "-b"]

FROM python:3.8-slim
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python","./task_2.py"]