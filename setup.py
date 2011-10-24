from distutils.core import setup

setup(
    name='geonition_utils',
    version='1.0.x',
    author='Kristoffer Snabb',
    url='https://github.com/geonition/django_geonition_utils',
    packages=['geonition_utils'],
    install_requires=['django',
                      'pymongo'],
)
