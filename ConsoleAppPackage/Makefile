#include .env

PYTHON=python3
VENV_NAME=.venv

#######################################################################
############################### TARGETS ###############################
#######################################################################

help:
	@echo " 🚩 help   ........................   Show help"
	@echo " 🚩 setup-venv   ..................   Setup venv (clean)"
	@echo " 🚩 clean-venv   ..................   Delete venv"
	@echo " 🚩 clean-build-support   .........   Delete build support files"
	@echo " 🚩 clean-all   ...................   Delete venv and build support files"
	@echo " 🚩 build   .......................   Build package"
	@echo " 🚩 one-time-build   ..............   Setup venv & Build & Clean all"


setup-venv:
	@echo "Deleting venv '$(VENV_NAME)'"
	@make clean-venv
	@{ \
		echo "Creating new venv '$(VENV_NAME)'" ;\
		$(PYTHON) -m venv $(VENV_NAME) ;\
		echo "Entering venv '$(VENV_NAME)'" ;\
  		source $(VENV_NAME)/bin/activate ;\
		echo "Updating pip" ;\
		pip install --upgrade pip ;\
		echo "Installing required packages" ;\
		pip install -r requirements.txt ;\
		echo "Exiting venv" ;\
		deactivate ;\
	}

clean-venv:
	@rm -Rf ./$(VENV_NAME)/

clean-build-support:
	@rm -Rf ./$(VENV_NAME)/ ./build/ ./*\.egg-info/

clean-all: clean-venv clean-build-support

build:
	@{ \
  		source $(VENV_NAME)/bin/activate ;\
		python setup.py sdist bdist_wheel ;\
		deactivate ;\
	}

one-time-build: setup-venv build clean-all
