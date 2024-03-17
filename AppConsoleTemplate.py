#!/usr/bin/env python3

import os
import platform
import re
import json


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

	def eval(self, source: str) -> any:
		return eval(source, None, {'self': self.context})

	def show(self) -> None:
		"""
		Prints the menu
		"""
		submenu = self.get_current().submenu
		if submenu:
			for key, option in submenu.items():
				if option.show_condition and not self.eval(option.show_condition):
					continue
				title: str = option.title
				title_evals = re.findall(r'\{\{.*?\}\}', title)
				for item in title_evals:
					title = title.replace(item, str(self.eval(item[2:-2])))

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

class Core:
	def __init__(self, title: str, menu: Menu, show_menu_path: bool = False) -> None:
		"""
		Parameters
		----------
		title : dict[int | str, MenuItem]
			title of app, that is set as title of terminal window
		menu : object
		show_menu_path : bool = False
			if True, on the top of menu will be shown current path in menu
		"""
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
				option = self.input('Option: ')
				if option.isdigit():
					option = int(option)
				current_submenu = self.menu.get_option(option)
				if current_submenu and (not current_submenu.show_condition or self.menu.eval(current_submenu.show_condition)) and not current_submenu.title_only:
					break
				else:
					print('Invalid option')
			if current_submenu.fnc:
				print()
				current_submenu.fnc(*current_submenu.fnc_args)
			if current_submenu.submenu:
				self.menu.step_in(option)

	def clear_screen(self) -> None:
		machine_os = Machine.get_os()
		if machine_os == Machine.WINDOWS:
			os.system('cls')
		elif machine_os == Machine.DARWIN:
			os.system('clear')
		else:
			print('\n\n')
		try:
			terminal_size_columns: int = os.get_terminal_size().columns
		except:
			terminal_size_columns: int = 80
		print(('{:=^' + str(terminal_size_columns) + '}').format(' ' + self.title + ' '))

	def set_title(self, title: str|None = None) -> None:
		title = self.title + ' - ' + title if title else self.title
		machine_os = Machine.get_os()
		if machine_os == Machine.WINDOWS:
			os.system('title ' + title)
		elif machine_os == Machine.DARWIN:
			os.system('echo -n -e "\033]0;' + title + '\007"')
			pass
		else:
			self.input('UNSUPPORTED OS')
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

	def input_int_range(self, text_from: str, text_to: str) -> tuple[int, int]|None:
		while True:
			tmp = (self.input_int(text_from), self.input_int(text_to))
			if tmp[0] <= tmp[1]:
				return tmp
			else:
				print('Invalid range')

	def input_bool(self, text: str, required: bool = True, options: tuple[str] = ('Y', 'n')) -> bool|None:
		while True:
			x = self.input(text + ' (' + options[0].upper() + '/' + options[1].lower() + '): ')
			if not x and not required:
				return None
			if x == options[0].upper():
				return True
			elif x.lower() == options[1].lower():
				return False

	def input_file(self, text: str, extensions: list[str]|None = None, required: bool = True, existing: bool|None = None) -> str|None:
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
					if not os.path.isfile(x):
						print('File does not exist.')
						continue
				else:
					if os.path.isfile(x):
						print('File already exists.')
						continue

			if extensions:
				name, extension = os.path.splitext(x)
				if not extension in extensions:
					print('File type is not supported.')
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

class Config:
	def __init__(self, loader: callable, saver: callable = None, path: str|None = None, default_data: dict = {}) -> None:
		"""
		Parameters
		----------
		path : str|None
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
		Returns
		-------
		bool
			if the loader was successful
		"""
		self.path: str|None = path
		self.data: dict = default_data
		self.loader: callable = loader
		self.saver: callable = saver

	def load(self, path: str = None) -> bool:
		if not path:
			path = self.path
		try:
			with open(path, 'r', encoding='UTF-8') as file:
				conf_content: dict = json.load(file)
		except:
			return False
		data = self.loader(conf_content)
		if data is None:
			return False
		self.path = path
		self.data = data
		return True

	def save(self) -> bool:
		data = self.saver(self.data)
		if data is None:
			return False
		try:
			with open(self.path, 'w', encoding='UTF-8') as file:
				json.dump(data, file, indent='	')
		except:
			return False
		return True


class MyApp(Core):
	def __init__(self):
		super().__init__(
			'Counter',
			Menu(
				{
					'counterDisplay': MenuItem('Counter: {{self.config.data[\'counter\']}}', title_only=True),
					'S': MenuItem('Value edit', submenu={
						'counterDisplay': MenuItem('Counter: {{self.config.data[\'counter\']}}', title_only=True),
						'I': MenuItem('Increase', self.counter_increase),
						'D': MenuItem('Decrease', self.counter_decrease),
						'IT': MenuItem('Increase by 10', self.counter_increase, [10]),
						'S': MenuItem('Set value', self.counter_set_prompt),
						'C': MenuItem('Clear counter', self.counter_clear_prompt),
						'b': MenuItem('Back', self.menu_back)
					}),
					'e': MenuItem('End', exit),
				},
				self
			),
			True
		)
		self.config: Config = Config(
			self.__config_loader,
			self.__config_saver,
			os.path.splitext(os.path.basename(__file__))[0] + '.conf',
			self.__config_loader({})
		)
		self.config.load()

	@staticmethod
	def __config_loader(data: dict) -> dict|None:
		conf: dict = {
			'counter': data['counter'] if 'counter' in data else 0
		}
		return conf

	@staticmethod
	def __config_saver(data: dict) -> dict | None:
		conf: dict = {
			'counter': data['counter']
		}
		return conf

	def counter_increase(self, step: int = 1) -> None:
		self.config.data['counter'] += step
		self.config.save()

	def counter_decrease(self, step: int = 1) -> None:
		self.config.data['counter'] -= step
		self.config.save()

	def counter_set(self, num: int) -> None:
		self.config.data['counter'] = num
		self.config.save()

	def counter_set_prompt(self) -> None:
		self.counter_set(self.input_int('New value'))

	def counter_clear(self) -> None:
		self.config.data['counter'] = 0
		self.config.save()

	def counter_clear_prompt(self) -> None:
		if self.input_bool('Clear counter'):
			self.counter_clear()



app = MyApp()
app.__main__()
