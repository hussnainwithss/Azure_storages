FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /home/hussnain/Azure_storages
WORKDIR /home/hussnain/Azure_storages
COPY requirements.txt /Azure_storages
RUN pip install -r requirements.txt
COPY . /Azure_storages/
