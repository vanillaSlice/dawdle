#!/usr/bin/env bash

pytest --cov=$(dirname $0)/../dawdle/ --cov-fail-under=90
