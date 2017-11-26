FROM python:2.7.14-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python setup.py install

CMD [ "python", "./bin/funcy-task-engine.py" ]