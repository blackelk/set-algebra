from setuptools import setup

import set_algebra


with open('README.rst') as f:
    readme = f.read()

setup(
    name = 'set-algebra',
    packages = ['set_algebra'],
    version = set_algebra.__version__,
    author = 'Constantine Parkhimovich',
    author_email = 'cparkhimovich@gmail.com',
    url = 'https://github.com/blackelk/set-algebra',
    description = 'Algebra of Sets',
    license = 'MIT',
    long_description = readme,
    keywords = 'math set interval',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
