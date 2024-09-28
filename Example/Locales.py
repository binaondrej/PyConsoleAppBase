#!/usr/bin/env python3

from ConsoleAppBase import LocaleBase


class Locale(LocaleBase):
	COUNTER: str
	VALUE_EDIT: str
	INCREASE: str
	DECREASE: str
	INCREASE_BY: str
	SET_VALUE: str
	NEW_VALUE: str
	CLEAR_COUNTER: str


class LocaleEn(Locale):
	##### BASE TRANSLATIONS #####
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
	INVALID_LANGUAGE = 'Invalid language \'{%}\''
	LOADER_IMPLEMENTATION_IS_NOT_CONFIGURED: str = 'Loader implementation is not configured'
	SAVER_IMPLEMENTATION_IS_NOT_CONFIGURED: str = 'Saver implementation is not configured'
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
	##### BASE TRANSLATIONS #####
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
	INVALID_LANGUAGE = 'Neplatný jazyk \'{%}\''
	LOADER_IMPLEMENTATION_IS_NOT_CONFIGURED: str = 'Není nastaveno načítání konfigurace'
	SAVER_IMPLEMENTATION_IS_NOT_CONFIGURED: str = 'Není nastaveno ukládání konfigurace'
	#############################
	COUNTER = 'Počítadlo'
	VALUE_EDIT = 'Změnit hodnotu'
	INCREASE = 'Zvýšit'
	DECREASE = 'Snížit'
	INCREASE_BY = 'Zvýšit o {%}'
	SET_VALUE = 'Nastavit hodnotu'
	NEW_VALUE = 'Nová hodnota'
	CLEAR_COUNTER = 'Vynulovat počítadlo'
