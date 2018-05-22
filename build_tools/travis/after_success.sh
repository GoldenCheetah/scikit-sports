#!/bin/bash
# License: MIT

set -e

cd $TRAVIS_BUILD_DIR
codecov || echo "Covdecov upload failed"
