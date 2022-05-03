FROM python:3.7

RUN mkdir /Ange
WORKDIR /Ange
COPY . /Ange

RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install