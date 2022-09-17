pl-chrisproject-matplotlib
================================

.. image:: https://img.shields.io/docker/v/fnndsc/pl-chrisproject-matplotlib?sort=semver
    :target: https://hub.docker.com/r/fnndsc/pl-chrisproject-matplotlib

.. image:: https://img.shields.io/github/license/fnndsc/pl-chrisproject-matplotlib
    :target: https://github.com/FNNDSC/pl-chrisproject-matplotlib/blob/master/LICENSE

.. image:: https://github.com/FNNDSC/pl-chrisproject-matplotlib/workflows/ci/badge.svg
    :target: https://github.com/FNNDSC/pl-chrisproject-matplotlib/actions


.. contents:: Table of Contents


Abstract
--------

Create static, animated, and interactive visualizations with Matplotlib for ChRIS


Description
-----------


``chrisproject_matplotlib`` is a *ChRIS ds-type* application that takes in data as text files
and produces images.


Usage
-----

.. code::

    docker run --rm fnndsc/pl-chrisproject-matplotlib chrisproject_matplotlib
        [-h|--help]
        [--json] [--man] [--meta]
        [--savejson <DIR>]
        [-v|--verbosity <level>]
        [--version]
        <inputDir> <outputDir>


Arguments
~~~~~~~~~

.. code::

    [-h] [--help]
    If specified, show help message and exit.
    
    [--json]
    If specified, show json representation of app and exit.
    
    [--man]
    If specified, print (this) man page and exit.

    [--meta]
    If specified, print plugin meta data and exit.
    
    [--savejson <DIR>] 
    If specified, save json representation file to DIR and exit. 
    
    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.
    
    [--version]
    If specified, print version number and exit. 


Getting inline help is:

.. code:: bash

    docker run --rm fnndsc/pl-chrisproject-matplotlib chrisproject_matplotlib --man

Run
~~~

You need to specify input (containing NII files) and output directories (to which PNGs of the plots would be written to) using the `-v` flag to `docker run`.


.. code:: bash

    docker run --rm -u $(id -u)                                        \
        -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing                 \
        fnndsc/pl-chrisproject-matplotlib chrisproject_matplotlib      \
        /incoming /outgoing


Development
-----------

Build the Docker container:

.. code:: bash

    docker build -t local/pl-chrisproject-matplotlib .

Run unit tests:

.. code:: bash

    docker run --rm local/pl-chrisproject-matplotlib nosetests

Examples
--------

Overview of many common plotting commands in Matplotlib: https://matplotlib.org/stable/plot_types/index.html

Example plots: https://matplotlib.org/stable/gallery/index.html


.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
