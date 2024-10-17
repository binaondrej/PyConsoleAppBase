#!/usr/bin/env python3

import json

from ConsoleAppBase.LocaleBase import LocaleBase


class Config[LOCALE: LocaleBase]:
	def __init__(self, locales: dict[str, type[LOCALE]], default_lang: str, loader: callable = None, saver: callable = None, path: str|None = None, default_data: dict = {}) -> None:
		"""
		Parameters
		----------
		locales: dict[str, LOCALE]
			dict of available locales eg: { 'en': LanguageEn(), 'cs': LanguageCs() }
		default_lang: str
			shortcut for language (en/cs/...)
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
		Returns
		-------
		bool
			if the loader was successful
		"""
		self.__instantiated = False

		self.__locales: dict[str, type[LOCALE]] = {key.lower(): value for key, value in locales.items()}
		self.__locale: LOCALE = LocaleBase()
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
		lang = lang.lower()
		if not lang in self.__locales:
			raise ValueError(self.locale.translate('INVALID_LANGUAGE', lang))
		self.__lang = lang
		self.__locale = self.__locales[lang]()
		if self.__instantiated and self.path and self.saver:
			self.save()
	@property
	def locale(self) -> LOCALE:
		return self.__locale

	def load(self, path: str = None) -> bool:
		if self.loader is None:
			raise NotImplementedError(self.locale.LOADER_IMPLEMENTATION_IS_NOT_CONFIGURED)
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
			raise NotImplementedError(self.locale.SAVER_IMPLEMENTATION_IS_NOT_CONFIGURED)
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
