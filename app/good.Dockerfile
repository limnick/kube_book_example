FROM alpine:3.6

ENV APP_DIR=/app
RUN mkdir -p ${APP_DIR}
ADD app/requirements.txt ${APP_DIR}/requirements.txt
RUN apk add --no-cache --update python3 python3-dev gcc g++\
            musl-dev ca-certificates linux-headers && \
    python3 -m ensurepip && \
    pip3 install --upgrade pip && \
    pip3 install -U -r ${APP_DIR}/requirements.txt && \
    apk del python3-dev musl-dev gcc g++ linux-headers

ADD app ${APP_DIR}
EXPOSE 8888
CMD python3 ${APP_DIR}/server.py
