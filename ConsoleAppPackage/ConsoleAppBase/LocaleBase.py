#!/usr/bin/env python3


class LocaleBase:
	# labels
	LANGUAGE: str = 'LANGUAGE'
	ENGLISH: str = 'ENGLISH'
	OPTION: str = 'OPTION'
	BACK: str = 'BACK'
	QUIT: str = 'QUIT'
	EXIT: str = 'EXIT'
	BOOL_Y: str = 'BOOL_Y'
	BOOL_N: str = 'BOOL_N'
	# errors
	INVALID_OPTION: str = 'INVALID_OPTION'
	FILE_DOES_NOT_EXIST: str = 'FILE_DOES_NOT_EXIST'
	FILE_ALREADY_EXISTS: str = 'FILE_ALREADY_EXISTS'
	FILE_TYPE_NOT_SUPPORTED: str = 'FILE_TYPE_NOT_SUPPORTED'
	INVALID_RANGE: str = 'INVALID_RANGE'
	UNSUPPORTED_OS: str = 'UNSUPPORTED_OS'
	INVALID_LANGUAGE: str = 'INVALID_LANGUAGE'
	LOADER_IMPLEMENTATION_IS_NOT_CONFIGURED: str = 'LOADER_IMPLEMENTATION_IS_NOT_CONFIGURED'
	SAVER_IMPLEMENTATION_IS_NOT_CONFIGURED: str = 'SAVER_IMPLEMENTATION_IS_NOT_CONFIGURED'

	def translate(self, identifier: str, *params) -> str:
		text: str = eval('self.' + identifier)
		for item in params:
			text = text.replace('{%}', str(item), 1)
		return text
