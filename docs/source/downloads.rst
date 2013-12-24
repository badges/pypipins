=========
Downloads
=========

This shield shows your package downloads, it defaults to use total this month but can
show today, this week or this month.

.. image:: https://pypip.in/d/blackhole/badge.png
    :target: https://pypi.python.org/pypi/blackhole/
    :alt: Downloads

Query string parameters
~~~~~~~~~~~~~~~~~~~~~~~

You can modify the download shields by appending a query string. Currently you can only modify it in two ways;

+--------------------------------+---------------------------------------------+----------------------------------------------------------------+
| Parameter                      | Description                                 | Example                                                        |
+================================+=============================================+================================================================+
| ?period=day|week|month         | Show total downloads for the latest version | .. image:: https://pypip.in/d/blackhole/badge.png?period=month |
+--------------------------------+---------------------------------------------+----------------------------------------------------------------+

Sadly, with the changes to PyPI and crate.io being discontinued, the ability to count downloads for specific versions and for an entire total
has had to be removed. Sorry.

Image URL
~~~~~~~~~
::

    https://pypip.in/d/PYPI_PKG_NAME/badge.png

RST
~~~
::

    .. image:: https://pypip.in/d/PYPI_PKG_NAME/badge.png
        :target: https://pypi.python.org/pypi//PYPI_PKG_NAME/
        :alt: Downloads

Markdown
~~~~~~~~
::

    [![Downloads](https://pypip.in/d/PYPI_PKG_NAME/badge.png)](https://pypi.python.org/pypi/PYPI_PKG_NAME/)

Textile
~~~~~~~
::

    !https://pypip.in/d/PYPI_PKG_NAME/badge.png!:https://pypi.python.org/pypi/PYPI_PKG_NAME/

RDOC
~~~~
::

    {<img src="https://pypip.in/d/PYPI_PKG_NAME/badge.png" alt="Downloads" />}[https://pypi.python.org/pypi/PYPI_PKG_NAME/]

AsciiDoc
~~~~~~~~
::

    image:https://pypip.in/d/PYPI_PKG_NAME/badge.png["Downloads", link="https://pypi.python.org/pypi/PYPI_PKG_NAME/"]

