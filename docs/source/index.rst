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

You will need to replace **PYPI_PKG_NAME** with your package name and
**VERSION_NUMBER** with the exact version as it is displayed in PyPI.


Downloads
---------

This shield shows a total of all the downloads of your package from PyPI
for every version released.

.. image:: https://pypip.in/d/blackhole/badge.png
        :target: https://crate.io/packages/blackhole
        :alt: Downloads

Query string parameters
~~~~~~~~~~~~~~~~~~~~~~~

You can modify the download shields by appending a query string. Currently you can only modify it in two ways;

+-------------------------+---------------------------------------------+------------------------------------------------------------------+
| Parameter               | Description                                 | Example                                                          |
+=========================+=============================================+==================================================================+
| ?version=latest         | Show total downloads for the latest version | .. image:: https://pypip.in/d/blackhole/badge.png?version=latest |
+-------------------------+---------------------------------------------+------------------------------------------------------------------+
| ?version=VERSION_NUMBER | Show downloads for the specified version    | .. image:: https://pypip.in/d/blackhole/badge.png?version=1.5.0  |
+-------------------------+---------------------------------------------+------------------------------------------------------------------+

Image URL
~~~~~~~~~
::

    https://pypip.in/d/PYPI_PKG_NAME/badge.png

RST
~~~
::

    .. image:: https://pypip.in/d/PYPI_PKG_NAME/badge.png
            :target: https://crate.io/packages/PYPI_PKG_NAME
            :alt: Downloads

Markdown
~~~~~~~~
::

    [![Downloads](https://pypip.in/d/PYPI_PKG_NAME/badge.png)](https://crate.io/package/PYPI_PGK_NAME)

Textile
~~~~~~~
::

    !https://pypip.in/d/PYPI_PKG_NAME/badge.png!:https://crate.io/package/PYPI_PGK_NAME

RDOC
~~~~
::

    {<img src="https://pypip.in/d/PYPI_PKG_NAME/badge.png" alt="Downloads" />}[https://crate.io/package/PYPI_PGK_NAME]

AsciiDoc
~~~~~~~~
::

    image:https://pypip.in/d/PYPI_PKG_NAME/badge.png["Downloads", link="https://crate.io/package/PYPI_PGK_NAME"]


Latest release
--------------

This shield displays the latest version release of your package

.. image:: https://pypip.in/v/blackhole/badge.png
        :target: https://crate.io/packages/blackhole
        :alt: Latest Version

Image URL
~~~~~~~~~
::

    https://pypip.in/v/PYPI_PKG_NAME/badge.png

RST
~~~
::

    .. image:: https://pypip.in/v/PYPI_PKG_NAME/badge.png
            :target: https://crate.io/packages/PYPI_PKG_NAME
            :alt: Latest Version

Markdown
~~~~~~~~
::

    [![Latest Version](https://pypip.in/v/PYPI_PKG_NAME/badge.png)](https://crate.io/package/PYPI_PGK_NAME)

Textile
~~~~~~~
::

    !https://pypip.in/v/PYPI_PKG_NAME/badge.png!:https://crate.io/package/PYPI_PGK_NAME

RDOC
~~~~
::

    {<img src="https://pypip.in/v/PYPI_PKG_NAME/badge.png" alt="Latest Version" />}[https://crate.io/package/PYPI_PGK_NAME]

AsciiDoc
~~~~~~~~
::

    image:https://pypip.in/v/PYPI_PKG_NAME/badge.png["Latest Version", link="https://crate.io/package/PYPI_PGK_NAME"]

