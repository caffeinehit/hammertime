# Hammertime

Git based time tracking. Use it either with your repository you're doing
work in, or create a new repository to track your work. 

## Installation

Either with `pip` or `easy_install`:

    $ easy_install Hammertime
    $ pip install Hammertime

## Usage

    $ cd /repository
    $ git time start -m "Doing some work"
    $ # do work, commits, etc
    $ git time stop -m "Not doing work anymore"
    $ git time show

If you've got a [json command line utility](https://github.com/zpoley/json-command) installed, try something like:

    $ git time show | json -o times delta
    $ git time show | json -o times start.message end.message delta

## Help

    $ git time -h

## Note

Invoking `git time stop` in sequence twice or more will always override
the last `git time stop` entry. Invoking `git time start` will always
create new entries.

## Example session

    alen@mu:[hammertime ~master]$ git time start -m "Starting something to work on"
    alen@mu:[hammertime ~master]$ vim README.md 
