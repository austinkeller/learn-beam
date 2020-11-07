EXPECTED_PYTHON_VERSION = $(shell head -n1 .python-version)
PYTHON_VERSION = $(shell python --version | sed 's/^.* //g')

venv: requirements.txt
	[ "$(PYTHON_VERSION)" == "$(EXPECTED_PYTHON_VERSION)" ]
	python3 -m venv venv
	. venv/bin/activate; pip install -U pip; pip install -Ur requirements.txt

clean:
	rm -rf venv
