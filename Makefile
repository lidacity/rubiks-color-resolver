
init:
	python3 -m venv venv
	@./venv/bin/python3 -m pip install -e .

install:
	python3 setup.py install

clean:
	sudo rm -rf build dist venv
	sudo rm -rf rubiks_color_resolver.egg-info rubiks_color_resolver/*.pyc rubiks_color_resolver/__pycache__

test:
	python3 ./tests/test-unittest.py
	python3 ./tests/test-cubes.py

checks: black-check lint-check   ## Run all checks (black, lint)

black-check:  ## Check code formatter.
	black --check rubiks_color_resolver/ utils/ usr/

black-format:
	black rubiks_color_resolver/ utils/ usr/

lint-check:  ## Check linter.
	flake8 --config .flake8 --statistics rubiks_color_resolver/ utils/ usr/
