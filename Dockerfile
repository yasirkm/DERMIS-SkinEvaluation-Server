FROM tensorflow/tensorflow:2.12.0


RUN apt-get update && apt-get install -y git

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt


COPY . /app

ENV MODEL="skin-v1"
ENV BUCKET="dermis-capstone"
ENV ENVIRONMENT="DEPLOYMENT"

EXPOSE 8080

CMD ["python", "app.py"]