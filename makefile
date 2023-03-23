install:
	python -m pip install -Ue .[dev,docs]

.venv:
	python -m venv .venv
	source .venv/bin/activate && make install
	echo 'run `source .venv/bin/activate` to activate virtualenv'

venv: .venv

test:
	python -m unittest -v
	python -m mypy -p with_context

lint:
	python -m flake8 with_context
	python -m ufmt check with_context

format:
	python -m ufmt format with_context

.PHONY: html
html:
	sphinx-build -ab html docs/ html/

release: lint test clean
	flit publish

clean:
	rm -rf .mypy_cache build dist html *.egg-info

distclean: clean
	rm -rf .venv
