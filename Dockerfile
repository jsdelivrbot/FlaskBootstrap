FROM ubuntu:16.10

RUN apt-get update && apt-get install -y python3 python3-pip 

RUN pip3 install flask pymysql sqlalchemy flask-sqlalchemy Flask-Migrate flask-login Flask-WTF bcrypt

ADD src /src/
ENV FLASK_APP=main.py
ENV FLASK_DEBUG=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /src/
# CMD ["bash", "init-db.sh"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
