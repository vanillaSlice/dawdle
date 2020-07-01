#!/usr/bin/env bash

set -e

cd $(dirname $0)/..

if [ "$#" -ne 1 ]; then
  echo "Need version parameter"
  exit 1
fi

VERSION="$1"

git reset --hard HEAD
git checkout master
git pull

grep -rl --exclude=$(basename "$0") __DAWDLE_VERSION__ . | xargs sed -i '' -e "s/__DAWDLE_VERSION__/$VERSION/g"

BRANCH="release-v$VERSION"
git checkout -b $BRANCH
git add .
git commit -m "Release v$VERSION"
git push --set-upstream origin $BRANCH
