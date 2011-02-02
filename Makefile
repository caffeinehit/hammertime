all:
	@echo "Nothing to do"

upload: 
	pandoc README.md -o README.rst
