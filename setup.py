from distutils.core import setup

setup(
    name='geonition_utils',
    version='2.0.0',
    author='Kristoffer Snabb',
    url='https://github.com/geonition/django_geonition_utils',
    packages=['geonition_utils'],
    install_requires=['django',
                      'pymongo'],
)
