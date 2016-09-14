FROM gliderlabs/alpine:latest

COPY requirements.txt run.py /workdir/

RUN apk --no-cache add \
    python3 \
    py-pip \
  && apk --update add --virtual build-dependencies gcc python3-dev build-base \
  && pip install -r /workdir/requirements.txt \
  && apk del build-dependencies \
  && adduser -D app \
  && mkdir -p /workdir  \
  && chown -R app:app /workdir

COPY flask_app /workdir/flask_app/

VOLUME /tmp

RUN chown -R app:app /workdir

WORKDIR /workdir

USER app

EXPOSE 8081

CMD ["python3", "run.py"]
