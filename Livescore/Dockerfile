FROM python:3.12

RUN pip install tornado
RUN pip install pymongo

WORKDIR .

COPY . .

EXPOSE 8888

CMD ["python3", "livescore.py"]