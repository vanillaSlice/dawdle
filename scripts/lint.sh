#!/usr/bin/env sh

DIR=$(dirname $0)
pycodestyle ${DIR}/../*.py ${DIR}/../dawdle/ ${DIR}/../tests/
pylint ${DIR}/../*.py ${DIR}/../dawdle/ ${DIR}/../tests/
