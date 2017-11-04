from setuptools import setup, find_packages
from tempus import constant

setup(
	name = 'tempus',
	packages = find_packages(),
	install_requires = [
		'click==6.7',
	],
	python_requires='>=3',
	version = constant.VERSION,
	description = 'Tempus est de essentia',
	author = 'Marcus Mu',
	author_email = 'chunkhang@gmail.com',
	license = 'UNLICENSE',
	url = 'https://github.com/chunkhang/tempus',
	keywords = [
		'tempus'
	], 
	classifiers = [
		'Intended Audience :: End Users/Desktop',
		'Environment :: Console',
		'Programming Language :: Python :: 3 :: only'
	],
	entry_points = {
		'console_scripts': [
			'tempus=tempus.main:cli'
		]
	}
)