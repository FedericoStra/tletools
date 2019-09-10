#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md") as fp:
    long_description = fp.read()

setup(
    name='TLE-tools',
    version='0.2.0.post0',
    description='Library to work with two-line element set files',
    license='MIT',
    author='Federico Stra',
    author_email='stra.federico@gmail.com',
    url='https://federicostra.github.io/tletools',
    project_urls={
        'Documentation': 'https://tletools.readthedocs.io',
        'Code': 'https://github.com/FedericoStra/tletools',
        'Issue tracker': 'https://github.com/FedericoStra/tletools/issues',
    },
    packages=find_packages(include='tletools.*'),
    python_requires='>=3.4',
    install_requires=[
        'attrs>=19.0.0',
        'numpy>=1.16.0',
        'pandas>=0.24.0',
        'astropy>=3.2.0',
        'poliastro>=0.12.0',
    ],
    tests_require=[
        'flake8>=3.7.0',
        'pytest>=5.0.0',
    ],
    extras_require={
        'dev': [
            'pytest',
            'coverage',
            'tox',
            'sphinx',
            'pallets-sphinx-themes',
            'sphinxcontrib-log-cabinet',
            'sphinx-issues',
        ],
        'docs': [
            'sphinx',
            'sphinx-rtd-theme',
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Framework :: IPython',
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
