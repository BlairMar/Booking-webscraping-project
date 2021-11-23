FROM python:3.9.7-slim 
#scanned with docker scan, suggested this for less vulnerabilty

COPY booking.py requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python","booking.py"]