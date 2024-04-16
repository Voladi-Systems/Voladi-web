#!/bin/bash

set -e

if [ ! $# -eq 1 ]; then
  echo "Usage: ./dump.sh <environment>"
  exit 1
fi

ENV=$1
DATE=$(date +%Y%m%d-%H%M%S)
FILENAME=db_${ENV}_${DATE}.sql
LATEST_FILENAME=db_${ENV}_latest.gz
DB_CONTAINER=voladi-database-$ENV


function create_backup {
  # Start DB container if not running
  if [ -z "$(docker ps -qf name=$DB_CONTAINER$)" ]; then
    echo "Container not running: starting..."
    docker start "$DB_CONTAINER"
  fi

  DB_CONTAINER_ID=$(docker ps -aqf "name=$DB_CONTAINER$")

  echo $DB_CONTAINER_ID

  echo "Creating database dump: $FILENAME"

  docker exec -e FILENAME=$FILENAME $DB_CONTAINER bash -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" -h localhost | gzip -c > /tmp/$FILENAME.gz'

  echo "Copying database dump to host..."

  docker cp $DB_CONTAINER_ID:/tmp/$FILENAME.gz $FILENAME.gz

  echo "Database dump copied to $PWD/$FILENAME.gz"

  docker exec -e FILENAME=$FILENAME $DB_CONTAINER bash -c 'rm /tmp/$FILENAME.gz'
}

create_backup
