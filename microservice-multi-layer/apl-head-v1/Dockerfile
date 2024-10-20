FROM python:3.9.0-alpine3.12

WORKDIR /

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY apl.py ./

CMD [ "python3", "./apl.py" ]
