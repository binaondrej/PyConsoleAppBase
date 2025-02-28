#!/usr/bin/env python3

import os
import re
from typing import Callable

from ConsoleAppBase.Config import Config
from ConsoleAppBase.Machine import Machine
from ConsoleAppBase.Menu import Menu


class Core:
	def __init__(self, title: str, menu: Menu, config: Config, show_menu_path: bool = False) -> None:
		"""
		Parameters
		----------
		title : str
			title of app, that is set as title of terminal window
			you can use "{{ ... }}" to evaluate content inside
		menu : Menu
		show_menu_path : bool = False
			if True, on the top of menu will be shown current path in menu
		"""
		self.config: Config = config
		self.title: str = title
		self.menu: Menu = menu
		self.showMenuPath: bool = show_menu_path
		self.set_terminal_window_title()
		self.__stdin: list = []

	def __main__(self) -> None:
		while True:
			self.clear_screen()
			if self.showMenuPath and self.menu.menu_path:
				print('> ' + ' > '.join(self.menu.get_path_text()))

			self.menu.show()
			while True:
				option = self.input(self.config.locale.OPTION + ': ')
				if option.isdigit():
					option = int(option)
				current_submenu = self.menu.get_option(option)
				if current_submenu and (not current_submenu.show_condition or self.__eval(current_submenu.show_condition)) and not current_submenu.label_only:
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

	def set_terminal_window_title(self, title: str|None = None) -> None:
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
		options_str_lower: list[str] = []
		for i in range(len(options)):
			options_str_lower.append(str(options[i]).lower())
		while True:
			x = self.input(text + ': ').lower()
			if not x and not required:
				return None
			if x in options_str_lower:
				return options[options_str_lower.index(x)]

	def simple_menu[K, V](self, options: dict[K, V]|list[V], prompt: str|None = None, required: bool = True, option_label_getter: Callable[[V], str]|None = None) -> str|int|None:
		def get_option_label(value: V) -> str:
			if option_label_getter is not None and callable(option_label_getter):
				return option_label_getter(value)
			return str(value)

		_opts: dict[str, V] = {}
		if type(options) is dict:
			for key in options:
				_opts[str(key)] = options[key]
		else:
			for i in range(len(options)):
				_opts[str(i + 1)] = options[i]
		options: dict[str, V] = _opts

		for key in options:
			print('{:.<5}.. {}'.format(key +  ' ', get_option_label(options[key])))
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
		self.set_terminal_window_title()

	def clean_and_exit(self, exit_code: int = 0) -> None:
		self.clear_screen(False)
		exit(exit_code)
