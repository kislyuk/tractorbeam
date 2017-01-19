Tractor Beam: File I/O staging for JSON documents with Amazon S3 URLs
=====================================================================
Tractor Beam is a utility to download S3 URLs using the AWS CLI. If you have structured input (JSON) for your application, and
that input contains references to files on S3, and your application expects these files to be on a local POSIX path, then you
can pipe your JSON through ``tractor pull`` to download these URLs and rewrite the JSON to contain ``file://`` URLs instead.
You can also do the reverse with ``tractor push``.

Installation
------------
::

    pip install tractorbeam

Synopsis
--------

Use ``aws configure`` to set up your AWS command line environment.

.. code-block:: bash

    $ echo '{"input1": "s3://mybucket/path/to/myfile.bam"}' | tractor pull --strip-components 1
    {"input1": "file:///cwd/path/to/myfile.bam"}
    
    $ echo '{"input2": "file:///path/to/myfile.bam"}' | tractor push s3://mybucket/prefix/ --strip-components 0
    {"input2": "s3://mybucket/prefix/path/to/myfile.bam"}

Authors
-------
* Andrey Kislyuk

Links
-----
* `Project home page (GitHub) <https://github.com/kislyuk/tractorbeam>`_
* `Documentation (Read the Docs) <https://tractorbeam.readthedocs.io/en/latest/>`_
* `Package distribution (PyPI) <https://pypi.python.org/pypi/tractorbeam>`_
* `Change log <https://github.com/kislyuk/tractorbeam/blob/master/Changes.rst>`_

Bugs
~~~~
Please report bugs, issues, feature requests, etc. on `GitHub <https://github.com/kislyuk/tractorbeam/issues>`_.

License
-------
Licensed under the terms of the `Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_.

.. image:: https://img.shields.io/travis/kislyuk/tractorbeam.svg
        :target: https://travis-ci.org/kislyuk/tractorbeam
.. image:: https://codecov.io/github/kislyuk/tractorbeam/coverage.svg?branch=master
        :target: https://codecov.io/github/kislyuk/tractorbeam?branch=master
.. image:: https://img.shields.io/pypi/v/tractorbeam.svg
        :target: https://pypi.python.org/pypi/tractorbeam
.. image:: https://img.shields.io/pypi/l/tractorbeam.svg
        :target: https://pypi.python.org/pypi/tractorbeam
.. image:: https://readthedocs.org/projects/tractorbeam/badge/?version=latest
        :target: https://tractorbeam.readthedocs.io/
