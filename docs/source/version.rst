==============
Latest release
==============

This shield displays the latest version release of your package.

.. image:: https://pypip.in/version/blackhole/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/blackhole/
    :alt: Latest Version

Query string parameters
~~~~~~~~~~~~~~~~~~~~~~~

You can modify the shield using the query string.

+---------------+--------------------------------+---------------------------------------------------------------------------------+
| Parameter     |                                | Example                                                                         |
+===============+================================+=================================================================================+
| ?text=pypi    | Show the word "pypi" [default] | .. image:: https://pypip.in/version/blackhole/badge.svg?style=flat              |
+---------------+--------------------------------+---------------------------------------------------------------------------------+
| ?text=version | Show the word "version"        | .. image:: https://pypip.in/version/blackhole/badge.svg?style=flat&text=version |
+---------------+--------------------------------+---------------------------------------------------------------------------------+

Image URL
~~~~~~~~~
::

    https://pypip.in/version/<PYPI_PKG_NAME>/badge.svg

RST
~~~
.. code-block:: rst

    .. image:: https://pypip.in/version/<PYPI_PKG_NAME>/badge.svg
        :target: https://pypi.python.org/pypi/<PYPI_PKG_NAME>/
        :alt: Latest Version

Markdown
~~~~~~~~
::

    [![Latest Version](https://pypip.in/version/<PYPI_PKG_NAME>/badge.svg)](https://pypi.python.org/pypi/<PYPI_PKG_NAME>/)
