FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "-u", "./multimodalFusionServiceForSingleImage.py"]

EXPOSE 9005
