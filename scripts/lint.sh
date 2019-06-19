#!/usr/bin/env bash

DIR=$(dirname $0)
pylint ${DIR}/../*.py ${DIR}/../dawdle/ ${DIR}/../tests/
