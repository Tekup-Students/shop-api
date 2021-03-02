#!/bin/bash

set -e

run_migrations () {
  if [[ $DJANGO_RUN_MIGRATION = "on" ]]; then
    echo -e "Run migrations : Start \n"
    echo -e "Database migrations : Start \n"

    exec python3 src/manage.py migrate jwt_authentication --database=default&
    wait $!


    DATABASES_FILE="/app/databases/databases.json";
    exec cat $DATABASES_FILE &

    while read -r line;do
      if [[ $line != "default" ]]; then
        echo $line
        echo -e "Start migrations for database -> $line \n"
        exec python3 src/manage.py migrate --database=$(echo $line) &
        wait $!
        echo -e "Run migrations for database -> $line was Done \n"
        echo -e "Start Create Groups for database -> $line \n"
        exec python3 src/manage.py create_groups --database=$(echo $line) &
        wait $!
        echo -e "End Create Groups for database -> $line \n"
      fi
    done < <(cat $DATABASES_FILE | jq -r "keys[]")

    echo -e "Run migrations : Done \n"
  fi
}

echo -e "Start background process to run migrations"
run_migrations &

echo -e "Starting production server\n************\n"
exec supervisord -c /supervisor/supervisor.conf
