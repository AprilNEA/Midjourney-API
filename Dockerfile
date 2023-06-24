FROM python:3.11-alpine as requirement-stage

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN apk add --no-cache \
        curl \
        gcc \
        libressl-dev \
        musl-dev \
        libffi-dev \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile=minimal \
    && source $HOME/.cargo/env\
    && pip install --no-cache-dir poetry \
    && apk del \
           curl \
           gcc \
           libressl-dev \
           musl-dev \
           libffi-dev \
    && poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-alpine
ENV TZ="Asia/Shanghai"

RUN apk add --no-cache gcc python3-dev musl-dev tzdata \
    && ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

RUN mkdir /code

WORKDIR /code

COPY --from=requirement-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/

RUN chmod +x ./run.sh

EXPOSE 8080

CMD ["sh", "run.sh"]
