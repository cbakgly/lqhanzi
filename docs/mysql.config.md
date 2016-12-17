Config MySQL
============
> Author: xianduan
> Email: quqinglei@icloud.com
> Date: 2016-12-17

On Debian/Ubuntu based distributions
---------------------------------------

1. Install MySQL Server and Python MySQL client
```bash
sudo apt-get install mysql-server # Set root password
sudo apt-get install python-mysqldb
```
2. Edit mysql-server bind-address config to `0.0.0.0`
```bash
bind-address		= 0.0.0.0
```

3. Connect to MySQL Server and create database
```mysql
mysql> create database lqhanzi default character set utf8 collate utf8_general_ci;
Query OK, 1 row affected (0.01 sec)

mysql> -- If you want to make testcase works, you should give privileges to current mysql user --
mysql> grant all privileges on *.* to lq@'%' identified by '123456'; 
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)
```
On redhat Based distributions
-----------------------------
Like on Debian based system
```bash
sudo yum install mysql-server
```

On Windows
----------
1. Download setup packages from the website https://www.mysql.com/downloads/
2. Install it
3. Like Debian

On macOs
--------
1. Download MySQL Server from https://www.mysql.com/downloads/
2. Install it 
3. Just do next ... like Debian
