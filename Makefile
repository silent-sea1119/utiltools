


#virtenvinstall:
#	sudo pip3 install virtualenv virtualenvwrapper

#setup: virtenvinstall
#	source `which virtualenvwrapper.sh` && mkvirtualenv kosandr --python=`which python3` && workon kosandr && pip install setuptools pip wheel && pip install -r misc/freeze.txt; dactivate

build:
	cd misc/setup; python3 setup.py bdist_wheel

install:
	cd misc/setup; sudo pip3 install --upgrade dist/utiltools-`cat version.txt`-py3-none-any.whl

