from setuptools import setup, find_packages


description = 'A Python 3 utility to interact with Wikipedia'
url = 'https://github.com/AKAlex92/search_wikipedia'
requires = ['urllib3==1.25.7',
			'wikipedia==1.4.0'
			]

with open('README.md', 'r') as f:
	readme = f.read()

setup(
	name                 = 'search_wikipedia',
	version              = version,
	description          = description,
	long_description     = readme,
	author               = 'Alessandro Ripa',
	author_email         = 'alessandroclion18@gmail.com',
	url                  = url,
	license              = 'MIT License',
	python_requires      = '>=3.6.0',
	install_requires     = requires,
	packages             = find_packages(),
	include_package_data = True,
	)