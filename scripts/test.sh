#!/usr/bin/env sh

pytest --cov-report term-missing --cov=$(dirname $0)/../dawdle/
