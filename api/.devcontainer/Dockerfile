FROM reachsh/reach:circleci--master as build

FROM python:3.10.5-alpine3.16
RUN apk add gmp libgmpxx git mariadb-connector-c-dev pcre-dev

COPY --from=build /usr/bin/solc /usr/bin/solc
COPY --from=build /usr/bin/goal /usr/bin/goal
COPY --from=build /usr/bin/z3 /usr/bin/z3
COPY --from=build /usr/bin/reachc /usr/bin/reachc
RUN chmod +x /usr/bin/reachc

RUN apk --no-cache add musl-dev linux-headers g++
RUN apk --no-cache add bash

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

EXPOSE 8000

CMD ["uvicorn"," server:app", "--reload"]