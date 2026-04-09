## Development

```
git clone git@github.com:blackelk/set-algebra.git
cd set-algebra

python -m venv ~/venvs/set-algebra
source ~/venvs/set-algebra/bin/activate
pip install -e .[dev]

pylint src/set_algebra
pylint --errors-only tests/*.py
pytest tests
```


## For release testing
```
rm -rf build dist *.egg-info src/*.egg-info

python -m build
python -m venv /tmp/venv-test-set-algebra
source /tmp/venv-test-set-algebra/bin/activate

pip install dist/*.whl
python -c "import set_algebra"
pip install pytest
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
rm -rf build dist *.egg-info src/*.egg-info
python -m build
python -m venv /tmp/venv-try-set-algebra-wheel
source /tmp/venv-try-set-algebra-wheel/bin/activate

pip install twine
pip install dist/set_algebra-*.whl
python -c "import set_algebra"

python -m twine upload \
    --verbose \
    --repository-url https://test.pypi.org/legacy/ \
    -u __token__ \
    dist/*
```
^ Enter the TestPyPI API token when prompted for password.

Review [Set Algebra at testPyPI](https://test.pypi.org/project/set-algebra/)


## Verify package from TestPyPI
```
python -m venv /tmp/venv-testpypi-set-algebra
source /tmp/venv-testpypi-set-algebra/bin/activate

pip install \
    --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple \
    set-algebra

python -c "from set_algebra import Set, Interval"
python -c "import set_algebra; print(set_algebra.__version__)"

pip install pytest
pytest tests
```


## Packaging (live)
Remove `.devN` from `version` in:
- `pyproject.toml`
- `src/set_algebra/__init__.py`
- `HISTORY.md`

```
rm -rf build dist *.egg-info src/*.egg-info
python -m build
python -m venv /tmp/venv-try-set-algebra-wheel
source /tmp/venv-try-set-algebra-wheel/bin/activate

pip install dist/set_algebra-*.whl
python -c "import set_algebra"

python -m twine upload \
    --verbose \
    -u __token__ \
    dist/*
```
Review [Set Algebra at PyPI](https://pypi.org/project/set-algebra/)
