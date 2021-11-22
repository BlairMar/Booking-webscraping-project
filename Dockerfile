FROM python:3.8-slim-buster

COPY booking.py requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python","booking.py"]