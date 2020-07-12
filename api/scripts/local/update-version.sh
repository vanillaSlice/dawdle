#!/usr/bin/env bash

set -e

cd $(dirname "$0")/../..

if [[ -z "$CREATE_RELEASE_SCRIPT" ]]; then
  echo "Must be run by create release script."
  exit 1
fi

VERSION="$1"

sed -i "" -e "s/  version.*/  version: $VERSION/g" ./docs/api.yml
sed -i "" -e "s/__VERSION = .*/__VERSION = \"$VERSION\"/g" ./dawdle/__init__.py
