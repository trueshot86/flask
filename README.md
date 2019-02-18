# flask

* [what is this?](#what-is-this)
* [install](#install)
* [command](#command)

## What is this?
this is my flask template.



## install
```
$ pip install flask
$ (localedef -f UTF-8 -i ja_JP ja_JP.UTF-8)
$ (export LC_ALL=ja_JP.utf8)
```

## command
- python server.py
  - run flask.

## tips
- install mysql
  - curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash
  - yum install MariaDB-server MariaDB-client -y
  - systemctl start mariadb
  - systemctl enable mariadb
  - mysql_secure_installation

- setting mysql
  - create database infra;
  - create table dns(id integer primary key auto_increment, ip text, domain text, mac text, username text, dhcp_flag int default 0, lock_flag int default 0);
  - insert into dns(ip, domain, username) values('192.168.100.1','yamaha-rtx.xxx','system_admin');
  - select * from dns;

- to use sqlalchemy
  - pip install sqlalchemy
  - yum install MariaDB-shared MariaDB-devel -y
  - pip install mysqlclient

