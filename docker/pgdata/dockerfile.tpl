FROM postgres:latest

ENV PATH="${PATH}:/opt:/vol/tools/shed"

RUN apt update -y && apt install -y \
    postgresql-client

<ADDITIONAL_PACKAGES>

RUN sed -i -e 's/^\(postgres:[^:]\):[0-9]*:[0-9]*:/\1:1000:1000:/' /etc/passwd
