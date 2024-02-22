
FROM python:3.10.9


COPY . /app
WORKDIR /app
RUN apt-get update
#RUN apt-get -y install libsasl2-dev python-dev libldap2-dev libssl-dev
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install firebase-admin
# RUN export NET_TEXTFSM=/app/pullers/ntc-templates/ntc_templates/templates/
RUN apt-get -y install nmap

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
# RUN alembic upgrade head

EXPOSE 8080
#ENTRYPOINT ["python"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
