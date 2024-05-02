.ONESHELL:
.SHELLFLAGS = -ec
.SILENT:
version := $(shell python -c "exec(open('ipython_cells/version.py').read());print(__version__)")

.PHONY: dist
dist:
	python setup.py sdist

.PHONY: release
release: dist
	twine upload -u __token__ dist/ipython_cells-$(version)*