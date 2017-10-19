.. role:: bash(code)
   :language: bash

.. role:: python(code)
   :language: python

=============
pycontextfree
=============

.. image:: https://api.travis-ci.org/undertherain/pycontextfree.svg?branch=master
    :target: https://travis-ci.org/undertherain/pycontextfree
    :alt: build status from Travis CI

.. image:: https://coveralls.io/repos/github/undertherain/pycontextfree/badge.svg?branch=master
    :target: https://coveralls.io/github/undertherain/pycontextfree?branch=master

.. image:: https://badge.fury.io/py/contextfree.svg
    :target: https://badge.fury.io/py/contextfree
    :alt: pypi version

`CFDG
<https://www.contextfreeart.org/>`_-inspired cairo-based pythonic generative art tool

Here is an example of simple code producing stochastic fractal tree:

.. code:: python

    from contextfree.contextfree import *
    @check_limits
    def branch():
        line(0, 1)
        with translate(0, 0.9):
            with scale(0.7 + rnd(0.3)):
                with rotate(-0.4 + rnd(0.5)):
                    branch()
                with rotate(0.4 + rnd(0.5)):
                    branch()
    init(canvas_size=(300, 300))
    with translate(0, -1):
        with scale(0.6):
            branch()
    display_ipython()

Here is the output:

.. image:: https://user-images.githubusercontent.com/1635907/30413703-9e585f54-995a-11e7-8566-bdded386be8d.png
   :alt: [tree_example]
   :align: center

Check examples folder for more fun stuff. 

How do I get set up?
--------------------

* ``pip3 install contextfree`` for latest stable release
* ``pip3 install git+https://github.com/undertherain/pycontextfree.git`` for recent development version
* Python 3.4 or later is required

