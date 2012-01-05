import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='weathercli',
    version='1.0.0',
    author='Brian Riley',
    author_email='brian@btriley.com',
    description="A command line weather tool",
    url='https://github.com/brianriley/weather-cli',
    packages=find_packages(),
    long_description=read('README.mkd'),
    install_requires=['clint'],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'weather = weathercli.main:main',
        ]
    },
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Topic :: Utilities'
    ]
)
