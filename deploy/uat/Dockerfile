FROM er5bus/python-supervisor-nginx:python3.8

LABEL MAINTAINER="Infinity Management <rami.safari@infinitymgt.fr>"

# set nginx work dir
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy project
COPY ./src /app/src

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

COPY ./supervisor/supervisor.conf /supervisor/

# Create New user & group
RUN groupadd -r www-nginx && useradd -r -g www-nginx nginx

## add permissions for nginx user
RUN touch /var/run/nginx.pid && \
  chown -R nginx:www-nginx /var/lib/nginx /var/run/nginx.pid /var/log

EXPOSE 8080

COPY ./entrypoint.build.sh ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
