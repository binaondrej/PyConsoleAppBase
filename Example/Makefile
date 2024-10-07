#include .env

PYTHON=python3
VENV_NAME=.venv

PACKAGE=../ConsoleAppPackage/dist/ConsoleAppBase-1.0.1-py3-none-any.whl
PROG_NAME=MyCounterApp

#######################################################################
############################### TARGETS ###############################
#######################################################################

help:
	@echo " 🚩 help   ........................   Show help"
	@echo " 🚩 setup-venv   ..................   Setup venv (clean)"
	@echo " 🚩 clean-venv   ..................   Delete venv"
	@echo " 🚩 run   .........................   Run program"


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
		pip install $(PACKAGE) ;\
		echo "Exiting venv" ;\
		deactivate ;\
	}

clean-venv:
	@rm -Rf ./$(VENV_NAME)/

run:
	@{ \
  		source $(VENV_NAME)/bin/activate ;\
		python "$(PROG_NAME).py" ;\
		deactivate ;\
	}
