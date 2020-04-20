.. _install:

************
Installation
************

Supported versions
------------------

* Python 3.5+

Dependencies
------------

#. `Kivy <https://kivy.org/#download>`_


Installation
------------

Install it from PyPI via::

    python -m pip install kivy_garden.mapview

Or even shorter::

    python -m pip install mapview

Alternatively, you can install mapview develop directly from github with::

    python -m pip install https://github.com/kivy-garden/mapview/archive/master.zip

Look under the `releases tab <https://github.com/kivy-garden/mapview/releases>`_ if you'd like to
install a specific release or a pre-compiled wheel, if the flower has any.
Then use the url with `pip`.

Or you can automatically install it using garden's pypi server with::

    python -m pip install kivy_garden.mapview --extra-index-url https://kivy-garden.github.io/simple/

To permanently add our garden server to your pip configuration so that you
don't have to specify it with `--extra-index-url`, add::

    [global]
    timeout = 60
    index-url = https://kivy-garden.github.io/simple/

to your `pip.conf <https://pip.pypa.io/en/stable/user_guide/#config-file>`_.

Please see the `garden docs <https://kivy-garden.github.io/>`_ for further installation instructions.
