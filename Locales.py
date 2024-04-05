#!/usr/bin/env python3

class Locale:
	##### CORE TRANSLATIONS - DONT EDIT #####
	LANGUAGE: str
	CZECH: str
	ENGLISH: str
	OPTION: str
	BACK: str
	QUIT: str
	EXIT: str
	BOOL_Y: str
	BOOL_N: str
	# errors
	INVALID_OPTION: str
	FILE_DOES_NOT_EXIST: str
	FILE_ALREADY_EXISTS: str
	FILE_TYPE_NOT_SUPPORTED: str
	INVALID_RANGE: str
	UNSUPPORTED_OS: str
	TRANSLATION_NOT_IMPLEMENTED: str
	INVALID_LANGUAGE: str
	#############################
	COUNTER: str
	VALUE_EDIT: str
	INCREASE: str
	DECREASE: str
	INCREASE_BY: str
	SET_VALUE: str
	NEW_VALUE: str
	CLEAR_COUNTER: str

	def translate(self, identifier: str, *params) -> str:
		text: str = eval('self.' + identifier)
		for item in params:
			text = text.replace('{%}', str(item), 1)
		return text

class LocaleEn(Locale):
	##### CORE TRANSLATIONS #####
	LANGUAGE = 'Language'
	CZECH = 'Czech'
	ENGLISH = 'English'
	OPTION = 'Option'
	BACK = 'Back'
	QUIT = 'Quit'
	EXIT = 'Exit'
	BOOL_Y = 'Y'
	BOOL_N = 'n'
	# errors
	INVALID_OPTION = 'Invalid option'
	FILE_DOES_NOT_EXIST = 'File does not exist'
	FILE_ALREADY_EXISTS = 'File already exists'
	FILE_TYPE_NOT_SUPPORTED = 'File type is not supported'
	INVALID_RANGE = 'Invalid range'
	UNSUPPORTED_OS = 'UNSUPPORTED OS'
	TRANSLATION_NOT_IMPLEMENTED = 'Translation for language \'{%}\' is not implemented'
	INVALID_LANGUAGE = 'Invalid language \'{%}\''
	#############################
	COUNTER = 'Counter'
	VALUE_EDIT = 'Value edit'
	INCREASE = 'Increase'
	DECREASE = 'Decrease'
	INCREASE_BY = 'Increase by {%}'
	SET_VALUE = 'Set value'
	NEW_VALUE = 'New value'
	CLEAR_COUNTER = 'Clear counter'

class LocaleCs(Locale):
	##### CORE TRANSLATIONS #####
	LANGUAGE = 'Jazyk'
	CZECH = 'Čeština'
	ENGLISH = 'Angličtina'
	OPTION = 'Volba'
	BACK = 'Zpět'
	QUIT = 'Ukončit'
	EXIT = 'Ukončit'
	BOOL_Y = 'A'
	BOOL_N = 'n'
	# errors
	INVALID_OPTION = 'Neplatná volba'
	FILE_DOES_NOT_EXIST = 'Soubor neexistuje'
	FILE_ALREADY_EXISTS = 'Soubor již existuje'
	FILE_TYPE_NOT_SUPPORTED = 'Nepodporovaný typ souboru'
	INVALID_RANGE = 'Neplatné rozmezí'
	UNSUPPORTED_OS = 'NEPODPOROVANÝ OS'
	TRANSLATION_NOT_IMPLEMENTED = 'Překlad pro jazyk \'{%}\' není implementován'
	INVALID_LANGUAGE = 'Neplatný jazyk \'{%}\''
	#############################
	COUNTER = 'Počítadlo'
	VALUE_EDIT = 'Změnit hodnotu'
	INCREASE = 'Zvýšit'
	DECREASE = 'Snížit'
	INCREASE_BY = 'Zvýšit o {%}'
	SET_VALUE = 'Nastavit hodnotu'
	NEW_VALUE = 'Nová hodnota'
	CLEAR_COUNTER = 'Vnulovat počítadlo'
