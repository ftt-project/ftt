run:
	poetry run python -m ftt

clean:
	rm -rf dist build .mypy_cache .pytest_cache
	find . -regex ".*/__pycache__" -exec rm -rf {} +
	find . -regex ".*\.egg-info" -exec rm -rf {} +
	find . -regex ".*/.coverage" -exec rm -rf {} +
	find . -regex ".*/.pytest_cache" -exec rm -rf {} +

test:
	poetry run pytest -s tests

lint:
	poetry run black ftt tests
	poetry run flake8 ftt
	poetry run mypy ftt

build: clean
	poetry build

package: clean
	pyinstaller --onefile \
	--hidden-import="sklearn.utils._typedefs" \
	--hidden-import="numpy" --copy-metadata=numpy \
	--copy-metadata=property_cached \
	--hidden-import=property_cached \
	--collect-all=property_cached \
	--collect-all=ftt \
	--name ftt \
	ftt/__main__.py