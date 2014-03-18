help:
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests"
	@echo "coverage - check code coverage quickly with the default Python"

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	find . -iname "*.py" | xargs flake8

test:
	clear; nosetests -s --exe --cover-erase --with-coverage --cover-package=release

coverage:
	clear; nosetests --exe --cover-erase --with-coverage --cover-package=release
	coverage html release.py
	open htmlcov/index.html
