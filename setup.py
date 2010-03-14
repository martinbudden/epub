from setuptools import setup, find_packages

from epub import __version__ as VERSION


setup(
    name = 'epub',
    version = VERSION,
    description = 'Produce epub files form mediawiki and wikisource',
    author = 'Martin Budden',
    author_email = '',
    platforms = 'Posix; MacOS X; Windows',
    scripts = ['example_script'],
    packages = find_packages(exclude=['test']),
    install_requires = [
        'mwlib',
        'jinja2',
        'PIL'],
    include_package_data = True,
    zip_safe = False
    )
