
blogspam.net
============

The site https://blogspam.net/ is generated from a series of templates,
via the [templer static site generator](http://github.com/skx/templer).

This repository contains the source which is used to generate that site.


Building
--------

To build the site, assuming you have templer installed, you should be
able to run `templer` with no arguments.

The supplied `Makefile` will do this automatically if called with
no arguments::

     precious ~/git/www.blogspam.net $ make
     templer

     All done: 24 page(s) updated in less than 1 second.


Testing
-------

If you run `make serve` you can open the rebuilt site by point your browser
at the following URL:

* http://localhost:4433/

Steve
--
