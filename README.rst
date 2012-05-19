Dozens
======

Wrapper for `Dozens`_ API

.. image:: https://secure.travis-ci.org/mikamix/dozens.png?branch=master
    :target: http://travis-ci.org/mikamix/dozens

Install
-------

::

    $ pip install dozens

Usage
-----

::

    from dozens import Dozens

    user = 'user'               # user name for Dozens
    key = 'key'                 # your API key
    dozens = Dozens(user, key)  # create instance
    dozens.start()              # get token and hold it

See `API doc`_ for more detail.

License
-------

Distributed under the `MIT License`.

.. _Dozens: https://dozens.jp/
.. _API doc: https://sites.google.com/a/dozens.jp/docs/
.. _MIT License: http://www.opensource.org/licenses/mit-license.php