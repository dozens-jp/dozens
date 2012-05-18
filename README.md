Dozens
======

Wrapper for [Dozens][site] API

[![Build Status](https://secure.travis-ci.org/mikamix/dozens.png?branch=master)](http://travis-ci.org/mikamix/dozens)

Usage
-----

    from dozens import Dozens

    user = 'user'               # user name for Dozens
    key = 'key'                 # your API key
    dozens = Dozens(user, key)  # create instance
    dozens.start()              # get token and hold it

See [API doc][api] for more detail.

License
-------

Distributed under the [MIT License][mit].

[site]: https://dozens.jp/
[api]: https://sites.google.com/a/dozens.jp/docs/
[mit]: http://www.opensource.org/licenses/mit-license.php