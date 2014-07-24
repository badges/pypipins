=================
PyPI Shields/Pins
=================

.. image:: https://pypip.in/d/blackhole/badge.svg
        :target: https://pypi.python.org/pypi/blackhole/

.. image:: https://pypip.in/v/blackhole/badge.svg
        :target: https://pypi.python.org/pypi/blackhole/

.. image:: https://pypip.in/py_versions/blackhole/badge.svg
        :target: https://pypi.python.org/pypi/blackhole/

.. image:: https://pypip.in/egg/blackhole/badge.svg
        :target: https://pypi.python.org/pypi/blackhole/

.. image:: https://pypip.in/wheel/blackhole/badge.svg
        :target: https://pypi.python.org/pypi/blackhole/

.. image:: https://pypip.in/format/blackhole/badge.svg
        :target: https://pypi.python.org/pypi/blackhole/

.. image:: https://pypip.in/license/blackhole/badge.svg
        :target: https://pypi.python.org/pypi/blackhole/

PyPI Shields/Pins are shields for your GitHub repo, documentation or website that show
how many times your project has been downloaded, its latest version, whether
you provide egg and wheel distributions and what license your project is released under.

Please note, due to how PyPI works, you'll need to use the exact name of your PyPI package
i.e.

- Sphinx not sphinx
- Django not django

You will need to replace **PYPI_PKG_NAME** with your package name.

`Service Status <http://status.pypip.in/>`__
============================================

`Service status <http://status.pypip.in/>`__ is provided by the wonderful guys at `statuspage.io <https://www.statuspage.io/>`__.

Shields & Usage
===============

.. toctree::
    :maxdepth: 2

    downloads
    version
    python_versions
    wheel
    egg
    format
    license

Shield Styling
==============

You can change the style of the shield from the rounded corners to a cleaner,
flat style by setting a style value in the REQUEST_URI.

If no style is provided, the default rounded corner style will be used, setting
the style value to 'flat' will use the flat style as seen below.

.. code::

    ?style=flat

.. image:: https://pypip.in/py_versions/blackhole/badge.svg?style=flat

Using other image formats
=========================

By default, pypip.in returns images in SVG format but you can have it return
other formats by changing the badge extension.

.. code::

    https://pypip.in/download/blackhole/badge.svg

As an example you could use any of the following extensions;

- SVG
- PNG
- JPEG
- GIF
- TIFF

Thanks
======

PyPI Pins uses the wonderful http://b.repl.ca (Buckler) API.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
