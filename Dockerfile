FROM alpine:3.3
MAINTAINER Danilo Bargen <mail@dbrgn.ch>

RUN apk add --no-cache python3 && \
    apk add --no-cache --virtual=build-dependencies wget ca-certificates && \
    wget "https://bootstrap.pypa.io/get-pip.py" -O /dev/stdout | python3 && \
    apk del build-dependencies
ENV PYTHONUNBUFFERED=1

# Create code directory
RUN mkdir /code

# Create unprivileged user
RUN adduser -D logger

# Add files
ADD logger.py run.sh requirements.txt /code/
RUN chown -R logger:logger /code
RUN pip3 install -r /code/requirements.txt

# Change to unprivileged user
USER logger

# Entry point
WORKDIR /code
CMD ["bash", "run.sh"]
