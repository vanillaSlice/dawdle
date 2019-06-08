#!/usr/bin/env bash

pytest --cov-report term-missing --cov=$(dirname $0)/../dawdle/
