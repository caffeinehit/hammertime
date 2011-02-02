Hammertime
==========

Git based time tracking. Use it either with your repository you're
doing work in, or create a new repository to track your work.

Installation
------------

Either with ``pip`` or ``easy_install``:

::

    $ easy_install Hammertime
    $ pip install Hammertime

Usage
-----

::

    $ cd /repository
    $ git time start -m "Doing some work"
    $ # do work, commits, etc
    $ git time stop -m "Not doing work anymore"
    $ git time show

If you've got a
`json command line utility <https://github.com/zpoley/json-command>`_
installed, try something like:

::

    $ git time show | json -o times delta
    $ git time show | json -o times start.message end.message delta

Help
----

::

    $ git time -h

Note
----

Invoking ``git time stop`` in sequence twice or more will always
override the last ``git time stop`` entry. Invoking
``git time start`` will always create new entries.

Example session
---------------

::

    alen@mu:[hammertime ~master]$ git time start -m "Starting something to work on"
    alen@mu:[hammertime ~master]$ vim README.md 
    alen@mu:[hammertime ~master]$ git commit -am "Saved the example session"
    [master 11a0c98] Saved the example session
     1 files changed, 5 insertions(+), 0 deletions(-)
    alen@mu:[hammertime ~master]$ git time stop -m "Readme updates with example session"
    alen@mu:[hammertime ~master]$ git time show 
    {"times": [{"start": {"message": "Starting something to work on", "time": "2011-02-02T13:37:44.761185"}, "stop": {"message": "Readme updates with example session", "time": "2011-02-02T13:39:21.330041"}, "delta": "0:01:36"}]}
    alen@mu:[hammertime ~master]$ git time show | json -o times delta
    {
      "delta": "0:01:36"
    }
    alen@mu:[hammertime ~master]$ git time show | json -o times delta start.message stop.message
    {
      "delta": "0:01:36",
      "start": {
        "message": "Starting something to work on"
      },
      "stop": {
        "message": "Readme updates with example session"
      }
    }


