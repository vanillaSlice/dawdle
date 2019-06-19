#!/usr/bin/env bash

docker login --username=_ --password="$HEROKU_API_KEY" registry.heroku.com
docker build -t registry.heroku.com/dawdle/web -f $(dirname $0)/../docker/prod.Dockerfile .
docker push registry.heroku.com/dawdle/web
image_id=$(docker inspect registry.heroku.com/dawdle/web --format={{.Id}})
payload='{"updates":[{"type":"web","docker_image":"'"$image_id"'"}]}'
curl -n -X PATCH https://api.heroku.com/apps/dawdle/formation \
     -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
     -H "Authorization: Bearer $HEROKU_API_KEY" \
     -H "Content-Type: application/json" \
     -d "$payload"
