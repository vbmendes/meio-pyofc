# Geraldo setup

# Downloads setuptools if not find it before try to import
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup
from meiopyofc import get_version

setup(
    name = 'meiopyofc',
    version = get_version(),
    description = 'meiopyofc is a Python binding for Open Flash Chart 2',
    long_description = 'meiopyofc is a Python binding for Open Flash Chart 2 to generate the JSON required to display beautiful charts.',
    author = 'Vinicius Mendes',
    author_email = 'vbmendes@gmail.com',
    url = 'http://github.com/vbmendes/meio-pyofc/',
    license = 'BSD License',
    packages = ['meiopyofc',],
    install_requires = ['django'],
)
