#!/bin/bash
set -e

if [ "$1" = 'start' ]; then
  wait-for-it $DB_HOST:$DB_PORT --timeout=0
  confd -onetime -backend env -confdir="$WORKDIR/confd"

  chown -R www-data:www-data $WORKDIR

  if [ ! -z "$CRONJOBS_ENABLED" ]; then
    env >> /etc/environment
    python update_cronjobs.py
  fi

  if [ "$ENVIRONMENT" = "local" ]; then
    python manage.py tailwind install
  fi

  gosu www-data python manage.py migrate

  clear=''
  if [ "$ENVIRONMENT" != "local" ]; then
    clear='--clear -v0'
  fi

  gosu www-data python manage.py collectstatic --noinput $clear
  gosu www-data python manage.py compilemessages

  if [ "$ENVIRONMENT" = "local" ]; then
    if [ ! -z "$CRONJOBS_ENABLED" ]; then
      /bin/bash -c "cron"
    fi
    gosu www-data python manage.py shell < create_default_superuser.py
    exec python manage.py runserver 0.0.0.0:80
  fi

  exec forego start -r
fi

exec "$@"
