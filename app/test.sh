#!/bin/bash

docker build -t app-test --target test .

docker run --rm \
    --name app_test_cont \
    --volume=`pwd`/src:/usr/src/app \
    app-test
    