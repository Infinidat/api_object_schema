default: test

test: env
	.env/bin/coverage run .env/bin/py.test -x tests && .env/bin/coverage report -m

env: .env/.up-to-date


.env/.up-to-date: setup.py Makefile
	virtualenv --no-site-packages .env
	.env/bin/pip install -e .
	.env/bin/pip install pytest
	.env/bin/pip install coverage
	touch $@

