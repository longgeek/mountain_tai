====
MOUNTAIN_TAI
====


Why moutain_tai? It is like moutain tai, it's strong enougth to scheduler data about docker host.

Getting Started
---------------

If you'd like to run from the master branch, you can clone the git repo:

    git clone git@git.pyindex.com:reviewdev/mountain_tai.git


* Wiki: http://wiki.pyindex.com


AMQP Client - Python Pika
-------------
https://github.com/pika/pika

References
----------
* http://wiki.pyindex.com

We have integration with
------------------------
* git@git.pyindex.com:reviewdev/looker.git (online)
* git@git.pyindex.com:reviewdev/boss.git (online manager)
* git@git.pyindex.com:reviewdev/telegraph_pole (restful api)
* git@git.pyindex.com:reviewdev/bat.git (create)

How to use (For Ubuntu-14.04.1 Server)
--------------------------------------
Dependent on the installation of the mountain_tai:
    git clone git@git.pyindex.com:reviewdev/mountain_tai.git
    cd mountain_tai/
    pip install -r requirements.txt
    python setup.py install (Develop mode: python setup.py develop)

The configuration file:
    cd mountain_tai/
    cp -r etc/* /etc/
    cp sbin/mountain-scheduler /usr/sbin/
    mkdir /var/log/mountain
    chown :adm /var/log/mountain
    logrotate -f /etc/logrotate.d/mounatin-tai
    service rsyslog restart

Modify the configuration file:
    vim /etc/mountain/mountain.conf
    ....

Run it:
    service mountain-tai restart

Log:
    tail -f /var/log/mountain/moutain.log
