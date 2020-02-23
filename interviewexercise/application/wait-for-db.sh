#!/bin/sh
# wait-for-mysql

set -e

cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD mysql --host="mysql" --user="timesheet" --password="timesheet" "timesheet"; do
  >&2 echo "MYSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MYSQL is up - executing command"

exec $cmd