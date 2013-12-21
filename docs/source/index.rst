=================
PyPI Shields/Pins
=================

PyPI Shields/Pins are shields for you GitHub repo, documentation or website that show
your many times your project has been downloaded from PyPI or it's latest version.

Please note, due to how PyPI works, you'll need to use the exact name of your PyPI package
i.e.

- Sphinx not sphinx
- Django not django

You'll notice my examples below all use crate.io rather than pypi.python.org, but you
can always change where the image links to or remove that entire.

You will need to replace **PYPI_PKG_NAME** with your package name.

Downloads
---------

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


Latest release
--------------

This shield displays the latest version release of your package

.. image:: https://pypip.in/v/blackhole/badge.png
    :target: https://pypi.python.org/pypi/blackhole/
    :alt: Latest Version

Image URL
~~~~~~~~~
::

    https://pypip.in/v/PYPI_PKG_NAME/badge.png

RST
~~~
::

    .. image:: https://pypip.in/v/PYPI_PKG_NAME/badge.png
        :target: https://pypi.python.org/pypi/PYPI_PKG_NAME/
        :alt: Latest Version

Markdown
~~~~~~~~
::

    [![Latest Version](https://pypip.in/v/PYPI_PKG_NAME/badge.png)](https://pypi.python.org/pypi/PYPI_PKG_NAME/)

Textile
~~~~~~~
::

    !https://pypip.in/v/PYPI_PKG_NAME/badge.png!:https://pypi.python.org/pypi/PYPI_PKG_NAME/

RDOC
~~~~
::

    {<img src="https://pypip.in/v/PYPI_PKG_NAME/badge.png" alt="Latest Version" />}[https://pypi.python.org/pypi/PYPI_PKG_NAME/]

AsciiDoc
~~~~~~~~
::

    image:https://pypip.in/v/PYPI_PKG_NAME/badge.png["Latest Version", link="https://pypi.python.org/pypi/PYPI_PKG_NAME/"]



Wheel
-----

This shield displays whether your package has a wheel version available.

.. image:: https://pypip.in/wheel/blackhole/badge.png
    :target: https://pypi.python.org/pypi/blackhole/
    :alt: Wheel Available

Image URL
~~~~~~~~~
::

    https://pypip.in/wheel/PYPI_PKG_NAME/badge.png

RST
~~~
::

    .. image:: https://pypip.in/wheel/PYPI_PKG_NAME/badge.png
        :target: https://pypi.python.org/pypi/PYPI_PKG_NAME/
        :alt: Wheel Available

Markdown
~~~~~~~~
::

    [![Wheel Available](https://pypip.in/wheel/PYPI_PKG_NAME/badge.png)](https://pypi.python.org/pypi/PYPI_PKG_NAME/)

Textile
~~~~~~~
::

    !https://pypip.in/wheel/PYPI_PKG_NAME/badge.png!:https://pypi.python.org/pypi/PYPI_PKG_NAME/

RDOC
~~~~
::

    {<img src="https://pypip.in/wheel/PYPI_PKG_NAME/badge.png" alt="Wheel Available" />}[https://pypi.python.org/pypi/PYPI_PKG_NAME/]

AsciiDoc
~~~~~~~~
::

    image:https://pypip.in/wheel/PYPI_PKG_NAME/badge.png["Wheel Available", link="https://pypi.python.org/pypi/PYPI_PKG_NAME/"]

