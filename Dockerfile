FROM python:3.8

LABEL MAINTAINER="Rami sfari <rami2sfari@gmail.com>"

# install dependencies & set working directory
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy project
COPY ./src ./src

EXPOSE 5000

COPY ./entrypoint.sh ./entrypoint.sh

# Runtime configuration
ENTRYPOINT ["./entrypoint.sh"]
