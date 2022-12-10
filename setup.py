from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'chrisproject_matplotlib',
    version          = '0.1',
    description      = 'Create static, animated, and interactive visualizations with Matplotlib for ChRIS',
    long_description = readme,
    author           = 'rohanarora',
    author_email     = 'rohan@rohanarora.name',
    url              = 'http://wiki',
    packages         = ['chrisproject_matplotlib'],
    install_requires = ['chrisapp', 'matplotlib', 'numpy', 'nibabel'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'chrisproject_matplotlib = chrisproject_matplotlib.__main__:main'
            ]
        }
)
