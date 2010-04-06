Example Test Suite
==================

This directory contains the test suite.

The tests may be run with py.test[1]. If you have py.test
installed, from the example base directory simply type

    py.test

and the tests will be found and run. If there are failures
the output can be a bit hard to interpret. You can run
an individual test file, with more verbose output as follows:

    py.test -v --nocapture test/test_example.py

You can run the tests to the first failure:

    py.test -svx

This helps quite a bit with dealing with the error output.

[1] py.test is part of py lib and can be found at
http://codespeak.net/py/dist/test.html