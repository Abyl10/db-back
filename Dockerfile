#
FROM python:3.9

#
WORKDIR /assignment2

#
COPY ./requirements.txt /assignment2/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /assignment2/requirements.txt

#
COPY ./app /assignment2/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]