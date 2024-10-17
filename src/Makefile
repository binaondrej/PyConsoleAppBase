PYTHON=python3.12
VENV_NAME=.venv

.PHONY: build clean-all

#######################################################################
############################### TARGETS ###############################
#######################################################################

help:
	@echo " 🚩 help   ........................   Show help"
	@echo " 🚩 venv-setup   ..................   Setup venv (clean)"
	@echo " 🚩 venv-clean   ..................   Delete venv"
	@echo " 🚩 clean-build-support   .........   Delete build support files"
	@echo " 🚩 clean-all   ...................   Delete venv and build support files"
	@echo " 🚩 build   .......................   Build package"
	@echo " 🚩 one-time-build   ..............   Setup venv & Build & Clean all"


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
		echo "Installing required packages" ;\
		pip install -r requirements.txt ;\
		echo "Exiting venv" ;\
		deactivate ;\
	}

venv-clean:
	@rm -Rf ./$(VENV_NAME)/

clean-build-support:
	@rm -Rf ./build/ ./*\.egg-info/ ./dist/*.tar.gz

clean-all: venv-clean clean-build-support

build:
	@{ \
  		source $(VENV_NAME)/bin/activate ;\
		python -m build ;\
		deactivate ;\
	}

one-time-build: venv-setup build clean-all
