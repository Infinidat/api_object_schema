default: test

test: env
	.env/bin/coverage run .env/bin/pytest -x tests && .env/bin/coverage report -m

env: .env/.up-to-date

.env/.up-to-date: setup.py Makefile
	virtualenv --no-site-packages .env
	.env/bin/pip install -e .[testing] -r doc/pip_requirements.txt
	.env/bin/pip install pytest pylint
	.env/bin/pip install coverage
	touch $@

doc: env
	.env/bin/sphinx-build -a -E doc build/sphinx/html

.PHONY: doc
