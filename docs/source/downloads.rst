=========
Downloads
=========

This shield shows your package downloads, it defaults to use total this month but can
show today, this week or this month.

.. image:: https://pypip.in/download/blackhole/badge.svg?period=day&style=flat
    :target: https://pypi.python.org/pypi/blackhole/
    :alt: Downloads

.. image:: https://pypip.in/download/blackhole/badge.svg?period=week&style=flat
    :target: https://pypi.python.org/pypi/blackhole/
    :alt: Downloads

.. image:: https://pypip.in/download/blackhole/badge.svg?period=month&style=flat
    :target: https://pypi.python.org/pypi/blackhole/
    :alt: Downloads

Query string parameters
~~~~~~~~~~~~~~~~~~~~~~~

You can modify the download shields by appending a query string. Currently you can only modify it in two ways;

+--------------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| Parameter                      | Description                                 | Example                                                               |
+================================+=============================================+=======================================================================+
| ?period=day|week|month         | Show total downloads for the latest version | .. image:: https://pypip.in/download/blackhole/badge.svg?period=month |
+--------------------------------+---------------------------------------------+-----------------------------------------------------------------------+

Sadly, with the changes to PyPI and crate.io being discontinued, the ability to count downloads for specific versions and for an entire total
has had to be removed. Sorry.

Image URL
~~~~~~~~~
::

    https://pypip.in/download/PYPI_PKG_NAME/badge.svg

RST
~~~
::

    .. image:: https://pypip.in/download/PYPI_PKG_NAME/badge.svg
        :target: https://pypi.python.org/pypi//PYPI_PKG_NAME/
        :alt: Downloads

Markdown
~~~~~~~~
::

    [![Downloads](https://pypip.in/download/PYPI_PKG_NAME/badge.svg)](https://pypi.python.org/pypi/PYPI_PKG_NAME/)
