FROM alpine:3.6

ADD app /app

RUN apk add --no-cache --update python3 python3-dev \
            musl-dev gcc g++ ca-certificates linux-headers
RUN python3 -m ensurepip
RUN pip3 install --upgrade pip
RUN pip3 install -U -r /app/requirements.txt
RUN apk del python3-dev musl-dev gcc g++ linux-headers

EXPOSE 8888

CMD python3 /app/server.py

