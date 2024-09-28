from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='ConsoleAppBase',
	version='1.0.0',
	author='Ondřej (Binič) Bína',
	author_email='xbinao@seznam.cz',
	description='Console App Base',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=find_packages(),
	license='MIT',
	install_requires=[
		# eg: 'numpy>=1.11.1' 
	],
)
