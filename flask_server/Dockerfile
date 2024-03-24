FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY Allie_X_Downtown.mp3 /home
RUN pip install -r requirements.txt
COPY . /code/
CMD python run.py