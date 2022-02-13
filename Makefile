clean:
	rm -rf dist/*
	rm -rf build/*

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