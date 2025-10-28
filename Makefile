.ONESHELL:
.SHELLFLAGS = -ec
.SILENT:
version := $(shell python -c "from importlib import metadata; print(metadata.version('ipython-cells'))")

.PHONY: dist
dist:
	python -m build

.PHONY: release
release: dist
	twine upload -u __token__ dist/ipython_cells-$(version)*