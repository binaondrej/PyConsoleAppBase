#!/usr/bin/env python3

import re

from ConsoleAppBase.MenuItem import MenuItem


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
				label = self.__eval_string(option.label)
				if not option.label_only and not option.fnc and not option.submenu:
					label = label + ' [ NOT IMPLEMENTED ]'

				if option.label_only:
					print(label)
				else:
					print('{:.<10}.. {}'.format(str(key) +  ' ', label))

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
	def dict_get_case_insensitive[T](dictionary: dict[int|str, T], key: int|str) -> T|None:
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
		return None

	def get_option(self, option: int|str) -> MenuItem|None:
		menu = self.get_current()
		if menu.submenu:
			return self.dict_get_case_insensitive(menu.submenu, option)
		else:
			return None

	def get_current(self) -> MenuItem|None:
		tmp_menu_item: MenuItem = self.menu
		for item in self.menu_path:
			if tmp_menu_item.submenu:
				tmp_menu_item = self.dict_get_case_insensitive(tmp_menu_item.submenu, item)
			else:
				return None
		return tmp_menu_item

	def get_path(self) -> list[int|str]:
		return self.menu_path

	def get_path_text(self) -> list[str]:
		result: list[str] = []
		menu: MenuItem = self.menu

		for option in self.menu_path:
			menu = self.dict_get_case_insensitive(menu.submenu, option)
			if menu.label:
				result.append(self.__eval_string(menu.label))

		return result
