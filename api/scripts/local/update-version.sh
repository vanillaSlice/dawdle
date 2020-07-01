#!/usr/bin/env bash

set -e

cd $(dirname $0)/../..

if [ "$#" -ne 1 ]; then
  echo "Need version parameter"
  exit 1
fi

VERSION="$1"

sed -i '' -e "s/  version.*/  version: $VERSION/g" ./docs/api.yml
sed -i '' -e "s/__VERSION__ = .*/__VERSION__ = \"v$VERSION\"/g" ./dawdle/__init__.py
