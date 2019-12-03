REPOSITORY_URL ?= 

bumpversion:
	python --version
	bumpversion minor
	git push & git push --tags

clean:
	find . -name '*.pyc' -delete

package:
	python setup.py sdist bdist_wheel

do_dist:
	python -m twine upload dist/*

do_dist_specific:
	python -m twine upload --repository-url ${REPOSITORY_URL} dist/*
