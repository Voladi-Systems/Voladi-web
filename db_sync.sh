#!/bin/bash

set -e

if [ ! $# -eq 2 ]; then
  echo "Usage: ./db_sync.sh <environment> <gzipped file>"
  exit 1
fi

printf "\nThis will irreversibly destroy the database and replace the content with the provided file.\nAre you sure you want to continue? [y/N]: "

read CONFIRM;

if [[ "$CONFIRM" =~ ^(n|N)$ ]];then
  exit 0
elif [[ "$CONFIRM" =~ ^(y|Y)$ ]]; then
  ENV=$1

  DB_CONTAINER=voladi-database-$ENV

  DB_CONTAINER_ID=$(docker ps -aqf "name=$DB_CONTAINER$")

  DUMP_PATH=$2

  DUMP_NAME=$(basename $DUMP_PATH)

  # Start DB container if not running
  if [ ! '$(docker ps -qf "name=$DB_CONTAINER$")' ]; then
    docker start "$DB_CONTAINER"
  fi

  echo "Copying dump \"$DUMP_NAME\" to container"

  docker cp $DUMP_PATH $DB_CONTAINER_ID:/tmp/$DUMP_NAME

  docker exec $DB_CONTAINER bash -c 'dropdb -e -U "$POSTGRES_USER" "$POSTGRES_DB"'

  docker exec $DB_CONTAINER bash -c 'createdb -e -U "$POSTGRES_USER" "$POSTGRES_DB"'

  docker exec -e DUMP_NAME=$DUMP_NAME $DB_CONTAINER bash -c 'gunzip < /tmp/$DUMP_NAME | psql -e -U "$POSTGRES_USER" "$POSTGRES_DB"'

  docker exec $DB_CONTAINER bash -c "rm /tmp/$DUMP_NAME"
fi
