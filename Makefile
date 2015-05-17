PYPREFIX_PATH=/usr
PYTHONPATH=$(PYPREFIX_PATH)/bin/python
FIRST_EASYINSTALL=easy_install
PIP=pip
PYTHON=bin/python
EASYINSTALL=bin/easy_install
VIRTUALENV=virtualenv
SOURCE_ACTIVATE=. bin/activate; 


bin/activate: requirements.txt
	@ echo "[ using        ] $(PYTHONPATH)"
	@ echo "[ installing   ] $(VIRTUALENV)"
	@ echo "[ sudo access  ] We need to update the virtualenv"
	sudo $(FIRST_EASYINSTALL) virtualenv
	@ echo "[ creating     ] $(VIRTUALENV) with no site packages"
	@ $(PYTHONLIBS) $(VIRTUALENV) --python=$(PYTHONPATH) --no-site-packages .
	@ echo "[ installing   ] $(PIP) inside $(VIRTUALENV)"
	@ $(SOURCE_ACTIVATE) $(EASYINSTALL) pip 
	@ echo "[ installing   ] $(PIP) requirements"
	@ $(SOURCE_ACTIVATE) $(PIP) install --upgrade pip
	@ $(SOURCE_ACTIVATE) $(PIP) install --upgrade distribute
	@ $(SOURCE_ACTIVATE) $(PIP) install -e  .
	@ $(SOURCE_ACTIVATE) $(PIP) install --default-timeout=100 -r requirements.development.txt
	@ touch bin/activate

deploy: bin/activate
	@ echo "[ deployed     ] the system was completly deployed"

show-version:
	@ $(SOURCE_ACTIVATE) $(PYTHON) --version

shell:
	@ $(SOURCE_ACTIVATE) ipython

pypi-register:
	@ echo "[ record       ] package to pypi servers"
	@ $(SOURCE_ACTIVATE) $(PYTHON) setup.py register -r pypi
	@ echo "[ registered   ] the new version was successfully registered"

pypi-upload:
	@ echo "[ uploading    ] package to pypi servers"
	@ $(SOURCE_ACTIVATE) $(PYTHON) setup.py sdist upload -r https://pypi.python.org/pypi 
	@ echo "[ uploaded     ] the new version was successfully uploaded"

clean:
	@ echo "[ cleaning     ] remove deployment generated files that doesn't exists in the git repository"
	rm -rf bin/ include/ lib/ share/ pip-selfcheck.json .Python dist/ twitter_follow_bot.egg-info/
