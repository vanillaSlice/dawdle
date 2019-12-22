#!/usr/bin/env sh

DIR=$(dirname $0)
docker build -t vanillaslice/dawdle-test -f ${DIR}/../docker/test.Dockerfile ${DIR}/..
docker run vanillaslice/dawdle-test /opt/app/scripts/lint.sh
docker run vanillaslice/dawdle-test /opt/app/scripts/test.sh
