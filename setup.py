from distutils.core import setup
import uiset


with open('README.rst') as f:
    readme = f.read()

setup(
    name = 'uiset',
    packages = ['uiset'],
    version = uiset.__version__,
    author = 'Constantine Parkhimovich',
    author_email = 'cp@core-tech.ru',
    url = 'https://github.com/blackelk/uiset',
    download_url = 'https://github.com/blackelk/uiset/tarball/0.2.2',
    description = 'Uncountable Infinite Set',
    license = 'MIT',
    long_description = readme,
    keywords = ['math', 'set', 'interval'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
