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
	def get_os() -> str:
		if platform.system() == 'Windows':
			return Machine.WINDOWS
		elif platform.system() == 'Darwin':
			return Machine.DARWIN
		else:
			return Machine.UNDEFINED

class MenuItem:
	def __init__(self, title: str, fnc: callable = None, fnc_args: list = [], submenu: dict = None, title_only: bool = False) -> None:
		self.title = title
		self.fnc = fnc
		self.fnc_args = fnc_args
		self.submenu: dict[int|str, MenuItem] = submenu
		self.title_only: bool = title_only

class Menu:
	def __init__(self, menu: dict[int|str, MenuItem], context: object = None) -> None:
		"""
		Parameters
		----------
		menu : dict[int | str, MenuItem]
		context : object
		empty_menu_items : bool = False
			if False, when menu item has empty fnc and submenu, NOT IMPLEMENTED text is printed
		"""

		self.menu: MenuItem = MenuItem(None, submenu=menu)
		self.menu_path: list[int|str] = []
		self.context = context

	def show(self) -> None:
		"""
		Prints the menu
		"""
		submenu = self.get_current().submenu
		if submenu:
			for key, option in submenu.items():
				title: str = option.title
				title_evals = re.findall('\{\{.*?\}\}', title)
				for item in title_evals:
					title = title.replace(item, str(eval(item[2:-2], None, {'self': self.context})))

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
		def to_lower(item):
			if type(item) == str:
				return item.lower()
			return item
		key = to_lower(key)
		for item in dictionary:
			if to_lower(item) == key:
				return dictionary[item]

	def get_option(self, option: int|str) -> MenuItem:
		menu = self.get_current()
		if menu.submenu:
			return self.dict_get_case_insensitive(menu.submenu, option)
		else:
			return None

	def get_current(self) -> MenuItem:
		tmpMenuItem = self.menu
		for item in self.menu_path:
			if tmpMenuItem.submenu:
				tmpMenuItem = self.dict_get_case_insensitive(tmpMenuItem.submenu, item)
			else:
				return None
		return tmpMenuItem

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
	def __init__(self, title: str, menu: Menu, showMenuPath: bool = False) -> None:
		self.title = title
		self.menu = menu
		self.showMenuPath = showMenuPath
		self.set_title()

	def __main__(self) -> None:
		currentSubmenu: MenuItem = None
		while True:
			self.clear_screen()
			if self.showMenuPath and self.menu.menu_path:
				print('> ' + ' > '.join(self.menu.get_path_text()))

			self.menu.show()
			while True:
				option = input('Option: ')
				if option.isdigit():
					option = int(option)
				currentSubmenu = self.menu.get_option(option)
				if currentSubmenu:
					break
				else:
					print('Invalid option')
			if currentSubmenu.fnc:
				print()
				currentSubmenu.fnc(*currentSubmenu.fnc_args)
			if currentSubmenu.submenu:
				self.menu.step_in(option)

	def clear_screen(self) -> None:
		machineOs = Machine.get_os()
		if machineOs == Machine.WINDOWS:
			os.system('cls')
		elif machineOs == Machine.DARWIN:
			os.system('clear')
		else:
			print('\n\n')
		print(('{:=^' + (str)(os.get_terminal_size().columns) + '}').format(' ' + self.title + ' '))

	def set_title(self, title: str = None) -> None:
		title = self.title + ' - ' + title if title else self.title
		machineOs = Machine.get_os()
		if machineOs == Machine.WINDOWS:
			os.system('title ' + title)
		elif machineOs == Machine.DARWIN:
			os.system('echo -n -e "\033]0;' + title + '\007"')
			pass
		else:
			input('UNSUPPORTED OS')
			exit(1)

	def menu_back(self) -> None:
		self.menu.step_out()

	@staticmethod
	def input_int(text: str, required: bool = True) -> int|None:
		while True:
			x = input(text + ': ')
			if not x and not required:
				return None
			if x.isdigit():
				return int(x)

	@staticmethod
	def input_int_range(textFrom: str, textTo: str) -> tuple[int, int]|None:
		while True:
			tmp = (Core.input_int(textFrom), Core.input_int(textTo))
			if tmp[0] <= tmp[1]:
				return tmp
			else:
				print('Invalid range')

	@staticmethod
	def input_bool(text: str, required: bool = True, options: tuple[str] = ('Y', 'n')) -> bool|None:
		while True:
			x = input(text + ' (' + options[0].upper() + '/' + options[1].lower() + '): ')
			if not x and not required:
				return None
			if x == options[0].upper():
				return True
			elif x.lower() == options[1].lower():
				return False

	@staticmethod
	def input_file(text: str, extensions: list = None, required: bool = True, first_variant: str = None):
		if extensions:
			text += ' (' + ', '.join(extensions) + ')'
		text = text + ': '
		while True:
			if first_variant:
				print(text + first_variant)
				x = first_variant
				first_variant = None
			else:
				x = input(text)
				if not x and not required:
					return None

			if (x[0] == '"' and x[-1] == '"') or (x[0] == '\'' and x[-1] == '\''):
				x = x[1:-1]
			if os.path.isfile(x):
				if extensions:
					name, extension = os.path.splitext(x)
					if extension in extensions:
						return x
					else:
						print('File type is not supported.')
				else:
					return x
			else:
				print('File does not exist.')

class Config:
	def __init__(self) -> None:
		##### Properties definition (and default values) #####
		self.counter: int = 0
		######################################################
		self.load()

	def get_config_path(self) -> str:
		return os.path.splitext(os.path.basename(__file__))[0] + '.conf'

	def load(self) -> None:
		if os.path.isfile(self.get_config_path()):
			with open(self.get_config_path(), 'r', encoding='UTF-8') as file:
				confContent = json.load(file)
				###### Properties loading #####
				# connection mode
				if 'counter' in confContent:
					self.counter = confContent['counter']
				###############################

	def save(self) -> None:
		###### Properties saving #####
		confContent = {
			'counter': self.counter,
		}
		##############################
		with open(self.get_config_path(), 'w', encoding='UTF-8') as file:
			json.dump(confContent, file, indent='	')


class MyApp(Core):
	def __init__(self):
		self.config: Config = Config()
		super().__init__(
			'Counter',
			Menu(
				{
					'counterDisplay': MenuItem('Counter: {{self.config.counter}}', title_only=True),
					'S': MenuItem('Value edit', submenu={
						'counterDisplay': MenuItem('Counter: {{self.config.counter}}', title_only=True),
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

	def counter_increase(self, step: int = 1) -> None:
		self.config.counter += step
		self.config.save()

	def counter_decrease(self, step: int = 1) -> None:
		self.config.counter -= step
		self.config.save()

	def counter_set(self, num: int) -> None:
		self.config.counter = num
		self.config.save()

	def counter_set_prompt(self) -> None:
		self.counter_set(self.input_int('New value'))

	def counter_clear(self) -> None:
		self.config.counter = 0
		self.config.save()

	def counter_clear_prompt(self) -> None:
		if self.input_bool('Clear counter'):
			self.counter_clear()



app = MyApp()
app.__main__()