try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='mailinator',
    version='0.1',
    author='Timothy Mellor',
    author_email='timothy.mellor+pip@gmail.com',
    url='https://github.com/mellort/mailinator',
    description='A python API for mailinator.com',
    long_description=('Please see the `documentation on github '
                      '<https://github.com/mellort/mailinator>`_.'),
    classifiers=['Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License (GPL)',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Utilities'],
    license='GPLv3',
    keywords=['mailinator', 'api'],
    packages=['mailinator'],
)

