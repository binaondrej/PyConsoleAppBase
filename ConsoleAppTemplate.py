#!/usr/bin/env python3

import os
import platform
import re
import json
from Locales import *

"""
Version: 2024.05.01
"""

class Machine:
	UNDEFINED = 0
	WINDOWS = 1
	DARWIN = 2

	@staticmethod
	def get_os() -> int:
		if platform.system() == 'Windows':
			return Machine.WINDOWS
		elif platform.system() == 'Darwin':
			return Machine.DARWIN
		else:
			return Machine.UNDEFINED


class MenuItem:
	def __init__(self, title: str, fnc: callable = None, fnc_args: list = [], submenu: dict|None = None, title_only: bool = False, show_condition: str|None = None) -> None:
		self.title = title
		self.fnc = fnc
		self.fnc_args = fnc_args
		self.submenu: dict[int|str, MenuItem] = submenu
		self.title_only: bool = title_only
		self.show_condition: str|None = show_condition

class Menu:
	def __init__(self, menu: dict[int|str, MenuItem], context: object|None = None) -> None:
		"""
		Parameters
		----------
		menu : dict[int | str, MenuItem]
		context : object
		"""

		self.menu: MenuItem = MenuItem('root menu', submenu=menu)
		self.menu_path: list[int|str] = []
		self.context = context

	def __eval(self, source: str) -> any:
		return eval(source, None, {'self': self.context})
	def __eval_string(self, source: str) -> str:
		source_evals = re.findall(r'\{\{.*?\}\}', source)
		for item in source_evals:
			source = source.replace(item, str(self.__eval(item[2:-2])))
		return source

	def show(self) -> None:
		"""
		Prints the menu
		"""
		submenu = self.get_current().submenu
		if submenu:
			for key, option in submenu.items():
				if option.show_condition and not self.__eval(option.show_condition):
					continue
				title = self.__eval_string(option.title)
				if not option.title_only and not option.fnc and not option.submenu:
					title = title + ' [ NOT IMPLEMENTED ]'

				if option.title_only:
					print(title)
				else:
					print('{:.<10}.. {}'.format(str(key) +  ' ', title))

	def step_in(self, option: int) -> None:
		"""
		Opens submenu
		"""
		self.menu_path.append(option)

	def step_out(self) -> None:
		"""
		Steps out from submenu to its parent
		"""
		self.menu_path.pop()

	@staticmethod
	def dict_get_case_insensitive(dictionary: dict, key: int|str) -> any:
		"""
		Gets value in dictionary by key (if str - case insensitive)

		Parameters
		----------
		dictionary : dict
			The dictionary where the key is looked for
		key : int | str
			The looked for key
		"""
		def to_lower(x):
			if type(x) == str:
				return x.lower()
			return x
		key = to_lower(key)
		for item in dictionary:
			if to_lower(item) == key:
				return dictionary[item]

	def get_option(self, option: int|str) -> MenuItem|None:
		menu = self.get_current()
		if menu.submenu:
			return self.dict_get_case_insensitive(menu.submenu, option)
		else:
			return None

	def get_current(self) -> MenuItem|None:
		tmp_menu_item = self.menu
		for item in self.menu_path:
			if tmp_menu_item.submenu:
				tmp_menu_item = self.dict_get_case_insensitive(tmp_menu_item.submenu, item)
			else:
				return None
		return tmp_menu_item

	def get_path(self) -> list[int|str]:
		return self.menu_path

	def get_path_text(self) -> list[str]:
		result = []
		menu = self.menu

		for option in self.menu_path:
			menu = self.dict_get_case_insensitive(menu.submenu, option)
			if menu.title:
				result.append(menu.title)

		return result


class Config:
	def __init__(self, loader: callable = None, saver: callable = None, path: str|None = None, default_data: dict = {}, default_lang: str = 'en') -> None:
		"""
		Parameters
		----------
		loader: callable
			params:
				dict (data read from file)
			returns:
				dict|None (data to keep in memory)
		saver: callable
			params:
				dict (data kept in memory)
			returns:
				dict|None (data to write to file)
		path : str|None
		default_data: dict|None
		default_lang: str
			shortcut for language (en/cs/...)
		Returns
		-------
		bool
			if the loader was successful
		"""
		self.__instantiated = False

		self.__locale: Locale = Locale()
		self.__lang: str = default_lang
		self.lang = default_lang

		self.path: str|None = path
		self.data: dict = default_data
		self.loader: callable = loader
		self.saver: callable = saver

		self.__instantiated = True

	@property
	def lang(self) -> str:
		return self.__lang
	@lang.setter
	def lang(self, lang: str) -> None:
		if len(lang) != 2:
			raise ValueError(self.locale.translate('INVALID_LANGUAGE', lang))
		lang = lang.lower()
		try:
			self.__locale = eval('Locale' + lang[0].upper() + lang[1:] + '()')
			self.__lang = lang
		except:
			raise NotImplementedError(self.locale.translate('TRANSLATION_NOT_IMPLEMENTED', lang))
		if self.__instantiated and self.path and self.saver:
			self.save()
	@property
	def locale(self) -> Locale:
		return self.__locale

	def load(self, path: str = None) -> bool:
		if self.loader is None:
			raise NotImplementedError('Loader implementation is not configured')
		if not path:
			path = self.path
		try:
			with open(path, 'r', encoding='UTF-8') as file:
				conf_content: dict = json.load(file)
		except:
			return False
		if 'lang' in conf_content:
			self.__instantiated = False
			self.lang = conf_content['lang']
			del conf_content['lang']
			self.__instantiated = True
		data = self.loader(conf_content)
		if data is None:
			return False
		self.path = path
		self.data = data
		return True

	def save(self) -> bool:
		if self.saver is None:
			raise NotImplementedError('Saver implementation is not configured')
		data = self.saver(self.data)
		if data is None:
			return False
		data = {**{'lang': self.lang}, **data}
		try:
			with open(self.path, 'w', encoding='UTF-8') as file:
				json.dump(data, file, indent='	')
		except:
			return False
		return True

class Core:
	def __init__(self, title: str, menu: Menu, config: Config, show_menu_path: bool = False) -> None:
		"""
		Parameters
		----------
		title : dict[int | str, MenuItem]
			title of app, that is set as title of terminal window
		menu : object
		show_menu_path : bool = False
			if True, on the top of menu will be shown current path in menu
		"""
		self.config: Config = config
		self.title: str = title
		self.menu: Menu = menu
		self.showMenuPath: bool = show_menu_path
		self.actionsStack: list[tuple[str|int, list]] = []  # list of pairs: option and stdin that will be used instead on user input
		self.set_title()
		self.__stdin: list = []

	def __main__(self) -> None:
		while True:
			self.clear_screen()
			if self.showMenuPath and self.menu.menu_path:
				print('> ' + ' > '.join(self.menu.get_path_text()))

			self.menu.show()
			while True:
				self.__stdin = []
				if self.actionsStack:
					tmp = self.actionsStack.pop(0)
					self.__stdin = [tmp[0]] + tmp[1]
				option = self.input(self.config.locale.OPTION + ': ')
				if option.isdigit():
					option = int(option)
				current_submenu = self.menu.get_option(option)
				if current_submenu and (not current_submenu.show_condition or self.__eval(current_submenu.show_condition)) and not current_submenu.title_only:
					break
				else:
					print(self.config.locale.INVALID_OPTION)
			if current_submenu.fnc:
				print()
				current_submenu.fnc(*current_submenu.fnc_args)
			if current_submenu.submenu:
				self.menu.step_in(option)

	def __eval(self, source: str) -> any:
		return eval(source, None, {'self': self})
	def __eval_string(self, source: str) -> str:
		source_evals = re.findall(r'\{\{.*?\}\}', source)
		for item in source_evals:
			source = source.replace(item, str(self.__eval(item[2:-2])))
		return source

	@staticmethod
	def get_terminal_width() -> int:
		try:
			return os.get_terminal_size().columns
		except:
			return 80

	def clear_screen(self, print_header: bool = True) -> None:
		machine_os = Machine.get_os()
		if machine_os == Machine.WINDOWS:
			os.system('cls')
		elif machine_os == Machine.DARWIN:
			os.system('clear')
		else:
			print('\n\n')
		if print_header:
			print(('{:=^' + str(self.get_terminal_width()) + '}').format(' ' + self.__eval_string(self.title) + ' '))

	def set_title(self, title: str|None = None) -> None:
		title = self.__eval_string(self.title + ' - ' + title) if title else self.__eval_string(self.title)
		machine_os = Machine.get_os()
		if machine_os == Machine.WINDOWS:
			os.system('title ' + str(title))
		elif machine_os == Machine.DARWIN:
			os.system('echo -n -e "\033]0;' + str(title) + '\007"')
		else:
			self.input(self.config.locale.UNSUPPORTED_OS)
			exit(1)

	def menu_back(self) -> None:
		self.menu.step_out()

	def prepare_input(self, value: str):
		self.__stdin.append(value)

	def input(self, prompt: object = '') -> str:
		if self.__stdin:
			stdin = str(self.__stdin.pop(0))
			print(prompt, stdin, sep='', flush=True)
			return stdin
		else:
			return input(prompt)

	def input_int(self, text: str, required: bool = True) -> int|None:
		while True:
			x = self.input(text + ': ')
			if not x and not required:
				return None
			if x.isdigit():
				return int(x)

	def input_int_range(self, text_from: str, text_to: str, required: bool = True) -> tuple[int, int]|None:
		while True:
			tmp = (self.input_int(text_from, required), self.input_int(text_to, required))
			if tmp[0] is None or tmp[1] is None:
				return None
			if tmp[0] < tmp[1]:
				return tmp
			else:
				print(self.config.locale.INVALID_RANGE)

	def input_bool(self, text: str, required: bool = True, options: tuple[str,str]|None = None) -> bool|None:
		if options is None:
			options = (self.config.locale.BOOL_Y, self.config.locale.BOOL_N)
		while True:
			x = self.input(text + ' (' + options[0].upper() + '/' + options[1].lower() + '): ')
			if not x and not required:
				return None
			if x == options[0].upper():
				return True
			elif x.lower() == options[1].lower():
				return False

	def input_file(self, text: str, extensions: list[str]|None = None, required: bool = True, existing: bool|None = None, existing_file_type: str|None = None) -> str|None:
		existing_file_type = existing_file_type.upper() if existing_file_type is not None else None
		if extensions:
			text += ' (' + ', '.join(extensions) + ')'
		text = text + ': '
		while True:
			x = self.input(text)
			if not x:
				if required:
					continue
				else:
					return None

			if (x[0] == '"' and x[-1] == '"') or (x[0] == '\'' and x[-1] == '\''):
				x = x[1:-1]

			if existing is not None:
				if existing:
					if existing_file_type == 'F':
						if not os.path.isfile(x):
							print(self.config.locale.FILE_DOES_NOT_EXIST)
							continue
					elif existing_file_type == 'D':
						if not os.path.isdir(x):
							print(self.config.locale.FILE_DOES_NOT_EXIST)
							continue
					else:
						if not os.path.isfile(x) and not os.path.isdir(x):
							print(self.config.locale.FILE_DOES_NOT_EXIST)
							continue
				else:
					if os.path.isfile(x) or os.path.isdir(x):
						print(self.config.locale.FILE_ALREADY_EXISTS)
						continue

			if extensions:
				name, extension = os.path.splitext(x)
				if not extension in extensions:
					print(self.config.locale.FILE_TYPE_NOT_SUPPORTED)
					continue

			return x

	def input_option(self, text: str, options: list, required: bool = True) -> str|int|None:
		for i in range(len(options)):
			options[i] = str(options[i]).lower()
		while True:
			x = self.input(text + ': ').lower()
			if not x and not required:
				return None
			if x in options:
				return int(x) if x.isdigit() else x

	def simple_menu(self, options: dict|list, prompt: str|None = None, required: bool = True, option_name_getter: str|None = None) -> str|int|None:
		def get_option_name(item) -> str:
			if option_name_getter is not None:
				res = getattr(item, option_name_getter)
				item = res() if callable(res) else res
			return str(item)

		_opts: dict = {}
		if type(options) is dict:
			for key in options:
				_opts[str(key)] = options[key]
		else:
			for i in range(len(options)):
				_opts[str(i + 1)] = options[i]
		options = _opts

		for key in options:
			print('{:.<5}.. {}'.format(str(key) +  ' ', get_option_name(options[key])))
		return self.input_option(self.config.locale.OPTION if prompt is None else prompt, list(options.keys()), required)

	def prompt_change_language(self, languages: dict[str, str], toggle: bool = False) -> None:
		"""
		Prompts language change
		Parameters
		----------
		languages: dict
			dicts of languages in format {'en': 'ENGLISH', ...}, where the value is evaluated from Locales
		toggle: bool
			if true, language change is toggled, else prompt a simple menu with all languages (not required)
		"""
		languages_keys: list[str] = list(languages.keys())
		if toggle:
			self.config.lang = languages_keys[(languages_keys.index(self.config.lang) + 1) % len(languages_keys)]
		else:
			languages_values: list[str] = []
			for item in languages:
				languages_values.append(self.__eval('self.config.locale.' + languages[item]))
			lang_num = self.simple_menu(languages_values, self.config.locale.LANGUAGE, False)
			if not lang_num:
				return
			self.config.lang = languages_keys[lang_num - 1]
		self.set_title()

	def clean_and_exit(self, exit_code: int = 0) -> None:
		self.clear_screen(False)
		exit(exit_code)
