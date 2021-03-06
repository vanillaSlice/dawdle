#!/usr/bin/env bash

set -e

cd $(dirname "$0")/../..

if [[ -z "$CI" ]]; then
  echo "Must be run by CI server."
  exit 1
fi

docker login --username=_ --password="$HEROKU_API_KEY" registry.heroku.com
docker build -t registry.heroku.com/dawdle-api/web -f ./docker/prod.Dockerfile .
docker push registry.heroku.com/dawdle-api/web
image_id=$(docker inspect registry.heroku.com/dawdle-api/web --format={{.Id}})
payload='{"updates":[{"type":"web","docker_image":"'"$image_id"'"}]}'
curl -n -X PATCH https://api.heroku.com/apps/dawdle-api/formation \
    -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
    -H "Authorization: Bearer $HEROKU_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload"
