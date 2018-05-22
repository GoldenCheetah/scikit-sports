#!/bin/bash
# License: MIT

set -e

run_tests(){
    mkdir -p $TEST_DIR
    cp setup.cfg $TEST_DIR
    cp .coveragerc $TEST_DIR
    cd $TEST_DIR

    python --version
    python -c "import numpy; print('numpy %s' % numpy.__version__)"
    python -c "import scipy; print('scipy %s' % scipy.__version__)"
    python -c "import multiprocessing as mp; print('%d CPUs' % mp.cpu_count())"

    py.test --cov=$MODULE -r sx --pyargs $MODULE --cov-config .coveragerc
}

if [[ "$SKIP_TESTS" != "true" ]]; then
    run_tests
fi

# Is directory still empty ?
ls -ltra $TEST_DIR
ls -ltra $TRAVIS_BUILD_DIR
cp $TEST_DIR/.coverage $TRAVIS_BUILD_DIR
