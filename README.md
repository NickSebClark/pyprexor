# pyprexor

The **py**thon **pr**ocess **ex**ecut**or**.

![Tests](https://github.com/NickSebClark/pyprexor/actions/workflows/tests.yml/badge.svg?branch=main&event=push)
![Coverage](https://codecov.io/github/NickSebClark/pyprexor/coverage.svg?branch=main)
[![PyPI Latest](https://badgen.net/pypi/v/pyprexor)](https://pypi.org/project/pyprexor/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### What Does Pyprexor Do?

Pyprexor helps create traceability between your process inputs and process outputs.

Parameter sets are stored in a datastore and pyprexor seamlessly passes the required parameters to your annotated processes (a.k.a python functions).

Process outputs are added to the datastore complete with execution metadata and traceability back to your parameter set.
 
See [example.py](/example_app/example.py) for basic usage. 

## Installation

Pyprexor can be installed from PyPI using pip (`$ pip install pyprexor`) or your favourite package manager; we like poetry! (`$ poetry add pyprexor`)

### Running From Source

Dependencies are managed with [poetry](https://python-poetry.org/).

```cmd
pip install poetry
poetry install
```

## Contribution Guide

The project is linted with [ruff](https://github.com/astral-sh/ruff), styled with [black](https://github.com/psf/black) and type checked with [mypy](https://github.com/python/mypy).