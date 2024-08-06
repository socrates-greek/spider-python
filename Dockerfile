FROM python:3.12

WORKDIR /home/star

RUN pip install  --progress-bar off --debug flask

RUN pip install --progress-bar off  flask-cors

RUN pip install  --progress-bar off --upgrade spark_ai_python

COPY . .

CMD ["python", "SparkPythondemo.py"]
