#!/usr/bin/env python3


class MenuItem:
	def __init__(self, label: str, fnc: callable = None, fnc_args: list = [], submenu: dict|None = None, label_only: bool = False, show_condition: str|None = None) -> None:
		"""
		Parameters
		----------
		label : str
			you can use "{{ ... }}" to evaluate content inside
		fnc : callable
		fnc_args: list
		submenu: dict | None
		label_only: bool
		show_condition: str | None
		"""
		self.label = label
		self.fnc = fnc
		self.fnc_args = fnc_args
		self.submenu: dict[int|str, MenuItem] = submenu
		self.label_only: bool = label_only
		self.show_condition: str|None = show_condition
