#!/usr/bin/env sh

set -e

cd $(dirname $0)

./lint.sh
./test.sh
