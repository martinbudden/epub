# Simple Makefile for some common tasks. This will get
# fleshed out with time to make things easier on developer
# and tester types.
.PHONY: test dist upload

all:
	@echo "No target"

clean:
	rm -r dist || true
	rm -r build || true

test: remotes
	py.test -x test

dist: test
	python setup.py sdist

release: clean test pypi

pypi:
	python setup.py sdist upload

