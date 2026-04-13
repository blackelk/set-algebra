## Development

```
git clone git@github.com:blackelk/set-algebra.git
cd set-algebra

python -m venv ~/venvs/set-algebra
source ~/venvs/set-algebra/bin/activate
pip install -e .[dev]

pylint src/set_algebra
pylint tests/test_README.py
pylint --errors-only tests/*.py
pytest tests
```


## For release testing
```
deactivate

rm -rf build dist *.egg-info src/*.egg-info
python -m build

rm -rf /tmp/venv-test-set-algebra
python -m venv /tmp/venv-test-set-algebra
source /tmp/venv-test-set-algebra/bin/activate

pip install --force-reinstall dist/*.whl
python -c "import set_algebra"
pip install --upgrade pytest
pytest tests
```


## Packaging (testpypi)
In `pyproject.toml` append `.dev1` to `version`, \
or increase number if there is already `.devN`.

Make sure versions match in:
- `pyproject.toml`
- `src/set_algebra/__init__.py`
- `HISTORY.md`

```
deactivate

rm -rf build dist *.egg-info src/*.egg-info
python -m build

rm -rf /tmp/venv-try-set-algebra-wheel
python -m venv /tmp/venv-try-set-algebra-wheel
source /tmp/venv-try-set-algebra-wheel/bin/activate

pip install --upgrade twine
pip install --force-reinstall dist/set_algebra-*.whl
python -c "import set_algebra"

python -m twine upload \
    --verbose \
    --repository-url https://test.pypi.org/legacy/ \
    -u __token__ \
    dist/*
```
^ Enter the TestPyPI API token when prompted for password.

Review [Set Algebra at testPyPI](https://test.pypi.org/project/set-algebra/ )


## Verify package from TestPyPI

```
deactivate

rm -rf /tmp/venv-testpypi-wheel-set-algebra
python -m venv /tmp/venv-testpypi-wheel-set-algebra
source /tmp/venv-testpypi-wheel-set-algebra/bin/activate

pip install \
    --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple \
    set-algebra

python -c "from set_algebra import Set, Interval"
python -c "import set_algebra; print(set_algebra.__version__)"

pip install --upgrade pytest
pytest tests
```


## Packaging (live)

Remove `.devN` from `version` in:
- `pyproject.toml`
- `src/set_algebra/__init__.py`
- `HISTORY.md`

```
deactivate

rm -rf build dist *.egg-info src/*.egg-info
python -m build

rm -rf /tmp/venv-pypi-wheel-set-algebra
python -m venv /tmp/venv-pypi-wheel-set-algebra
source /tmp/venv-pypi-wheel-set-algebra/bin/activate

pip install --force-reinstall dist/set_algebra-*.whl
python -c "import set_algebra"

python -m twine upload \
    --verbose \
    -u __token__ \
    dist/*
```
^ Enter the PyPI API token when prompted for password.

Review [Set Algebra at PyPI](https://pypi.org/project/set-algebra/ )
