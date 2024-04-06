#!/usr/bin/env python3

from ConsoleAppTemplate import *

class MyApp(Core):
	def __init__(self):
		config: Config = Config(
			self.__config_loader,
			self.__config_saver,
			os.path.splitext(os.path.basename(__file__))[0] + '.conf',
			self.__config_loader({})
		)
		config.load()
		super().__init__(
			'{{self.config.locale.COUNTER}}: {{self.config.data[\'counter\']}}',
			Menu(
				{
					'counterDisplay': MenuItem('{{self.config.locale.COUNTER}}: {{self.config.data[\'counter\']}}', title_only=True),
					'E': MenuItem('{{self.config.locale.VALUE_EDIT}}', submenu={
						'counterDisplay': MenuItem('{{self.config.locale.COUNTER}}: {{self.config.data[\'counter\']}}', title_only=True),
						'I': MenuItem('{{self.config.locale.INCREASE}}', self.counter_increase),
						'D': MenuItem('{{self.config.locale.DECREASE}}', self.counter_decrease),
						'IT': MenuItem('{{self.config.locale.translate(\'INCREASE_BY\', 10)}}', self.counter_increase, [10]),
						'S': MenuItem('{{self.config.locale.SET_VALUE}}', self.counter_set_prompt),
						'C': MenuItem('{{self.config.locale.CLEAR_COUNTER}}', self.counter_clear_prompt),
						'b': MenuItem('{{self.config.locale.BACK}}', self.menu_back)
					}),
					'L': MenuItem('{{self.config.locale.LANGUAGE}} ({{self.config.lang}})', self.prompt_change_language, [{'en': 'ENGLISH', 'cs': 'CZECH'}, False]),
					'q': MenuItem('{{self.config.locale.QUIT}}', self.clean_and_exit),
				},
				self
			),
			config
		)

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
		self.counter_set(self.input_int(self.config.locale.NEW_VALUE))

	def counter_clear(self) -> None:
		self.config.data['counter'] = 0
		self.config.save()

	def counter_clear_prompt(self) -> None:
		if self.input_bool('Clear counter'):
			self.counter_clear()



app = MyApp()
app.__main__()
