#!/usr/bin/env python3

import platform


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
