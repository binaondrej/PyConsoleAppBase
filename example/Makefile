#include .env

PYTHON=python3
VENV_NAME=.venv

PACKAGE=../ConsoleAppPackage/dist/ConsoleAppBase-1.0.3-py3-none-any.whl
PROG_NAME=MyCounterApp

#######################################################################
############################### TARGETS ###############################
#######################################################################

help:
	@echo " 🚩 help   ........................   Show help"
	@echo " 🚩 venv-setup   ..................   Setup venv (clean)"
	@echo " 🚩 venv-clean   ..................   Delete venv"
	@echo " 🚩 run   .........................   Run program"


venv-setup:
	@echo "Deleting venv '$(VENV_NAME)'"
	@make venv-clean
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

venv-clean:
	@rm -Rf ./$(VENV_NAME)/

run:
	@{ \
  		source $(VENV_NAME)/bin/activate ;\
		python "$(PROG_NAME).py" ;\
		deactivate ;\
	}
