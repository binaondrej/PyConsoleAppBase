#!/usr/bin/env python3

import py_compile
import uuid
from ConsoleAppTemplate import *

"""
Version: 2024.04.04
"""

class Module:
	__py_header: str = '#!/usr/bin/env python3'

	def __init__(self, path: str, load: bool = True) -> None:
		self.path:str = path
		self.imports: dict[str, list[str]] = {}
		self.code: str = ''

		if load and path is not None:
			self.load()

	def load(self):
		with open(self.path, 'r', encoding='UTF-8') as file:
			imports_section: bool = True
			for line in file:
				line_stripped = line.strip()
				if imports_section:
					if not line_stripped or line_stripped.startswith('#'):
						continue
					if line_stripped.startswith('import') or line_stripped.startswith('from'):
						self.add_import(line_stripped)
						continue
					else:
						imports_section = False
				self.code += line
			self.sort_imports()

	def save(self):
		with open(self.path, 'w', encoding='UTF-8') as file:
			# py header
			file.write(self.__py_header + '\n\n')
			# imports
			for pkg in self.imports:
				for item in self.imports[pkg]:
					file.write(item + '\n')
			# code
			file.write(self.code)

	@staticmethod
	def get_package_from_import(line: str) -> str:
		line_parts: list[str] = []
		for item in line.strip().split(' '):
			if item:
				line_parts.append(item)
		return line_parts[1]
	def add_import(self, line: str) -> None:
		package: str = self.get_package_from_import(line)
		if package in self.imports:
			self.imports[package].append(line)
		else:
			self.imports[package] = [line]
	def add_imports(self, imports: list[str]|dict[str, list[str]]) -> None:
		if type(imports) is dict:
			tmp: list[str] = []
			for itemsList in list(imports.values()):
				for item in itemsList:
					tmp.append(item)
			imports: list[str] = tmp
		for item in imports:
			self.add_import(item)
	def pop_import(self, package: str) -> list[str]:
		if package in self.imports:
			return self.imports.pop(package)
		else:
			return []
	def sort_imports(self) -> None:
		self.imports = dict(sorted(self.imports.items()))

class Compiler(Core):
	__log_format: str = '{:.<20}..'
	def __init__(self):
		super().__init__(
			'Compiler',
			Menu(
				{
					'C': MenuItem('Compile to .py', self.compile_py_prompt),
					'B': MenuItem('Compile to .pyc (byte-code)', self.compile_pyc_prompt),
					'q': MenuItem('{{self.config.locale.QUIT}}', exit),
				},
				self
			),
			Config()
		)
		self.core_files: list[str] = ['Compiler.py', 'Locales.py', 'ConsoleAppTemplate.py']
		self.result_suffix = '_StandAlone'


	def compile_py_prompt(self) -> None:
		app_file = self.get_app_file_prompt()
		if not app_file:
			return

		app_dst_py = os.path.splitext(app_file)[0] + self.result_suffix + '.py'
		if os.path.exists(app_dst_py) and not self.input_bool('\nFile \'' + app_dst_py + '`\' already exists. Would you like to overwrite it?'):
			return

		print()
		self.compile_py(app_file, app_dst_py)
		self.input(5*'=' + ' ALL DONE ' + 5*'=')

	def compile_pyc_prompt(self) -> None:
		app_file = self.get_app_file_prompt()
		if not app_file:
			return

		app_tmp_py = app_file
		while os.path.exists(app_tmp_py):
			app_tmp_py = 'tmp_' + uuid.uuid4().hex + '.py'

		app_dst_pyc = os.path.splitext(app_file)[0] + self.result_suffix + '.pyc'
		if os.path.exists(app_dst_pyc) and not self.input_bool('\nFile \'' + app_dst_pyc + '`\' already exists. Would you like to overwrite it?'):
			return

		print()
		self.compile_py(app_file, app_tmp_py)
		self.compile_pyc(app_tmp_py, app_dst_pyc)
		os.remove(app_tmp_py)
		self.input(5*'=' + ' ALL DONE ' + 5*'=')


	def compile_py(self, app_src: str, app_dst: str) -> None:
		def make_code_block(name: str, code: str) -> str:
			separator_format: str = '#{:=^78}#\n'
			code_block = separator_format.format(' BEGIN: ' + name.upper() + ' ')
			code_block += code
			code_block += separator_format.format(' END: ' + name.upper() + ' ')
			return code_block

		print(self.__log_format.format('Loading '), end='', flush=True)
		# module - locale
		module_locales: Module = Module(self.core_files[1])
		# module - core
		module_core: Module = Module(self.core_files[2])
		module_core.pop_import(os.path.splitext(self.core_files[1])[0])
		# module - app
		module_app: Module = Module(app_src)
		module_app.pop_import(os.path.splitext(self.core_files[2])[0])
		print(' [ DONE ]')

		print(self.__log_format.format('Merging '), end='', flush=True)
		# final module
		final_module: Module = Module(app_dst, False)

		final_module.add_imports(module_locales.imports)
		final_module.add_imports(module_core.imports)
		final_module.add_imports(module_app.imports)
		final_module.sort_imports()

		final_module.code += '\n' + make_code_block('Locales', module_locales.code)
		final_module.code += '\n' + make_code_block('Core', module_core.code)
		final_module.code += '\n' + make_code_block('App', module_app.code)
		print(' [ DONE ]')

		print(self.__log_format.format('Saving '), end='', flush=True)
		final_module.save()
		print(' [ DONE ]')

	def compile_pyc(self, app_src: str, app_dst: str) -> None:
		print(self.__log_format.format('Compiling '), end='', flush=True)
		py_compile.compile(app_src, app_dst)
		print(' [ DONE ]')

	def get_app_file_prompt(self) -> str|None:
		files: list[str] = list(filter(
			lambda x: x.endswith('.py') and os.path.isfile(x) and x not in self.core_files and not x.endswith(self.result_suffix + '.py'),
			os.listdir()
		))
		files.sort()
		files: dict[int, str] = {i + 1: files[i] for i in range(len(files))}
		option = self.simple_menu({**files, 'x': 'Custom file', 'c': 'Cancel'})
		if option == 'c':
			return
		elif option == 'x':
			path = self.input_file('File name', required=False, existing=True)
			if not path:
				return
		else:
			path = files[option]
		return path


app = Compiler()
app.__main__()
