FROM python:3.10

WORKDIR /usr/src/app

RUN pip install poetry==1.2.1

COPY poetry.lock pyproject.toml /usr/src/app/
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . /usr/src/app
CMD ["python", "-u", "main.py"]