#!/usr/bin/env bash

set -e

cd $(dirname "$0")/..

if [[ "$#" -ne 1 ]]; then
  echo "Needs version parameter."
  exit 1
fi

VERSION="$1"
[[ "$VERSION" == v* ]] || VERSION="v$VERSION"

git reset --hard HEAD
git checkout master
git pull

echo "$VERSION" > version.txt
CREATE_RELEASE_SCRIPT=true ./api/scripts/local/update-version.sh "$VERSION"

BRANCH="releases/$VERSION"
git checkout -b "$BRANCH"
git add .
git commit -m "release: $VERSION"
PUSH_OUTPUT=$(git push --set-upstream origin "$BRANCH" 2>&1)
PR_URL=$(echo "$PUSH_OUTPUT" | grep https://github.com | sed "s/  //" | sed "s/remote: //" | xargs)
open "$PR_URL"
