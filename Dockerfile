FROM python:3.5

ENV APPLICATION_ROOT=/task/
ADD . $APPLICATION_ROOT
WORKDIR $APPLICATION_ROOT

RUN apt-get update
RUN apt-get install python-dev -y
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 80
CMD ["./run.sh"]