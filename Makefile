all:
	@echo "Nothing to do"

upload: 
	pandoc README.md -o README.rst
	python setup.py sdist upload
